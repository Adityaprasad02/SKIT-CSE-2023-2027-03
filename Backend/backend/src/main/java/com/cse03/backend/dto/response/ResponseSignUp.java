package com.cse03.backend.dto.response;

import com.cse03.backend.entity.enums.LoginAuthProvider;

import java.util.UUID;

public record ResponseSignUp(
        UUID id ,
        String name ,
        String username ,
        String email ,
        LoginAuthProvider loginAuthProvider
) {}
