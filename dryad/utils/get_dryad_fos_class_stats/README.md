# Dryad FOS Classification Statistics

Report summary stats for the Fields of science and technology (FOS) classifications assigned to Dryad records.

## Usage

```
python get_dryad_fos_class_stats.py -i <input_file> [-o <output_file>]
```

Arguments:
- `-i, --input_file`: Path to the input JSON file (output from create_test_data_from_dryad_fos_assignments.py)
- `-o, --output_file`: (Optional) Path to the output CSV file (default: output.csv)

## Input

The input should be the JSON file output from `create_test_data_from_dryad_fos_assignments.py` containing a list of Dryad records, each with `main-class` and `sub-class` fields appended.

## Output

1. Console output: Summary statistics including total entries, unique classes, and most/least common classes.
2. CSV file: Detailed breakdown of main classes and subclasses with their respective counts.

## Output Format

The output CSV has the following columns:
- `main-class`: The main FOS classification
- `sub-class`: The subclass of the FOS classification (empty for main class rows)
- `count`: The number of occurrences
