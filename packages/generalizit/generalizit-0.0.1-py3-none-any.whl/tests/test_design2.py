import pytest
import pandas as pd
from GeneralizIT.design2 import Design2

# Create synthetic data for testing
@pytest.fixture
def synthetic_data():
    data = {
        'person': list(range(1, 11)),
        'personi_item1': [2, 4, 5, 5, 4, 4, 2, 3, 0, 6],
        'personi_item2': [6, 5, 5, 9, 3, 4, 6, 4, 5, 8],
        'personi_item3': [7, 6, 4, 8, 5, 4, 6, 4, 4, 7],
        'personi_item4': [5, 7, 6, 6, 6, 7, 5, 5, 5, 6],
        'personi_item5': [2, 6, 5, 5, 4, 6, 2, 6, 5, 6],
        'personi_item6': [5, 7, 4, 7, 5, 4, 7, 6, 5, 8],
        'personi_item7': [5, 5, 5, 7, 6, 7, 7, 6, 5, 8],
        'personi_item8': [5, 7, 5, 6, 4, 8, 5, 4, 3, 6]
    }
    
    # Convert wide data to long format for Design2
    formatted_data = {
        'person': [],
        'item': [],
        'Response': []
    }

    for person in range(1, 11):
        for item in range(1, 9):
            key = f'personi_item{item}'
            formatted_data['person'].append(person)
            formatted_data['item'].append(item)
            formatted_data['Response'].append(data[key][person - 1])
    
    return pd.DataFrame(formatted_data)

@pytest.fixture
def corollary_df():
    return {'p': 'person', 'i': 'item'}

def test_design2_unique_levels(synthetic_data, corollary_df):
    """Test the `get_unique_levels` method of Design2."""
    design = Design2(synthetic_data, corollary_df)
    
    # Check levels for 'person' and 'item'
    assert design.levels['person'] == 10  # 10 unique persons
    assert design.levels['item'] == 8    # 8 unique items per person

def test_design2_anova(synthetic_data, corollary_df):
    """Test the ANOVA calculation of Design2."""
    design = Design2(synthetic_data, corollary_df)
    design.calculate_anova()
    
    # Check that ANOVA table exists
    assert hasattr(design, 'anova_table'), "ANOVA table should be calculated."
    
    # Verify dimensions of the ANOVA table
    assert design.anova_table.shape[0] == 2  # Two sources of variation: 'person' and 'item:person'
    
    # Check column names in ANOVA table
    expected_columns = ['Source of Variation', 'Degrees of Freedom', 'Sum of Squares', 'Mean Square', 'Variance Component']
    assert list(design.anova_table.columns) == expected_columns

def test_design2_g_coeffs(synthetic_data, corollary_df):
    """Test the G coefficient calculation of Design2."""
    design = Design2(synthetic_data, corollary_df)
    design.calculate_anova()  # ANOVA must be calculated first
    
    g_coeff_df = design._calculate_g_coeffs()
    
    # Check the resulting DataFrame
    assert not g_coeff_df.empty, "G coefficient DataFrame should not be empty."
    
    # Verify structure of the DataFrame
    expected_columns = ['Source of Variation', 'Generalized Over Fixed', 'Generalized Over Random', 'rho^2', 'phi^2']
    assert list(g_coeff_df.columns) == expected_columns
