package com.cse03.backend.controller;

import com.cse03.backend.dto.request.ResumeRequest;
import com.cse03.backend.dto.response.ResumeResponse;
import com.cse03.backend.service.ResumeService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Pattern;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.validation.annotation.Validated;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/resumes")
@Validated
public class ResumeController {

	private final ResumeService resumeService;

	public ResumeController(ResumeService resumeService) {
		this.resumeService = resumeService;
	}

	@PostMapping
	public ResponseEntity<ResumeResponse> createResume(@Valid @RequestBody ResumeRequest request) {
		return ResponseEntity.status(HttpStatus.CREATED).body(resumeService.createResume(request));
	}

	@GetMapping
	public ResponseEntity<Page<ResumeResponse>> getAll(
			@RequestParam(defaultValue = "0") @Min(value = 0, message = "page must be non-negative") int page,
			@RequestParam(defaultValue = "10") @Min(value = 1, message = "size must be at least 1")
			@Max(value = 100, message = "size must not exceed 100") int size,
			@RequestParam(defaultValue = "uploadedAt,desc")
			@Pattern(regexp = "(id|uploadedAt|fileName|candidateName|status)(,(?i:asc|desc))?",
					message = "sort must use an allowed field and optional direction") String sort) {
		return ResponseEntity.ok(resumeService.getAllResumes(toPageable(page, size, sort)));
	}

	private Pageable toPageable(int page, int size, String sort) {
		if (page < 0) {
			throw new IllegalArgumentException("page must be non-negative");
		}
		if (size < 1 || size > 100) {
			throw new IllegalArgumentException("size must be between 1 and 100");
		}
		if (!sort.matches("(id|uploadedAt|fileName|candidateName|status)(,(?i:asc|desc))?")) {
			throw new IllegalArgumentException("sort must use an allowed field and optional direction");
		}
		String[] parts = sort.split(",", -1);
		String property = parts[0];
		Sort.Direction direction = parts.length == 2
				? Sort.Direction.fromString(parts[1])
				: Sort.Direction.ASC;
		return PageRequest.of(page, size, Sort.by(direction, property));
	}

	@GetMapping("/{id}")
	public ResponseEntity<ResumeResponse> getById(@PathVariable Long id) {
		return ResponseEntity.ok(resumeService.getResumeById(id));
	}

	@PutMapping("/{id}")
	public ResponseEntity<ResumeResponse> update(@PathVariable Long id,
			@Valid @RequestBody ResumeRequest request) {
		return ResponseEntity.ok(resumeService.updateResume(id, request));
	}

	@DeleteMapping("/{id}")
	public ResponseEntity<Void> delete(@PathVariable Long id) {
		resumeService.deleteResume(id);
		return ResponseEntity.noContent().build();
	}
}
