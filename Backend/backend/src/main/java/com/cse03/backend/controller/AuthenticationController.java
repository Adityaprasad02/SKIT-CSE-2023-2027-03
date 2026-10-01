package com.cse03.backend.controller;


import com.cse03.backend.dto.request.RequestSignUp;
import com.cse03.backend.dto.response.ResponseSignUp;
import com.cse03.backend.service.UserService;
import com.cse03.backend.service.impl.UserServiceImpl;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
public class AuthenticationController {


    private final UserServiceImpl userServiceImpl ;

    public AuthenticationController(UserService userService, UserServiceImpl userServiceImpl) {
        this.userServiceImpl = userServiceImpl;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login () {
        return ResponseEntity.ok( HttpStatus.FOUND) ;
    }

    @PostMapping("/signup/")
    public ResponseEntity<ResponseSignUp> signup (@Valid @RequestBody RequestSignUp requestSignUp) {

        ResponseSignUp responseSignUp = null ;

       try {

         responseSignUp = userServiceImpl.createUser(requestSignUp);
       } catch (Exception e ){

           log.error("Error for signup :  " + e.getMessage() );
       }

        return  ResponseEntity.ok(responseSignUp) ;
    }


}
