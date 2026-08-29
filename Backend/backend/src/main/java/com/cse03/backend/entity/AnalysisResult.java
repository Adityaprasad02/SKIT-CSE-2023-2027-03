package com.cse03.backend.entity;

import jakarta.persistence.GeneratedValue;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "analysis_results")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AnalysisResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Double atsScore;

    private Double grammarScore;

    private Double structureScore;

    @Enumerated(EnumType.STRING)
    private AnalysisStatus status;

    private LocalDateTime createdAt;

    @ManyToOne
    @JoinColumn(name = "resume_id", nullable = false)
    private Resume resume;
}