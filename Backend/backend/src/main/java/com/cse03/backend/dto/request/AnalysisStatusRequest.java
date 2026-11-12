package com.cse03.backend.dto.request;

import com.cse03.backend.entity.enums.AnalysisStatus;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class AnalysisStatusRequest {

    @NotNull(message = "Analysis status is required")
    private AnalysisStatus status;
}
