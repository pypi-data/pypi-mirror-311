import pandas as pd
import numpy as np
from GeneralizITv3 import GeneralizIT
from generate_data import generate_data, generate_brennan_data




if __name__ == '__main__':
    
    ## ----------------- CARDINET 1976---------------- ##
    # # Define the levels for each factor
    # levels_dict = {
    #     'FactorA': 100,
    #     'FactorB': 3,
    #     'FactorC': 2
    # }
    
    # # Define the expected variance components
    # var_dict = {
    #     'FactorA': 10,
    #     'FactorB': 6,
    #     'FactorC': 5,
    #     'FactorA x FactorB': 3,
    #     'FactorA x FactorC': 5,
    #     'FactorB x FactorC': 4,
    #     'FactorA x FactorB x FactorC': 2
    # }
    
    # for i in range(9043, 10000):
    #     # Define the seed
    #     seed = i

    #     # Generate the synthetic data
    #     data, exp_variance_dict = generate_data(
    #         design='FactorA x FactorB x FactorC',
    #         levels_dict=levels_dict,
    #         exp_variance_dict=var_dict,
    #         seed=seed
    #     )

    #     print(data.head())
    #     print(exp_variance_dict)

    #     GT = GeneralizIT(data, design='FactorA x FactorB x FactorC', response='Response')
    #     GT.calculate_anova()

    #     # Get the variance components
    #     variance_dict = GT.anova_table.set_index('Source of Variation')['Variance Component'].to_dict()
        
    #     # replace '×' with 'x' in the keys
    #     variance_dict = {key.replace('×', 'x'): value for key, value in variance_dict.items()}

    #     # Drop 'Total' from the dictionary
    #     variance_dict.pop('Total')

    #     print(f"Variance Dict: {variance_dict}")

    #     tolerance = .75 # Tolerance for variance components

    #     # Check if the variance components are close to the pre-defined values
    #     if (
    #         np.isclose(variance_dict['FactorA'], var_dict['FactorA'], atol=tolerance) and
    #         np.isclose(variance_dict['FactorB'], var_dict['FactorB'], atol=tolerance) and
    #         np.isclose(variance_dict['FactorC'], var_dict['FactorC'], atol=tolerance) and
    #         np.isclose(variance_dict['FactorA x FactorB'], var_dict['FactorA x FactorB'], atol=tolerance) and
    #         np.isclose(variance_dict['FactorA x FactorC'], var_dict['FactorA x FactorC'], atol=tolerance) and
    #         np.isclose(variance_dict['FactorB x FactorC'], var_dict['FactorB x FactorC'], atol=tolerance) and
    #         np.isclose(variance_dict['FactorA x FactorB x FactorC'], var_dict['FactorA x FactorB x FactorC'], atol=tolerance)
    #     ):
    #         # Differentiation table for different rho^2 scenarios
    #         g_coeff_table = GT.g_coeff()

    #         # Summary Statistics
    #         GT.summary()  # Print ANOVA table
    #         GT.variance_summary()  # Print variance components table
    #         GT.g_coeff_summary()  # Print differentiation table
    #         print(f"Variance components are close to pre-defined values for seed: {i}")
    #         break
    #     else:
    #         print(f"Variance components are not close to pre-defined values for seed: {i}")
    
    ## ----------------- A X B X C X D Test---------------- ##
    # Define the levels for each factor
    levels_dict = {
        'FactorA': 100,
        'FactorB': 3,
        'FactorC': 2,
        'FactorD': 5
    }
    
    # Define the expected variance components
    var_dict = {
        'FactorA': 10,
        'FactorB': 6,
        'FactorC': 5,
        'FactorD': 4,
        'FactorA x FactorB': 3,
        'FactorA x FactorC': 5,
        'FactorA x FactorD': 4,
        'FactorB x FactorC': 4,
        'FactorB x FactorD': 3,
        'FactorC x FactorD': 2,
        'FactorA x FactorB x FactorC': 2,
        'FactorA x FactorB x FactorD': 3,
        'FactorA x FactorC x FactorD': 2,
        'FactorB x FactorC x FactorD': 3.5,
        'FactorA x FactorB x FactorC x FactorD': 1.5
    }
    
    design = 'FactorA x FactorB x FactorC x FactorD'
    
    for i in range(55, 10000):
        # Define the seed
        seed = i

        # Generate the synthetic data
        data, exp_variance_dict = generate_data(
            design=design,
            levels_dict=levels_dict,
            exp_variance_dict=var_dict,
            seed=seed
        )

        print(data.head())
        print(exp_variance_dict)

        GT = GeneralizIT(data, design=design, response='Response')
        GT.calculate_anova()

        # Get the variance components
        variance_dict = GT.anova_table.set_index('Source of Variation')['Variance Component'].to_dict()
        
        # replace '×' with 'x' in the keys
        variance_dict = {key.replace('×', 'x'): value for key, value in variance_dict.items()}

        # Drop 'Total' from the dictionary
        variance_dict.pop('Total')

        print(f"{'-'*50}")
        print(f"Variance Dict: {variance_dict}")
        print(f"{'-'*50}")
        
        tolerance = 2 # Tolerance for variance components
        get_summary = True
        # Check if the variance components are close to the pre-defined values
        for key, value in variance_dict.items():
            if key in var_dict:
                if np.isclose(value, var_dict[key], atol=tolerance):
                    print(f"{key} is close to pre-defined value")
                    # If all variance components are close to the pre-defined values, get the summary statistics
                    if key == list(var_dict.keys())[-1]:
                        get_summary = True
                else:
                    print(f"{key} is not close to pre-defined value")
                    break
            else:
                print(f"{key} is not in pre-defined value")
        
        if get_summary:
            # Differentiation table for different rho^2 scenarios
            g_coeff_table = GT.g_coeff()

            # Summary Statistics
            GT.summary()  # Print ANOVA table
            GT.variance_summary()  # Print variance components table
            GT.g_coeff_summary()  # Print differentiation table
            print(f"Variance components are close to pre-defined values for seed: {i}")
            break
        else:
            print(f"Variance components are not close to pre-defined values for seed: {i}")
            
    # ---------------------------------------------------------
    # SYNTHETIC DATA FROM BRENNAN (2001) - SYTNHETIC DATA SET NO. 3

    data = {
        'Person': range(1, 11),
        'O1_i1': [2, 4, 5, 5, 4, 4, 2, 3, 0, 6],
        'O1_i2': [6, 5, 5, 9, 3, 4, 6, 4, 5, 8],
        'O1_i3': [7, 6, 4, 8, 5, 4, 6, 4, 4, 7],
        'O1_i4': [5, 7, 6, 6, 6, 7, 5, 5, 5, 6],
        'O2_i1': [2, 6, 5, 5, 4, 6, 2, 6, 5, 6],
        'O2_i2': [5, 7, 4, 7, 5, 4, 7, 6, 5, 8],
        'O2_i3': [5, 5, 5, 7, 6, 7, 7, 6, 5, 8],
        'O2_i4': [5, 7, 5, 6, 4, 8, 5, 4, 3, 6]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    print(df.head(10))

    # New DataFrame with 'Person', 'i', 'o', and 'Response'
    new_data = {
        'Person': [],
        'i': [],
        'o': [],
        'Response': []
    }

    # Populate the new DataFrame
    for person in range(1, 11):
        for o in [1, 2]:  # Assuming 'O1' and 'O2'
            for i in range(1, 5):  # Assuming 'i1', 'i2', 'i3', 'i4'
                key = f'O{o}_i{i}'
                response = df.at[person-1, key]
                new_data['Person'].append(person)
                new_data['i'].append(i)
                new_data['o'].append(o)
                new_data['Response'].append(response)

    # Convert to DataFrame
    formatted_df = pd.DataFrame(new_data)

    print(formatted_df.head(8))
    print(formatted_df.tail(8))
    
    GT = GeneralizIT(data=formatted_df, design_str='Person x i x o', response='Response')
    
    GT.calculate_anova()
    GT.g_coeffs()
    
    GT.anova_summary()
    GT.g_coeff_summary()
    
    GT.calculate_d_study(levels={'Person': None, 'i': [4, 8], 'o': [1, 2]})
    GT.d_study_summary()
    
    GT.calculate_confidence_intervals(alpha=0.05)
    GT.confidence_intervals_summary()
    
    # # ---------------------------------------------------------
    # Synthetic Data Set No. 2 from Brennan (2001)
    
    # Load the csv file syndata2.csv
    df = pd.read_csv('syndata2.csv')

    print(df.head())

    # New DataFrame with columns 'person', 'item', 'Response'
    new_data = {
        'person': [],
        'item': [],
        'Response': []
    }

    # Populate the new DataFrame
    for person in range(1, 11):
        for item in range(1, 9):
            key = f'personi_item{item}'
            
            if key in df.columns:
                response = df.at[person-1, key]
                new_data['person'].append(person)
                new_data['item'].append((person-1)*8 + item)
                new_data['Response'].append(response)

    # Convert to DataFrame
    formatted_df = pd.DataFrame(new_data)

    print(formatted_df.head(10))

    GT = GeneralizIT(data=formatted_df, design_str='item:person', response='Response')
    
    GT.calculate_anova()
    GT.g_coeffs()
    
    GT.anova_summary()
    GT.g_coeff_summary()
    
    GT.calculate_confidence_intervals(alpha=0.05)
    GT.confidence_intervals_summary()
    
    # # ---------------------------------------------------------
    # # Synthetic Data Set No. 4 from Brennan (2001)
    # # Load the csv file syndata4.csv
    # df = pd.read_csv('syndata4.csv')

    # print(df.head())

    # # New DataFrame with columns 'person', 't', 'r', 'Response'
    # new_data = {
    #     'person': [],
    #     't': [],
    #     'r': [],
    #     'Response': []
    # }

    # # Populate the new DataFrame
    # for person in range(1, 11):
    #     for t in [1, 2, 3]:  # Assuming 't1', 't2', 't3'
    #         for r in range(1, 13):  # Assuming 'r1' to 'r12'
    #             key = f't{t}_r{r}'
    #             # check if the key exists
    #             if key in df.columns:
    #                 response = df.at[person-1, key]
    #                 new_data['person'].append(person)
    #                 new_data['t'].append(t)
    #                 new_data['r'].append(r)
    #                 new_data['Response'].append(response)

    # # Convert to DataFrame
    # formatted_df = pd.DataFrame(new_data)

    # print(formatted_df.head(10))

    # # Initialize the GeneralizIT class
    # GT = GeneralizIT(data=formatted_df, design_str='person x (r:t)', response='Response')
    
    # GT.calculate_anova()
    # GT.g_coeffs()
    
    # GT.anova_summary()
    # GT.g_coeff_summary()
    
    # GT.calculate_d_study(levels={'person': None, 't': [1, 2, 3], 'r': [12, 6, 4]})
    # GT.d_study_summary()
    
    # GT.calculate_confidence_intervals(alpha=0.05)
    # GT.confidence_intervals_summary()
        