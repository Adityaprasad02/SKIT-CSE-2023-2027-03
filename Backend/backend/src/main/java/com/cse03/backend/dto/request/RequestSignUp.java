package com.cse03.backend.dto.request;

import com.cse03.backend.entity.enums.LoginAuthProvider;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record RequestSignUp (

        @NotNull
        @NotBlank
        String name,

        @NotNull
        @NotBlank
        String username ,

        @NotNull
        @NotBlank
        String email ,

        @NotNull
        @NotBlank
        String password,

        @NotNull
        LoginAuthProvider loginAuthProvider
){}
