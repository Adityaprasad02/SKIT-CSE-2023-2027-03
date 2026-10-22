package com.cse03.backend.repository;

import com.cse03.backend.entity.AnalysisResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AnalysisResultRepository
        extends JpaRepository<AnalysisResult, Long> {

    List<AnalysisResult> findByResumeId(Long resumeId);
}


/*
mapper
├── ResumeMapper.java
└── AnalysisMapper.java
 */