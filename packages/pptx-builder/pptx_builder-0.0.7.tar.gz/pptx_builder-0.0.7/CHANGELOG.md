# Changelog

## [0.0.7] - 2024-11-26

### Added

- **Custom Positioning for Title and Body**:
    - Introduced `title_position` and `body_position` dictionaries in the slide content definitions to allow specifying
      exact positions (`left_cm`, `top_cm`, `width_cm`, `height_cm`) for the title and body text boxes.
    - Enabled adding new text boxes with custom positions when `title_position` or `body_position` is provided.

- **Enhanced Font Customization**:
    - Extended font properties to include `color` alongside `name`, `size`, and `bold` for titles, bodies, headers, and
      table cells.
    - Allowed specifying `alignment` (e.g., `PP_ALIGN.LEFT`, `PP_ALIGN.CENTER`) for both title and body texts.

- **Improved Placeholder Handling**:
    - Implemented `_get_placeholder_by_type` function to retrieve placeholders based on their specific
      types (`PP_PLACEHOLDER_TITLE`, `PP_PLACEHOLDER_BODY`) rather than relying solely on index positions.
    - Prioritized using existing Title and Body placeholders if available, maintaining design consistency with slide
      layouts.

- **Image Grid Enhancements**:
    - Added type checking and validation within the `_add_image_grid` method to ensure that all positional and sizing
      values are numeric.
    - Improved error handling to gracefully skip invalid image configurations and continue processing remaining images.

- **Debugging and Logging**:
    - Included informative `print` statements throughout the slide creation process to trace actions like adding titles,
      bodies, columns, image grids, and tables.
    - Enhanced error messages to provide clearer insights into issues encountered during presentation generation.

### Changed

- **Utility Functions**:
    - Updated `_set_text_properties` to include an optional `alignment` parameter, allowing for better control over text
      alignment within text frames.
    - Modified `_add_table` to center-align text in table headers and cells for improved readability.

- **Error Handling**:
    - Enhanced error handling in image addition to catch and report issues without halting the entire presentation
      generation process.
    - Ensured that all unit conversions (from millimeters to centimeters) are correctly handled to prevent attribute
      errors.

### Fixed

### Deprecated

## [0.0.6] - 2024-04-20

### Added

- **Initial Release**:
    - Developed the `CustomPresentationBuilder` class to generate PowerPoint presentations with customizable slides.
    - Implemented basic functionalities to add slides with titles and body texts using predefined layouts.
    - Created utility functions:
        - `_set_text_properties`: Sets text and font properties for text frames.
        - `_get_placeholder_by_idx`: Retrieves placeholders by index from slides.
        - `_add_table`: Adds tables to slides based on pandas DataFrames.

- **Slide Layout Customization**:
    - Enabled setting slide dimensions to a 16:9 aspect ratio using centimeters for consistent sizing.
    - Allowed specifying different slide layouts (e.g., `TITLE_AND_CONTENT`, `TITLE_ONLY`, `BLANK`) based on the slide
      content definitions.

- **Font Defaults**:
    - Established default font settings for titles, bodies, headers, and table cells to ensure consistency across
      slides.

### Fixed

- **Basic Slide Content Addition**:
    - Ensured that titles and body texts are correctly added to slides using the appropriate placeholders or by creating
      new text boxes when placeholders are absent.

### Known Issues

- **Limited Error Handling**:
    - Initial version has basic error handling. More robust mechanisms are planned for future releases to handle diverse
      edge cases.

---

# Versioning

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- **Major** version when you make incompatible API changes,
- **Minor** version when you add functionality in a backwards compatible manner, and
- **Patch** version when you make backwards compatible bug fixes.

---



