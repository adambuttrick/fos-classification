# Create test data from Dryad FOS assignments

Use existing Fields of science and technology (FOS) assignments in Dryad records to create test data entries by inferring the main classificaiton from the currently sub class assignments

## Files

- `create_test_data_from_dryad_fos_assignments.py`: Main script for classification
- `fos.json`: JSON file containing the classification system

## Usage

```
python create_test_data_from_dryad_fos_assignments.py -i <input_file> -c <classification_file> -o <output_file> [-u <unmatched_file>]
```

Arguments:
- `-i, --input_file`: Path to input JSON file with publication metadata
- `-c, --classification_file`: Path to JSON file with classification system
- `-o, --output_file`: Path to output JSON file for matched records
- `-u, --unmatched_file`: (Optional) Path to output JSON file for unmatched records (default: unmatched.json)

## Classification System

The `classifications/fos.json` file decribes the hierarchical FOS classifications with its main classes and subclasses.

## Output

The script generates two JSON files:
1. Matched records with assigned main-class and sub-class
2. Unmatched records that couldn't be classified
