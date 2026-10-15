package com.cse03.backend.service.impl;

import com.cse03.backend.dto.request.AnalysisRequest;
import com.cse03.backend.dto.response.AnalysisResponse;
import com.cse03.backend.entity.AnalysisResult;
import com.cse03.backend.entity.Resume;
import com.cse03.backend.entity.enums.AnalysisStatus;
import com.cse03.backend.exception.DBException;
import com.cse03.backend.exception.ResourceNotFoundException;
import com.cse03.backend.repository.AnalysisResultRepository;
import com.cse03.backend.repository.ResumeRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import org.springframework.dao.DataIntegrityViolationException;

@ExtendWith(MockitoExtension.class)
class AnalysisServiceImplTest {

    @Mock
    private AnalysisResultRepository analysisResultRepository;

    @Mock
    private ResumeRepository resumeRepository;

    @InjectMocks
    private AnalysisServiceImpl analysisService;

    @Test
    void shouldCreateAnalysisForExistingResume() {
        Long resumeId = 7L;
        Resume resume = Resume.builder().id(resumeId).build();
        AnalysisRequest request = new AnalysisRequest();
        request.setAnalysisType("ATS");

        when(resumeRepository.findById(resumeId)).thenReturn(Optional.of(resume));
        when(analysisResultRepository.save(any(AnalysisResult.class)))
                .thenAnswer(invocation -> {
                    AnalysisResult analysis = invocation.getArgument(0);
                    analysis.setId(11L);
                    return analysis;
                });

        AnalysisResponse response = analysisService.createAnalysis(resumeId, request);

        ArgumentCaptor<AnalysisResult> analysisCaptor =
                ArgumentCaptor.forClass(AnalysisResult.class);
        verify(analysisResultRepository).save(analysisCaptor.capture());
        AnalysisResult persisted = analysisCaptor.getValue();

        assertThat(persisted.getResume()).isSameAs(resume);
        assertThat(persisted.getStatus()).isEqualTo(AnalysisStatus.PENDING);
        assertThat(response.getId()).isEqualTo(11L);
        assertThat(response.getResumeId()).isEqualTo(resumeId);
    }

    @Test
    void shouldRejectAnalysisWhenResumeDoesNotExist() {
        Long resumeId = 404L;
        AnalysisRequest request = new AnalysisRequest();
        request.setAnalysisType("ATS");

        when(resumeRepository.findById(resumeId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> analysisService.createAnalysis(resumeId, request))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessage("Resume not found with id: " + resumeId);

        verify(analysisResultRepository, never()).save(any(AnalysisResult.class));
    }

    @Test
    void shouldExposePersistenceFailureWhenAnalysisCannotBeSaved() {
        Long resumeId = 7L;
        Resume resume = Resume.builder().id(resumeId).build();
        AnalysisRequest request = new AnalysisRequest();
        request.setAnalysisType("ATS");

        when(resumeRepository.findById(resumeId)).thenReturn(Optional.of(resume));
        when(analysisResultRepository.save(any(AnalysisResult.class)))
                .thenThrow(new DataIntegrityViolationException("database unavailable"));

        assertThatThrownBy(() -> analysisService.createAnalysis(resumeId, request))
                .isInstanceOf(DBException.class)
                .hasMessage("Unable to create analysis for resume: " + resumeId);
    }
}
