package com.cse03.backend.controller;


import com.cse03.backend.dto.request.RequestLogin;
import com.cse03.backend.dto.request.RequestSignUp;
import com.cse03.backend.dto.response.ResponseSignUp;
import com.cse03.backend.entity.RefreshToken;
import com.cse03.backend.entity.ResponseUserRegistration;
import com.cse03.backend.entity.TokenResponse;
import com.cse03.backend.entity.User;
import com.cse03.backend.exception.DBException;
import com.cse03.backend.exception.DenialException;
import com.cse03.backend.repository.RefreshTokenRepository;
import com.cse03.backend.repository.UserRepository;
import com.cse03.backend.service.impl.CookieService;
import com.cse03.backend.service.impl.JwtService;
import com.cse03.backend.service.UserService;
import com.cse03.backend.service.impl.UserServiceImpl;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.UUID;

@RestController
@Slf4j
public class AuthenticationController {


    private final UserServiceImpl userServiceImpl ;

    private final AuthenticationManager authenticationManager ;

    private final UserRepository userRepository  ;


    private final JwtService jwtService ;

    private final RefreshTokenRepository refreshTokenRepository ;

    private final CookieService cookieService ;

    public AuthenticationController( UserService userService, UserServiceImpl userServiceImpl , AuthenticationManager authenticationManager , UserRepository userRepository , JwtService jwtService , RefreshTokenRepository refreshTokenRepository , CookieService cookieService ) {
        this.userServiceImpl = userServiceImpl;
        this.authenticationManager = authenticationManager;
        this.userRepository = userRepository;

        this.jwtService = jwtService;
        this.refreshTokenRepository = refreshTokenRepository;
        this.cookieService = cookieService;
    }

    @PostMapping("/signup/")
    public ResponseEntity<ResponseSignUp> signup ( @Valid @RequestBody RequestSignUp requestSignUp ) {

        userServiceImpl.findByEmail(requestSignUp.email()).ifPresent(
                user -> {
                    throw new DenialException(
                            "Already user exists with email-id: " + user.getEmail()
                    );
                }
        );

        ResponseSignUp responseSignUp = null;

        try {

            responseSignUp = userServiceImpl.createUser ( requestSignUp );
        } catch (Exception e) {

            log.error( "Error for signup :  {}" , e.getMessage ( ) );
        }

        return ResponseEntity.ok ( responseSignUp );
    }


    @PostMapping("/login")
    public ResponseEntity<?> login ( @RequestBody RequestLogin loginRequest , HttpServletResponse response )  {
        String username = loginRequest.username();
        String password = loginRequest.password();


        try {
            Authentication authentication = authenticationManager
                    .authenticate(new UsernamePasswordAuthenticationToken (username,password)) ;

            User user = userRepository.findByUsername(username).orElseThrow(()->
                    new DBException ("user not found with username " + username)) ;

            //generate jti for refresh token
            String jti = UUID.randomUUID().toString() ;

            //refresh token build
            RefreshToken refreshTokenObj = RefreshToken.builder()
                    .jti(jti)
                    .user(user)
                    .createdAt( Instant.now())
                    .expiresAt(Instant.now().plusMillis(jwtService.getRefreshTokenExpiration()))
                    .revoked(false)
                    .build() ;

            // save
            refreshTokenRepository.save(refreshTokenObj) ;

            // generate access token
            String accessToken  = jwtService.generateAccessToken(user) ;

            // generate refresh token
            String refreshToken = jwtService.generateRefreshToken(user,refreshTokenObj.getJti()) ;

            // attach refresh token to cookie
            cookieService.attachRefreshCookie(response , refreshToken , Math.toIntExact(jwtService.getRefreshTokenExpiration()));

            // add no store in headers
            cookieService.addNoStoreHeaders(response);

            // return TokenResponse ;
            return ResponseEntity.ok( new TokenResponse (accessToken , refreshToken , jwtService.getAccessTokenExpiration(),
                    new ResponseUserRegistration (user.getId() , user.getEmail() , user.getUsername() ,
                             user.getLoginAuthProvider ()))
            );
        } catch (AuthenticationException e) {
            throw new DenialException (e.getMessage());
        } catch (DBException e) {
            throw new DBException(e.getMessage());
        }
    }

    @PostMapping("/refresh")
    public ResponseEntity<TokenResponse> refreshToken( HttpServletRequest request , HttpServletResponse response){

        String refreshToken  = null ;

        String refreshHeader = request.getHeader("X-REFRESH-TOKEN") ;
        if(refreshHeader!=null && !refreshHeader.isBlank()){
            refreshToken = refreshHeader.trim();
        }

        if(refreshToken!=null && jwtService.isRefreshToken(refreshToken)){
            String jti = jwtService.getJti(refreshToken) ;

            RefreshToken oldRefreshToken = refreshTokenRepository.findByJti(jti)
                    .orElseThrow(()-> new BadCredentialsException ("the refresh token ain't exist")) ;

            if(oldRefreshToken.isRevoked()){
                throw new BadCredentialsException("refreshToken has been revoked")  ;
            }

            if(oldRefreshToken.getExpiresAt().isBefore(Instant.now())){
                throw new BadCredentialsException("refresh token expired") ;
            }

            // revoke -> true
            oldRefreshToken.setRevoked(true);

            //generate new jti for new refresh token
            String newJti = UUID.randomUUID().toString() ;

            // set replaced by field from null to new jti
            oldRefreshToken.setReplacedByToken(newJti);

            // save the changes
            refreshTokenRepository.save(oldRefreshToken) ;

            User user = oldRefreshToken.getUser() ;


            // generate new Refresh Token
            RefreshToken refreshTokenObj = RefreshToken.builder()
                    .jti(newJti)
                    .user(user)
                    .createdAt(Instant.now())
                    .expiresAt(Instant.now().plusMillis(jwtService.getRefreshTokenExpiration()))
                    .revoked(false)
                    .build() ;

            // save
            refreshTokenRepository.save(refreshTokenObj) ;

            // generate new access token
            String newAccessToken  = jwtService.generateAccessToken(user) ;

            // generate new refresh token
            String newRefreshToken = jwtService.generateRefreshToken(user,refreshTokenObj.getJti()) ;

            // attach refresh token to cookie
            cookieService.attachRefreshCookie(response , newRefreshToken , Math.toIntExact(jwtService.getRefreshTokenExpiration()));

            // add no store in headers
            cookieService.addNoStoreHeaders(response);

            // return TokenResponse ;
            return ResponseEntity.ok( new TokenResponse(newAccessToken , newRefreshToken , jwtService.getAccessTokenExpiration(),
                    new ResponseUserRegistration(user.getId() , user.getEmail() , user.getUsername() ,
                             user.getLoginAuthProvider()))
            );
        }
        return null ;
    }

    @PostMapping("/logout")
    public ResponseEntity<Void>  logout (HttpServletRequest request , HttpServletResponse response){
        String refreshToken  = null ;

        String refreshHeader = request.getHeader("X-REFRESH-TOKEN") ;
        if(refreshHeader!=null && !refreshHeader.isBlank()){
            refreshToken = refreshHeader.trim();

            if(refreshToken!=null && jwtService.isRefreshToken(refreshToken)) {
                String jti = jwtService.getJti(refreshToken);

                RefreshToken oldRefreshToken = refreshTokenRepository.findByJti(jti)
                        .orElseThrow(() -> new BadCredentialsException("the refresh token ain't exist"));

                oldRefreshToken.setRevoked(true);
                refreshTokenRepository.save(oldRefreshToken) ;

                cookieService.clearRefreshCookie(response) ;
                cookieService.addNoStoreHeaders(response);

                SecurityContextHolder.clearContext();
                return ResponseEntity.status( HttpStatus.NO_CONTENT).build();
            }
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
    }


}
