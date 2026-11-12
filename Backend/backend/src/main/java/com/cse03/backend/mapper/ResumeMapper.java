package com.cse03.backend.mapper;

import com.cse03.backend.dto.response.ResumeResponse;
import com.cse03.backend.entity.Resume;

public class ResumeMapper {
    private ResumeMapper() {
    }

    public static ResumeResponse toResponse(Resume resume) {
        return ResumeResponse.builder()
                .id(resume.getId())
                .title(resume.getFileName())
                .candidateName(resume.getCandidateName())
                .fileName(resume.getFileName())
                .filePath(resume.getFilePath())
                .status(resume.getStatus())
                .uploadedAt(resume.getUploadedAt())
                .build();
    }
}
