# Implementation Plan: Enhanced Year Organization

## Overview

This plan implements the cascading year extraction feature (filename → metadata → PDF content) for the organize_by_year functionality. Tasks are ordered to build incrementally, with each step building on the previous.

## Tasks

- [x] 1. Add YearExtractionResult data class
  - Add new dataclass to `logic.py` after existing dataclasses
  - Fields: `year: Optional[int]`, `method: str`, `reason: str`
  - _Requirements: 4.4_

- [x] 2. Implement metadata year extraction
  - [x] 2.1 Create `extract_year_from_metadata` function
    - Extract ModDate/CreationDate from PDF metadata using PyPDF2
    - Parse PDF date format `D:YYYYMMDDHHmmSS`
    - Prefer modification date over creation date
    - Validate against min_year/max_year bounds
    - Return `(year, reason)` tuple
    - _Requirements: 2.1, 2.2, 2.3_
  - [x] 2.2 Write property test for metadata preference

    - **Property 5: Metadata Preference**
    - **Validates: Requirements 2.2**
  - [x] 2.3 Write unit tests for metadata extraction

    - Test PDF date parsing
    - Test preference of ModDate over CreationDate
    - Test boundary validation
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 3. Implement PDF content year extraction
  - [x] 3.1 Create `extract_year_from_pdf_content` function
    - Extract text from first page using existing `_pdf_page_text_or_ocr` helper
    - Reuse existing date patterns from `PATTERNS` list
    - Apply year_policy for multiple dates
    - Add 5-second timeout using signal or threading
    - Handle OCR unavailability gracefully
    - _Requirements: 3.1, 3.2, 3.3, 6.1, 6.2_
  - [x]* 3.2 Write property test for year policy consistency
    - **Property 2: Year Policy Consistency**
    - **Validates: Requirements 1.2, 3.3**
  - [x]* 3.3 Write unit tests for content extraction
    - Test text extraction path
    - Test OCR fallback
    - Test timeout behavior
    - _Requirements: 3.1, 3.2, 6.1_

- [x] 4. Checkpoint - Ensure extraction functions work
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement cascading extraction orchestrator
  - [x] 5.1 Create `extract_year_cascading` function
    - Call `extract_year_from_name` first (existing)
    - If no year, call `extract_year_from_metadata`
    - If no year and file is PDF, call `extract_year_from_pdf_content`
    - Return `YearExtractionResult` with method used
    - _Requirements: 4.1, 4.2, 5.1, 5.2_
  - [ ] 5.2 Write property test for fallback chain order

    - **Property 4: Fallback Chain Order**
    - **Validates: Requirements 4.1, 4.2**
  - [x]* 5.3 Write property test for non-PDF content scanning skip
    - **Property 6: Non-PDF Content Scanning Skip**
    - **Validates: Requirements 5.1, 5.2, 5.3**

- [x] 6. Update organize_by_year to use cascading extraction
  - [x] 6.1 Modify `organize_by_year` function
    - Replace `extract_year_from_name` call with `extract_year_cascading`
    - Pass file data (bytes) to cascading extractor
    - Log extraction method used for each file
    - _Requirements: 4.1, 4.4_
  - [x]* 6.2 Write property test for unknown folder fallback
    - **Property 8: Unknown Folder Fallback**
    - **Validates: Requirements 4.3**
  - [x]* 6.3 Write property test for processing resilience
    - **Property 7: Processing Resilience**
    - **Validates: Requirements 6.3**

- [x] 7. Checkpoint - Ensure integration works
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Add boundary enforcement tests
  - [x]* 8.1 Write property test for boundary enforcement
    - **Property 3: Boundary Enforcement**
    - **Validates: Requirements 1.3, 2.3, 3.4**
  - [x]* 8.2 Write property test for filename year detection
    - **Property 1: Filename Year Detection Accuracy**
    - **Validates: Requirements 1.1**

- [x] 9. Final checkpoint - All tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Existing helper functions (`_pdf_page_text_or_ocr`, `PATTERNS`) will be reused
- The `hypothesis` library is used for property-based testing
