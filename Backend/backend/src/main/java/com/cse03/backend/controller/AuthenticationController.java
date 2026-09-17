package com.cse03.backend.controller;


import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuthenticationController {

    @PostMapping("/login")
    public ResponseEntity<?> login () {
        return ResponseEntity.ok( HttpStatus.FOUND) ;
    }

    @PostMapping("/signup")
    public ResponseEntity<?> signup () {
        return  ResponseEntity.ok(HttpStatus.CREATED) ;
    }


}
