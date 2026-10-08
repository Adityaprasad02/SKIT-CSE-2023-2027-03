package com.cse03.backend.dto.request;

import com.cse03.backend.entity.enums.LoginAuthProvider;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record RequestSignUp (

        @NotNull
        @NotBlank(message = "name is required")
        String name,

        @NotNull
        @NotBlank(message = "username is required")
        String username ,

        @NotNull
        @NotBlank(message = "email is required")
        String email ,

        String password,

        @NotNull
        LoginAuthProvider loginAuthProvider
){}
