package com.cse03.backend.entity;

import com.cse03.backend.entity.enums.LoginAuthProvider;

import java.util.UUID;

public record ResponseUserRegistration (

        UUID userId ,
        String email ,
        String username ,
        LoginAuthProvider authProvider
) { }

