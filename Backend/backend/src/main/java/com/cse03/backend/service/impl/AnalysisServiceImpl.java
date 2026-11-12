package com.cse03.backend.service.impl;

import com.cse03.backend.dto.request.AnalysisRequest;
import com.cse03.backend.dto.response.AnalysisResponse;
import com.cse03.backend.entity.AnalysisResult;
import com.cse03.backend.entity.Resume;
import com.cse03.backend.entity.User;
import com.cse03.backend.entity.enums.AnalysisStatus;
import com.cse03.backend.exception.DBException;
import com.cse03.backend.exception.InvalidStateException;
import com.cse03.backend.exception.ResourceNotFoundException;
import com.cse03.backend.mapper.AnalysisMapper;
import com.cse03.backend.repository.AnalysisResultRepository;
import com.cse03.backend.repository.ResumeRepository;
import com.cse03.backend.service.AnalysisService;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.dao.DataAccessException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class AnalysisServiceImpl implements AnalysisService {

    private final AnalysisResultRepository analysisResultRepository;
    private final ResumeRepository resumeRepository;

    @Override
    @Transactional
    public AnalysisResponse createAnalysis(Long resumeId, AnalysisRequest request) {
        Resume resume = findResume(resumeId);
        validateOwnership(resume);

        AnalysisResult analysis = AnalysisResult.builder()
                .resume(resume)
                .analysisType(request.getAnalysisType().trim())
                .status(AnalysisStatus.PENDING)
                .createdAt(LocalDateTime.now())
                .build();

        try {
            return AnalysisMapper.toResponse(analysisResultRepository.save(analysis));
        } catch (DataAccessException exception) {
            throw new DBException("Unable to create analysis for resume: " + resumeId);
        }
    }

    @Override
    @Transactional
    public AnalysisResponse getAnalysisById(Long id) {
        try {
            AnalysisResult analysis = analysisResultRepository.findById(id)
                    .orElseThrow(() -> new ResourceNotFoundException(
                            "Analysis not found with id: " + id));
            validateOwnership(analysis.getResume());
            return AnalysisMapper.toResponse(analysis);
        } catch (DataAccessException exception) {
            throw new DBException("Unable to fetch analysis with id: " + id);
        }
    }

    @Override
    @Transactional
    public List<AnalysisResponse> getAnalysesByResume(Long resumeId) {
        Resume resume = findResume(resumeId);
        validateOwnership(resume);
        try {
            return analysisResultRepository.findByResumeId(resumeId)
                    .stream()
                    .map(AnalysisMapper::toResponse)
                    .toList();
        } catch (DataAccessException exception) {
            throw new DBException("Unable to fetch analyses for resume: " + resumeId);
        }
    }

    @Override
    @Transactional
    public AnalysisResponse updateStatus(Long id, AnalysisStatus requestedStatus) {
        AnalysisResult analysis = analysisResultRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Analysis not found with id: " + id));
        validateOwnership(analysis.getResume());
        if (!isValidTransition(analysis.getStatus(), requestedStatus)) {
            throw new InvalidStateException("Cannot transition analysis " + id
                    + " from " + analysis.getStatus() + " to " + requestedStatus);
        }
        analysis.setStatus(requestedStatus);
        return AnalysisMapper.toResponse(analysisResultRepository.save(analysis));
    }

    private Resume findResume(Long resumeId) {
        return resumeRepository.findById(resumeId)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Resume not found with id: " + resumeId));
    }

    private void validateOwnership(Resume resume) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof User currentUser)
                || resume.getOwner() == null) {
            return;
        }
        if (!currentUser.getId().equals(resume.getOwner().getId())) {
            throw new ResourceNotFoundException("Resume not found with id: " + resume.getId());
        }
    }

    private boolean isValidTransition(AnalysisStatus current, AnalysisStatus requested) {
        return current == requested
                || current == AnalysisStatus.PENDING
                && (requested == AnalysisStatus.PROCESSING || requested == AnalysisStatus.FAILED)
                || current == AnalysisStatus.PROCESSING
                && (requested == AnalysisStatus.COMPLETED || requested == AnalysisStatus.FAILED)
                || current == AnalysisStatus.FAILED && requested == AnalysisStatus.PROCESSING;
    }
}
