package com.cse03.backend.service;

import com.cse03.backend.dto.request.ResumeRequest;
import com.cse03.backend.dto.response.ResumeResponse;

import java.util.List;

public interface ResumeService {

    ResumeResponse createResume(ResumeRequest request);

    ResumeResponse getResumeById(Long id);

    List<ResumeResponse> getAllResumes();

    ResumeResponse updateResume(Long id, ResumeRequest request);

    void deleteResume(Long id);
}
