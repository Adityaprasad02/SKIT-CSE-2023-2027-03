package com.cse03.backend.entity;

import com.cse03.backend.entity.enums.ResumeStatus;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "resumes")
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Resume {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String candidateName;

    @Column(nullable = false)
    private String fileName;

    private String filePath;

    @Enumerated(EnumType.STRING)
    private ResumeStatus status;

    private LocalDateTime uploadedAt;
}
