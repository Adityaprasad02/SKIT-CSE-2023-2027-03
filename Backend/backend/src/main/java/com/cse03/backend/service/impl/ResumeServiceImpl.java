package com.cse03.backend.service.impl;


import com.cse03.backend.dto.request.ResumeRequest;
import com.cse03.backend.dto.response.ResumeResponse;
import com.cse03.backend.service.ResumeService;
import lombok.Builder;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
@Builder
public class ResumeServiceImpl implements ResumeService {
    @Override
    public ResumeResponse createResume(ResumeRequest request) {
        return null;
    }

    @Override
    public ResumeResponse getResumeById(Long id) {
        return null;
    }

    @Override
    public List<ResumeResponse> getAllResumes() {
        return List.of();
    }

    @Override
    public ResumeResponse updateResume(Long id, ResumeRequest request) {
        return null;
    }

    @Override
    public void deleteResume(Long id) {

    }
}
