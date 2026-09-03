package com.cse03.backend.controller;

import com.cse03.backend.dto.request.ResumeRequest;
import com.cse03.backend.dto.response.ResumeResponse;
import com.cse03.backend.service.ResumeService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/resumes")
@RequiredArgsConstructor
public class ResumeController {

    private final ResumeService resumeService;

    @PostMapping
    public ResponseEntity<ResumeResponse> createResume(
            @Valid @RequestBody ResumeRequest request
    ) {
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(resumeService.createResume(request));
    }

    @GetMapping
    public ResponseEntity<List<ResumeResponse>> getAll() {
        return ResponseEntity.ok(resumeService.getAllResumes());
    }

    @GetMapping("/{id}")
    public ResponseEntity<ResumeResponse> getById(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(
                resumeService.getResumeById(id)
        );
    }
}