# Test function
def test_parse_facets():
    """Test function to verify facet parsing for all design patterns"""
    test_cases = [
        ("persons x raters", 
         {'facet_1': 'persons', 'facet_2': 'raters'}, "crossed"),
        ("items:persons", 
         {'i': 'items', 'p': 'persons'}, 2),
        ("raters x items x helpers", 
         {'facet_1': 'raters', 'facet_2': 'items', 'facet_3': 'helpers'}, "crossed"),
        ("raters x (persons:items)", 
         {'p': 'raters', 'i': 'persons', 'h': 'items'}, 4),
        ("(items:persons) x helpers", 
         {'i': 'items', 'p': 'persons', 'h': 'helpers'}, 5),
        ("items:(persons x helpers)", 
         {'i': 'items', 'p': 'persons', 'h': 'helpers'}, 6),
        ("(doctors x items): raters", 
         {'i': 'doctors', 'h': 'items', 'p': 'raters'}, 7),
        ("xylaphones:helpers:persons", 
         {'i': 'xylaphones', 'h': 'helpers', 'p': 'persons'}, 8)
    ]
    
    for input_str, expected, design_num in test_cases:
        try:
            num_result, facets = match_research_design(input_str)
            result = parse_facets(design_facets=facets, design_num=num_result)
            assert num_result == design_num, f"Failed for {input_str}. Got {num_result}, expected {design_num}"
            assert result == expected, f"Failed for {input_str}. Got {result}, expected {expected}"
            print(f"✓ Passed: {input_str}")
            # print_design(num_result, result)
        except AssertionError as e:
            print(f"✗ Failed: {str(e)}")
        except Exception as e:
            print(f"✗ Error processing {input_str}: {str(e)}")