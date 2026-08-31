package com.cse03.backend.service.impl;

import com.cse03.backend.dto.request.AnalysisRequest;
import com.cse03.backend.dto.response.AnalysisResponse;
import com.cse03.backend.entity.AnalysisResult;
import com.cse03.backend.entity.Resume;
import com.cse03.backend.exception.ResourceNotFoundException;
import com.cse03.backend.repository.AnalysisResultRepository;
import com.cse03.backend.repository.ResumeRepository;
import com.cse03.backend.service.AnalysisService;
import lombok.Builder;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
@Builder
public class AnalysisServiceImpl implements AnalysisService {

    private final AnalysisResultRepository analysisResultRepository;
    private final ResumeRepository resumeRepository;

    @Override
    public AnalysisResponse createAnalysis(
            Long resumeId,
            AnalysisRequest request) {

        Resume resume = resumeRepository.findById(resumeId)
                .orElseThrow(
                );

        AnalysisResult analysis = AnalysisResult.builder()
                .resume(resume)
                .status(AnalysisStatus.PENDING)
                .createdAt(LocalDateTime.now())
                .build();

        AnalysisResult saved =
                analysisResultRepository.save(analysis);

        return toResponse(saved);
    }

    @Override
    public AnalysisResponse getAnalysisById(Long id) {

        AnalysisResult analysis =
                analysisResultRepository.findById(id)
                        .orElseThrow(
                        );

        return toResponse(analysis);
    }

    @Override
    public List<AnalysisResponse> getAnalysesByResume(
            Long resumeId) {

        if (!resumeRepository.existsById(resumeId)) {
            throw new ResourceNotFoundException(
                    "Resume not found with id: " + resumeId
            );
        }

        return analysisResultRepository
                .findByResumeId(resumeId)
                .stream()
                .map(this::toResponse)
                .toList();
    }

    private AnalysisResponse toResponse(
            AnalysisResult analysis) {

        return AnalysisResponse.builder()
                .id(analysis.getId())
                .resumeId(analysis.getResume().getId())
                .atsScore(analysis.getAtsScore())
                .grammarScore(analysis.getGrammarScore())
                .structureScore(analysis.getStructureScore())
                .status(analysis.getStatus())
                .createdAt(analysis.getCreatedAt())
                .build();
    }
}
