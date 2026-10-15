package com.cse03.backend.controller;

import com.cse03.backend.exception.GlobalExceptionHandler;
import com.cse03.backend.service.ResumeService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.Mockito.mock;
import static org.springframework.http.MediaType.APPLICATION_JSON;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
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
}
