# GeneralizIT: Generalizability Theory Analysis in Python

## Overview

GeneralizIT is a Python-based library designed for conducting Generalizability Theory (GT) analyses. The library supports multiple research designs and provides tools to calculate ANOVA tables, generalizability coefficients (G coefficients), and decision (D) studies.

It is particularly useful for researchers and practitioners who work with multi-faceted designs and want to quantify the reliability and generalizability of their measurements.

## Features

- **Support for Various Designs:** Handles different research designs (e.g., crossed, nested).
- **Automated Data Cleaning:** Prepares your data by dropping unnecessary columns and normalizing names.
- **ANOVA Calculation:** Produces ANOVA tables specific to your design.
- **G Coefficients:** Computes generalizability coefficients to assess reliability.
- **D Studies:** Performs decision studies with customizable levels for facets.
- **Summaries:** Provides concise summaries for ANOVA, G coefficients, and D studies.

## Installation

To use this library, the following dependencies are installed alongside the package:

- `pandas`
- `numpy`
- `re`
- `scipy`
- `itertools`
- `typing`
- `unittest`
- `itertools`

## Usage

### Initializing GeneralizIT

```python
from generalizit import GeneralizIT

# Initialize with:
# - `data`: A pandas DataFrame containing your data.
# - `input_str`: A string describing the research design (e.g., "Person x i x o").
# - `response`: The column name for the response variable.
GT = GeneralizIT(data=formatted_df, input_str='Person x i x o', response='Response')
```

### Example Workflow

1. **Calculate ANOVA**
   ```python
   GT.calculate_anova()
   ```
2. **Compute G Coefficients**
   ```python
   GT.g_coeffs()
   ```
3. **Perform a D Study**
   ```python
   GT.calculate_d_study(levels={'Person': None, 'i': [4, 8], 'o': [1, 2]})
   ```
4. **View Summaries**
   - ANOVA Summary:
     ```python
     GT.anova_summary()
     ```
   - G Coefficients Summary:
     ```python
     GT.g_coeff_summary()
     ```
   - D Study Summary:
     ```python
     GT.d_study_summary()
     ```

### Input Data Format

The input data must be a pandas DataFrame where each column represents a facet, and one column is the response variable.

For example:
| Person | i | o | Response |
|--------|---|---|----------|
| 1 | 1 | 1 | 5 |
| 1 | 2 | 1 | 7 |
| ... | | | |

### Example Datasets

#### Synthetic Data from Brennan (2001)

The package includes examples of synthetic data used to demonstrate the functionality of the library. You can adapt these examples to your own datasets.

## Research Design Syntax

The `input_str` parameter specifies the research design. Supported formats include:

- **Crossed Designs:** `"Person x i x o"`
- **Nested Designs:** `"Person x (r:t)"`

## Output

- **ANOVA Table:** Provides variance component estimates for each facet.
- **G Coefficients:** Estimates the reliability of measurements across facets.
- **D Studies:** Offers predictions of generalizability for specified facet levels.

## Notes

- Ensure your data is preprocessed to include only the necessary facets and the response variable.
- Column names should match those specified in the research design.
- Use the `_clean_data` method to automate column renaming and pruning.

## License

This library is licensed under the MIT License.

## Contributions

Contributions to improve functionality or expand supported designs are welcome! Please fork the repository and create a pull request.

## Contact

For questions or support, raise an issue in the github repo!

---

Happy analyzing with **GeneralizIT**!
