# OpenAI Dryad Dataset Subject Classifier

Classifies Dryad dataset records using the OpenAI API.

## Prerequisites

1. **OpenAI API Key**: You must have an OpenAI API key. You can sign up for an API key at [OpenAI's official website](https://platform.openai.com/signup/).
2. **Set the API Key**: Store the API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Installation
   ```
   pip install -r requirements.txt
   ```

## Usage

```
python script.py -t test_data.json -o output.json -m openai_model -p prompt.txt [-s system_prompt.txt] [-l true_label_key] [--temperature 0.1] [--max_tokens 500] [-v] [--metrics_file metrics.csv]
```

## Arguments

- `-t`: Path to the test data JSON file (required)
- `-o`: Output path for classification results (required)
- `-m`: OpenAI model name (e.g., `gpt-4`, `gpt-3.5`) (required)
- `-p`: Path to the classification prompt file (required)
- `-s`: Path to the system prompt file (optional)
- `-l`: Key for true label in the test data (optional)
- `--temperature`: Model temperature (default: 0.1, controls randomness)
- `--max_tokens`: Maximum tokens for the model output (default: 500)
- `-v`: Enable verbose output (optional)
- `--metrics_file`: Path to save the metrics CSV file (optional, default: `{input_file_name}_metrics.csv`)

## Output

- **JSON File**: Contains classification results, including predicted labels, true labels (if provided), and whether they match.
- **CSV File**: Contains overall metrics such as accuracy, precision, recall, and F1-score.

## Example Usage

```
python script.py -t test_data.json -o results.json -m gpt-4 -p classification_prompt.txt --temperature 0.2 --max_tokens 750 -v
```

## Output

- `output.json`: JSON file containing the classification results.
- `metrics.csv`: CSV file containing accuracy, precision, recall, and F1-score metrics.

## Notes

- You will need to ensure you have enough API credits preloaded to run the classification for your dataset. Refer to the OpenAI API documentation for details