package com.cse03.backend.dto.request;

import jakarta.validation.constraints.NotBlank;

public class ResumeRequest {

    @NotBlank(message = "Resume title is required")
    private String title;
}
