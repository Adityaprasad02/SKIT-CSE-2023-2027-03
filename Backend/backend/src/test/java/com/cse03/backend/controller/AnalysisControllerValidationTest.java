package com.cse03.backend.controller;

import com.cse03.backend.exception.GlobalExceptionHandler;
import com.cse03.backend.service.AnalysisService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.springframework.http.MediaType.APPLICATION_JSON;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.mockito.Mockito.mock;

class AnalysisControllerValidationTest {

    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        AnalysisService analysisService = mock(AnalysisService.class);
        mockMvc = MockMvcBuilders.standaloneSetup(new AnalysisController(analysisService))
                .setControllerAdvice(new GlobalExceptionHandler())
                .build();
    }

    @Test
    void shouldRejectBlankAnalysisType() throws Exception {
        mockMvc.perform(post("/api/v1/resumes/7/analyses")
                        .contentType(APPLICATION_JSON)
                        .content("{\"analysisType\":\"   \"}"))
                .andExpect(status().isBadRequest());
    }
}
