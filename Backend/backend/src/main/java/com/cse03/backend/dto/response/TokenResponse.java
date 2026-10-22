package com.cse03.backend.dto.response;

public record TokenResponse(
        String accessToken ,
        String refreshToken ,
        Long expiresIn ,
        ResponseUserRegistration userRegistration
) {
}
