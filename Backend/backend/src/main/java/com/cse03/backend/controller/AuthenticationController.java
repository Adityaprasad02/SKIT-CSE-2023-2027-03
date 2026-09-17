package com.cse03.backend.controller;


import com.cse03.backend.dto.request.RequestSignUp;
import com.cse03.backend.dto.response.ResponseSignUp;
import com.cse03.backend.service.UserService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuthenticationController {


    private final UserService userService ;

    public AuthenticationController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login () {
        return ResponseEntity.ok( HttpStatus.FOUND) ;
    }

    @PostMapping("/signup")
    public ResponseEntity<ResponseSignUp> signup (@Valid @RequestBody RequestSignUp requestSignUp) {

        ResponseSignUp responseSignUp = userService.createUser(requestSignUp); ;

        return  ResponseEntity.ok(responseSignUp) ;
    }


}
