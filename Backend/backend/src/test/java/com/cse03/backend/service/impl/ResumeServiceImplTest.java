package com.cse03.backend.service.impl;

import com.cse03.backend.dto.request.ResumeRequest;
import com.cse03.backend.dto.response.ResumeResponse;
import com.cse03.backend.entity.Resume;
import com.cse03.backend.entity.enums.ResumeStatus;
import com.cse03.backend.exception.ResourceNotFoundException;
import com.cse03.backend.repository.AnalysisResultRepository;
import com.cse03.backend.repository.ResumeRepository;
import com.cse03.backend.repository.UserRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ResumeServiceImplTest {

    @Mock
    private ResumeRepository resumeRepository;

    @Mock
    private AnalysisResultRepository analysisResultRepository;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private ResumeServiceImpl resumeService;

    @Test
    void shouldCreateResumeFromMetadataRequest() {
        ResumeRequest request = request("Backend resume");
        when(resumeRepository.save(any(Resume.class))).thenAnswer(invocation -> {
            Resume resume = invocation.getArgument(0);
            resume.setId(4L);
            return resume;
        });

        ResumeResponse response = resumeService.createResume(request);

        assertThat(response.getId()).isEqualTo(4L);
        assertThat(response.getTitle()).isEqualTo("Backend resume");
        assertThat(response.getStatus()).isEqualTo(ResumeStatus.UPLOADED);
        verify(resumeRepository).save(any(Resume.class));
    }

    @Test
    void shouldListPersistedResumes() {
        Resume resume = Resume.builder()
                .id(4L)
                .candidateName("Candidate")
                .fileName("resume.pdf")
                .status(ResumeStatus.UPLOADED)
                .build();
        when(resumeRepository.findAll()).thenReturn(List.of(resume));

        List<ResumeResponse> responses = resumeService.getAllResumes();

        assertThat(responses).singleElement().extracting(ResumeResponse::getId)
                .isEqualTo(4L);
    }

    @Test
    void shouldRejectMissingResumeDuringUpdate() {
        when(resumeRepository.findById(404L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> resumeService.updateResume(404L, request("Updated")))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessage("Resume not found with id: 404");
    }

    @Test
    void shouldDeleteDependentAnalysesBeforeResume() {
        Resume resume = Resume.builder().id(4L).build();
        when(resumeRepository.findById(4L)).thenReturn(Optional.of(resume));

        resumeService.deleteResume(4L);

        verify(analysisResultRepository).deleteByResumeId(4L);
        verify(resumeRepository).delete(resume);
    }

    private ResumeRequest request(String title) {
        ResumeRequest request = new ResumeRequest();
        request.setTitle(title);
        return request;
    }
}
