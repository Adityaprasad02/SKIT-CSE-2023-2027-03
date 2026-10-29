package com.cse03.backend.service.impl;

import com.cse03.backend.dto.request.AnalysisRequest;
import com.cse03.backend.dto.response.AnalysisResponse;
import com.cse03.backend.entity.AnalysisResult;
import com.cse03.backend.entity.Resume;
import com.cse03.backend.entity.enums.AnalysisStatus;
import com.cse03.backend.exception.DBException;
import com.cse03.backend.exception.ResourceNotFoundException;
import com.cse03.backend.repository.AnalysisResultRepository;
import com.cse03.backend.repository.ResumeRepository;
import com.cse03.backend.service.AnalysisService;
import lombok.Builder;
import lombok.RequiredArgsConstructor;
import org.springframework.dao.DataAccessException;
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
                .orElseThrow( () -> new ResourceNotFoundException(
                        "Resume not found with id: " + resumeId
                ) ) ;

        AnalysisResult analysis = AnalysisResult.builder()
                .resume(resume)
                .analysisType(request.getAnalysisType())
                .status(AnalysisStatus.PENDING)
                .createdAt(LocalDateTime.now())
                .build();

        AnalysisResult saved;
        try {
            saved = analysisResultRepository.save(analysis);
        } catch (DataAccessException exception) {
            throw new DBException("Unable to create analysis for resume: " + resumeId);
        }

        return toResponse(saved);
    }

    @Override
    public AnalysisResponse getAnalysisById(Long id) {

        AnalysisResult analysis =
                analysisResultRepository.findById(id)
                        .orElseThrow(
                                () -> new ResourceNotFoundException(
                                        "Analysis not found with id: " + id
                                )
                        );

        return toResponse(analysis);
    }

    @Override
    public List<AnalysisResponse> getAnalysesByResume(
            Long resumeId) {

        try {
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
        } catch (DataAccessException exception) {
            throw new DBException("Unable to fetch analyses for resume: " + resumeId);
        }
    }

    private AnalysisResponse toResponse(
            AnalysisResult analysis) {

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
