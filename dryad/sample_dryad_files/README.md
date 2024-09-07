# Sample Dryad files

Script for sampling records from Dryad files in various ways.

## Usage

```
python sample_dryad_files.py -i <input_file> -o <output_file> -m <mode> -n <num_samples> [-c <class_value>]
```

## Arguments

- `-i`, `--input_file`: Path to input JSON file
- `-o`, `--output_file`: Path to output JSON file (or base name for train/test/validation files)
- `-m`, `--mode`: Sampling mode (all, main, sub, categories, train)
- `-n`, `--num_samples`: Number of samples (not used in train mode)
- `-c`, `--class_value`: Class value for 'main' or 'sub' mode

## Modes

- `all`: Random sampling from the entire dataset
- `main`: Sample records based on a specific main class
- `sub`: Sample records based on a specific sub-class
- `categories`: Sample evenly across all main categories
- `train`: Split the dataset into train, test, and validation sets

### Mode Details

- `all`: Randomly selects the specified number of samples from the entire dataset.
- `main`/`sub`: Filters records by the specified class value before sampling. Requires `-c` argument.
- `categories`: Attempts to sample evenly from all main categories, cycling through them until the sample size is reached.
- `train`: Shuffles the dataset and splits it into train, test, and validation sets. Distributions are:
  - Train: 80% of the data
  - Test: 10% of the data
  - Validation: 10% of the data
  Outputs three separate files with suffixes _train.json, _test.json, and _validation.json.

## Example

```
python sample_dryad_files.py -i data.json -o sampled.json -m categories -n 100
```

This samples 100 records evenly across all main categories in data.json and saves the result to sampled.json.

For the train mode:

```
python sample_dryad_files.py -i data.json -o split_data -m train
```

This  will create three files: split_data_train.json, split_data_test.json, and split_data_validation.json with the 80-10-10 split.