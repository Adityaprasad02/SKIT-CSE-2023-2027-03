package com.cse03.backend.filter;

import com.cse03.backend.service.JwtService;
import com.cse03.backend.service.impl.CustomUserDetailService;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;


@Component
public class JwtFilter extends OncePerRequestFilter {


    private final CustomUserDetailService customUserDetailService ;

    private final JwtService jwtService ;

    public JwtFilter ( CustomUserDetailService customUserDetailService , JwtService jwtService ) {
        this.customUserDetailService = customUserDetailService;
        this.jwtService = jwtService;
    }

    @Override
    protected void doFilterInternal ( HttpServletRequest request , HttpServletResponse response , FilterChain filterChain ) throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization")  ;

        try {
            if(authHeader!=null && authHeader.startsWith("Bearer ")){

                String token = authHeader.substring(7) ;

                if(!jwtService.isAccessToken(token)){
                    filterChain.doFilter(request,response);
                    return;
                }


                if(!jwtService.isJwtValid(token)){
                    // Token is expired or invalid — skip authentication and let
                    // Spring Security return 401 via the configured entry point.
                    filterChain.doFilter(request, response);
                    return;
                }

                String username = jwtService.extractUsername(token) ;

                if(username!=null && SecurityContextHolder.getContext().getAuthentication()==null){

                    UserDetails userDetails = customUserDetailService.loadUserByUsername(username);

                    if(userDetails.isEnabled()) {
                        UsernamePasswordAuthenticationToken authenticationToken
                                = new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());

                        authenticationToken.setDetails(new WebAuthenticationDetailsSource ().buildDetails(request));

                        SecurityContext context = SecurityContextHolder.createEmptyContext();

                        context.setAuthentication(authenticationToken);
                        SecurityContextHolder.setContext(context);
                    }

                }
            }
        } catch (Exception e) {
            // Token parsing / validation failed — continue unauthenticated
            logger.error("JWT processing failed: " + e.getMessage());
        }

        filterChain.doFilter(request,response);
    }
}
