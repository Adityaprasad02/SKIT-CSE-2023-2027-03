package com.cse03.backend.repository;

import com.cse03.backend.entity.Resume;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface ResumeRepository
        extends JpaRepository<Resume, Long> {

    List<Resume> findByOwnerIdOrderByUploadedAtDesc(UUID ownerId);
}
