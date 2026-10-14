package com.cse03.backend.dto.request;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AnalysisRequestValidationTest {

    private static Validator validator;

    @BeforeAll
    static void setUp() {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    @Test
    void shouldFailValidationWhenAnalysisTypeIsBlank() {
        AnalysisRequest request = new AnalysisRequest();
        request.setAnalysisType("   ");

        Set<ConstraintViolation<AnalysisRequest>> violations = validator.validate(request);

        assertFalse(violations.isEmpty());
    }

    @Test
    void shouldPassValidationWhenAnalysisTypeIsProvided() {
        AnalysisRequest request = new AnalysisRequest();
        request.setAnalysisType("ATS");

        Set<ConstraintViolation<AnalysisRequest>> violations = validator.validate(request);

        assertTrue(violations.isEmpty());
    }
}
