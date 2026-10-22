package com.cse03.backend.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;


@Data
@Getter
@Setter
public class AnalysisRequest {
    @NotBlank(message = "Analysis type is required")
    private String analysisType;
}
