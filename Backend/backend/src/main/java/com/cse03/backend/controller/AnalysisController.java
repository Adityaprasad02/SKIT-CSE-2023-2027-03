package com.cse03.backend.controller;


import com.cse03.backend.dto.request.AnalysisRequest;
import com.cse03.backend.dto.response.AnalysisResponse;
import com.cse03.backend.service.AnalysisService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
public class AnalysisController {

    private final AnalysisService analysisService;

    @PostMapping("/resumes/{resumeId}/analyses")
    public ResponseEntity<AnalysisResponse> createAnalysis(
            @PathVariable Long resumeId,
            @Valid @RequestBody AnalysisRequest request) {

        AnalysisResponse response =
                analysisService.createAnalysis(resumeId, request);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(response);
    }

    @GetMapping("/analyses/{id}")
    public ResponseEntity<AnalysisResponse> getAnalysisById(
            @PathVariable Long id) {

        return ResponseEntity.ok(
                analysisService.getAnalysisById(id)
        );
    }

    @GetMapping("/resumes/{resumeId}/analyses")
    public ResponseEntity<List<AnalysisResponse>> getAnalysesByResume(
            @PathVariable Long resumeId) {

        return ResponseEntity.ok(
                analysisService.getAnalysesByResume(resumeId)
        );
    }
}
