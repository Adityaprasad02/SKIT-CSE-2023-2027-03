package com.cse03.backend.repository;

import com.cse03.backend.entity.AnalysisResult;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AnalysisResultRepository
        extends JpaRepository<AnalysisResult, Long> {

    List<AnalysisResult> findByResumeId(Long resumeId);
}


/*
mapper
├── ResumeMapper.java
└── AnalysisMapper.java
 */