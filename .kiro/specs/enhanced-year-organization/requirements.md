# Requirements Document

## Introduction

Enhancement to the existing "Organize by Year" feature to ensure ALL files are organized into year-based folders, not just those with a year in the filename. The system will use a cascading approach: first checking the filename, then file metadata (creation/modification dates), and finally scanning PDF content for dates.

## Glossary

- **Year_Extractor**: The component responsible for detecting years from various sources (filename, metadata, content)
- **Organize_Service**: The service that orchestrates file organization into year-based folders
- **Fallback_Chain**: The ordered sequence of year detection methods (filename → metadata → content)
- **PDF_Scanner**: Component that extracts text/dates from PDF content using OCR or text extraction

## Requirements

### Requirement 1: Filename Year Detection (Existing)

**User Story:** As a user, I want files with years in their filenames to be organized by that year, so that obviously dated files are sorted correctly.

#### Acceptance Criteria

1. WHEN a file has a year (1900-2099) in its filename, THE Year_Extractor SHALL detect and return that year
2. WHEN multiple years exist in a filename, THE Year_Extractor SHALL use the configured year_policy (first, last, or max)
3. WHEN the detected year falls outside min_year/max_year bounds, THE Year_Extractor SHALL treat it as no year found

### Requirement 2: Metadata Year Detection (New Fallback)

**User Story:** As a user, I want files without years in their filenames to use their file metadata dates, so that more files can be automatically organized.

#### Acceptance Criteria

1. WHEN no year is found in the filename, THE Year_Extractor SHALL attempt to extract year from file metadata
2. WHEN extracting from metadata, THE Year_Extractor SHALL prefer modification date over creation date
3. WHEN the metadata date falls outside min_year/max_year bounds, THE Year_Extractor SHALL proceed to the next fallback method
4. IF metadata is unavailable or corrupted, THEN THE Year_Extractor SHALL proceed to the next fallback method

### Requirement 3: PDF Content Year Detection (Final Fallback)

**User Story:** As a user, I want PDF files to be scanned for dates in their content when other methods fail, so that even poorly named files can be organized.

#### Acceptance Criteria

1. WHEN no year is found from filename or metadata for a PDF file, THE PDF_Scanner SHALL extract text from the first page
2. WHEN text extraction yields no dates, THE PDF_Scanner SHALL attempt OCR on the first page
3. WHEN multiple dates are found in content, THE PDF_Scanner SHALL use the configured year_policy
4. WHEN the content date falls outside min_year/max_year bounds, THE Year_Extractor SHALL place the file in the unknown folder
5. IF PDF content scanning fails or times out, THEN THE Year_Extractor SHALL place the file in the unknown folder

### Requirement 4: Fallback Chain Orchestration

**User Story:** As a user, I want the system to automatically try multiple methods to find a year, so that I don't have to manually organize files.

#### Acceptance Criteria

1. THE Year_Extractor SHALL attempt methods in order: filename → metadata → content
2. WHEN any method succeeds, THE Year_Extractor SHALL stop and use that year
3. WHEN all methods fail, THE Organize_Service SHALL place the file in the configured unknown_folder
4. THE Organize_Service SHALL log which method was used for each file (for debugging/transparency)

### Requirement 5: Non-PDF File Handling

**User Story:** As a user, I want non-PDF files to also be organized using available methods, so that all my files are sorted.

#### Acceptance Criteria

1. WHEN a non-PDF file has no year in filename, THE Year_Extractor SHALL attempt metadata extraction
2. THE Year_Extractor SHALL NOT attempt content scanning for non-PDF files
3. WHEN metadata extraction fails for non-PDF files, THE Organize_Service SHALL place them in the unknown folder

### Requirement 6: Performance and Reliability

**User Story:** As a user, I want the organization process to complete in reasonable time even with many files, so that I can process large batches.

#### Acceptance Criteria

1. WHEN scanning PDF content, THE PDF_Scanner SHALL timeout after 5 seconds per file
2. IF OCR is unavailable, THEN THE PDF_Scanner SHALL skip OCR and proceed with text extraction only
3. THE Organize_Service SHALL continue processing remaining files if one file fails
