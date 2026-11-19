package com.cse03.backend.controller;

import com.cse03.backend.exception.GlobalExceptionHandler;
import com.cse03.backend.service.ResumeService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.http.MediaType.APPLICATION_JSON;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class ResumeControllerValidationTest {

    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        ResumeService resumeService = mock(ResumeService.class);
        mockMvc = MockMvcBuilders.standaloneSetup(new ResumeController(resumeService))
                .setControllerAdvice(new GlobalExceptionHandler())
                .build();
    }

    @Test
    void shouldRejectBlankResumeTitle() throws Exception {
        mockMvc.perform(post("/api/v1/resumes")
                        .contentType(APPLICATION_JSON)
                        .content("{\"title\":\"   \"}"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void shouldRejectPageSizeAboveMaximum() throws Exception {
        mockMvc.perform(get("/api/v1/resumes?size=101"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void shouldRejectUnsupportedSortField() throws Exception {
        mockMvc.perform(get("/api/v1/resumes?sort=owner,desc"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void shouldPassPaginationAndSortingToService() throws Exception {
        ResumeService resumeService = mock(ResumeService.class);
        when(resumeService.getAllResumes(PageRequest.of(2, 5,
                Sort.by(Sort.Direction.ASC, "fileName"))))
                .thenReturn(Page.empty(PageRequest.of(2, 5,
                        Sort.by(Sort.Direction.ASC, "fileName"))));
        mockMvc = MockMvcBuilders.standaloneSetup(new ResumeController(resumeService))
                .setControllerAdvice(new GlobalExceptionHandler())
                .build();

        mockMvc.perform(get("/api/v1/resumes?page=2&size=5&sort=fileName,asc"))
                .andExpect(status().isOk());

        verify(resumeService).getAllResumes(PageRequest.of(2, 5,
                Sort.by(Sort.Direction.ASC, "fileName")));
    }
}
