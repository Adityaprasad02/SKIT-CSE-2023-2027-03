package com.cse03.backend.service.impl;

import com.cse03.backend.dto.request.ResumeRequest;
import com.cse03.backend.dto.response.ResumeResponse;
import com.cse03.backend.entity.Resume;
import com.cse03.backend.entity.User;
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
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

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

    @org.junit.jupiter.api.AfterEach
    void clearAuthentication() {
        SecurityContextHolder.clearContext();
    }

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
        UUID ownerId = UUID.randomUUID();
        User owner = User.builder().id(ownerId).build();
        SecurityContextHolder.getContext().setAuthentication(
                new UsernamePasswordAuthenticationToken(owner, null, owner.getAuthorities()));
        Resume resume = Resume.builder()
                .id(4L)
                .candidateName("Candidate")
                .fileName("resume.pdf")
                .status(ResumeStatus.UPLOADED)
                .build();
        PageRequest pageable = PageRequest.of(1, 2);
        when(resumeRepository.findByOwnerId(ownerId, pageable))
                .thenReturn(new PageImpl<>(List.of(resume), pageable, 3));

        var responses = resumeService.getAllResumes(pageable);

        assertThat(responses.getContent()).singleElement().extracting(ResumeResponse::getId)
                .isEqualTo(4L);
        verify(resumeRepository).findByOwnerId(ownerId, pageable);
    }

    @Test
    void shouldNotQueryResumesWithoutAnAuthenticatedOwner() {
        var responses = resumeService.getAllResumes(PageRequest.of(0, 10));

        assertThat(responses).isEmpty();
        verify(resumeRepository, org.mockito.Mockito.never())
                .findByOwnerId(any(), any());
    }

    @Test
    void shouldRejectResumeOwnedByAnotherUser() {
        User authenticatedOwner = User.builder().id(UUID.randomUUID()).build();
        User actualOwner = User.builder().id(UUID.randomUUID()).build();
        SecurityContextHolder.getContext().setAuthentication(
                new UsernamePasswordAuthenticationToken(authenticatedOwner, null,
                        authenticatedOwner.getAuthorities()));
        when(resumeRepository.findById(4L))
                .thenReturn(Optional.of(Resume.builder().id(4L).owner(actualOwner).build()));

        assertThatThrownBy(() -> resumeService.getResumeById(4L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessage("Resume not found with id: 4");
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
