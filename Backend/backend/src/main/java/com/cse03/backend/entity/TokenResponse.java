package com.cse03.backend.entity;

public record TokenResponse(
        String accessToken ,
        String refreshToken ,
        Long expiresIn ,
        ResponseUserRegistration userRegistration
) {
}
