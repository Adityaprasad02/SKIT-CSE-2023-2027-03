package com.cse03.backend.service.impl;


import com.cse03.backend.dto.request.ResumeRequest;
import com.cse03.backend.dto.response.ResumeResponse;
import com.cse03.backend.entity.Resume;
import com.cse03.backend.entity.User;
import com.cse03.backend.entity.enums.ResumeStatus;
import com.cse03.backend.exception.ResourceNotFoundException;
import com.cse03.backend.mapper.ResumeMapper;
import com.cse03.backend.repository.AnalysisResultRepository;
import com.cse03.backend.repository.ResumeRepository;
import com.cse03.backend.repository.UserRepository;
import com.cse03.backend.service.ResumeService;
import jakarta.transaction.Transactional;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class ResumeServiceImpl implements ResumeService {
    private final ResumeRepository resumeRepository;
    private final AnalysisResultRepository analysisResultRepository;
    private final UserRepository userRepository;

    public ResumeServiceImpl(ResumeRepository resumeRepository,
                             AnalysisResultRepository analysisResultRepository,
                             UserRepository userRepository) {
        this.resumeRepository = resumeRepository;
        this.analysisResultRepository = analysisResultRepository;
        this.userRepository = userRepository;
    }

    @Override
    @Transactional
    public ResumeResponse createResume(ResumeRequest request) {
        User owner = currentUser();
        String title = request.getTitle().trim();
        Resume resume = Resume.builder()
                .candidateName(valueOrDefault(request.getCandidateName(), title))
                .fileName(valueOrDefault(request.getFileName(), title))
                .filePath(normalize(request.getFilePath()))
                .status(ResumeStatus.UPLOADED)
                .uploadedAt(LocalDateTime.now())
                .owner(owner)
                .build();
        return ResumeMapper.toResponse(resumeRepository.save(resume));
    }

    @Override
    @Transactional
    public ResumeResponse getResumeById(Long id) {
        return ResumeMapper.toResponse(findOwnedResume(id));
    }

    @Override
    @Transactional
    public List<ResumeResponse> getAllResumes() {
        User owner = currentUser();
        List<Resume> resumes = owner == null
                ? resumeRepository.findAll()
                : resumeRepository.findByOwnerIdOrderByUploadedAtDesc(owner.getId());
        return resumes.stream().map(ResumeMapper::toResponse).toList();
    }

    @Override
    @Transactional
    public ResumeResponse updateResume(Long id, ResumeRequest request) {
        Resume resume = findOwnedResume(id);
        String title = request.getTitle().trim();
        resume.setFileName(valueOrDefault(request.getFileName(), title));
        resume.setCandidateName(valueOrDefault(request.getCandidateName(), resume.getCandidateName()));
        resume.setFilePath(normalize(request.getFilePath()));
        return ResumeMapper.toResponse(resumeRepository.save(resume));
    }

    @Override
    @Transactional
    public void deleteResume(Long id) {
        Resume resume = findOwnedResume(id);
        analysisResultRepository.deleteByResumeId(resume.getId());
        resumeRepository.delete(resume);
    }

    private Resume findOwnedResume(Long id) {
        Resume resume = resumeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Resume not found with id: " + id));
        User owner = currentUser();
        if (owner != null && resume.getOwner() != null
                && !owner.getId().equals(resume.getOwner().getId())) {
            throw new ResourceNotFoundException("Resume not found with id: " + id);
        }
        return resume;
    }

    private User currentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof User user)) {
            return null;
        }
        return userRepository.findById(user.getId()).orElse(user);
    }

    private String valueOrDefault(String value, String fallback) {
        return value == null || value.isBlank() ? fallback : value.trim();
    }

    private String normalize(String value) {
        return value == null || value.isBlank() ? null : value.trim();
    }
}
