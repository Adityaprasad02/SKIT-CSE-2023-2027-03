package com.cse03.backend.dto.response;

import com.cse03.backend.entity.enums.ResumeStatus;
import lombok.Builder;
import lombok.Value;

import java.time.LocalDateTime;

@Value
@Builder
public class ResumeResponse {
    Long id;
    String title;
    String candidateName;
    String fileName;
    String filePath;
    ResumeStatus status;
    LocalDateTime uploadedAt;
}
