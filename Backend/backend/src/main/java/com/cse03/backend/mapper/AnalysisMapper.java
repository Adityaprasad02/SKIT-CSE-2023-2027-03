package com.cse03.backend.mapper;

import com.cse03.backend.dto.response.AnalysisResponse;
import com.cse03.backend.entity.AnalysisResult;

public class AnalysisMapper {

    private AnalysisMapper() {
    }

    public static AnalysisResponse toResponse(AnalysisResult analysis) {
        return AnalysisResponse.builder()
                .id(analysis.getId())
                .resumeId(analysis.getResume().getId())
                .analysisType(analysis.getAnalysisType())
                .atsScore(analysis.getAtsScore())
                .grammarScore(analysis.getGrammarScore())
                .structureScore(analysis.getStructureScore())
                .status(analysis.getStatus())
                .createdAt(analysis.getCreatedAt())
                .build();
    }
}
