package com.cse03.backend.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class ResumeRequest {

    @NotBlank(message = "Resume title is required")
    @Size(max = 255, message = "Resume title must not exceed 255 characters")
    private String title;

    @Size(max = 255, message = "Candidate name must not exceed 255 characters")
    private String candidateName;

    @Size(max = 255, message = "File name must not exceed 255 characters")
    private String fileName;

    @Size(max = 1000, message = "File path must not exceed 1000 characters")
    private String filePath;
}
