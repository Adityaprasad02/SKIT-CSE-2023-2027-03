package com.cse03.backend.service;

import com.cse03.backend.dto.request.AnalysisRequest;
import com.cse03.backend.dto.response.AnalysisResponse;

import java.util.List;

public interface AnalysisService {

    AnalysisResponse createAnalysis(
            Long resumeId,
            AnalysisRequest request
    );

    AnalysisResponse getAnalysisById(Long id);

    List<AnalysisResponse> getAnalysesByResume(Long resumeId);
}