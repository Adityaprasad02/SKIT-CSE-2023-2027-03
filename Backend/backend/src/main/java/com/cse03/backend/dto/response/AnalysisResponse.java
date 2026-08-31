package com.cse03.backend.dto.response;

import com.cse03.backend.entity.enums.AnalysisStatus;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Data
@Getter
@Setter
public class AnalysisResponse {
    private Long id;

    private Long resumeId;

    private Double atsScore;

    private Double grammarScore;

    private Double structureScore;

    private AnalysisStatus status;

    private LocalDateTime createdAt;
}
