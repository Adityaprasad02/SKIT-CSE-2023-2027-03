package com.cse03.backend.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;


@Data
@Getter
@Setter
public class AnalysisRequest {
    @NotNull(message = "Analysis type is required")
    private String analysisType;
}
