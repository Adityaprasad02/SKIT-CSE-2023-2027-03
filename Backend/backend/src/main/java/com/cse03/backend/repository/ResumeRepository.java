package com.cse03.backend.repository;

import com.cse03.backend.entity.Resume;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface ResumeRepository
        extends JpaRepository<Resume, Long> {
}
