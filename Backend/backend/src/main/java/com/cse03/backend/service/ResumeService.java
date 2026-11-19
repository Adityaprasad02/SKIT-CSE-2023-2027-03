package com.cse03.backend.service;

import com.cse03.backend.dto.request.ResumeRequest;
import com.cse03.backend.dto.response.ResumeResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface ResumeService {

    ResumeResponse createResume(ResumeRequest request);

    ResumeResponse getResumeById(Long id);

    Page<ResumeResponse> getAllResumes(Pageable pageable);

    ResumeResponse updateResume(Long id, ResumeRequest request);

    void deleteResume(Long id);
}
