# Ollama Dryad Dataset Subject Classifier

Classifies Dryad dataset records using local LLMs via Ollama.

## Prerequisites

1. Install Ollama: Follow the instructions at [Ollama's official website](https://ollama.ai/download).
2. Download Ollama models: After installation, download the models you want to use. For example:
   ```
   ollama pull phi3
   ollama pull mistral
   ```
   Refer to Ollama's documentation for available models and usage instructions.

## Installation
   ```
   pip install -r requirements.txt
   ```

## Usage

```
python script.py -t test_data.json -o output.json -m ollama_model -p prompt.txt [-s system_prompt.txt] [-l true_label_key] [--temperature 0.1] [--top_k 10] [-v] [--metrics_file metrics.csv]
```

## Arguments

- `-t`: Path to test data JSON file (required)
- `-o`: Output path for classification results (required)
- `-m`: Ollama model name (required)
- `-p`: Classification prompt file path (required)
- `-s`: System prompt file path (optional)
- `-l`: Key for true label in test data (optional)
- `--temperature`: Model temperature (default: 0.1)
- `--top_k`: Model top-k value (default: 10)
- `-v`: Enable verbose output
- `--metrics_file`: Path for metrics CSV file

## Output

- JSON file with classification results
- CSV file with overall metrics (accuracy, precision, recall, F1-score)

## Note

Ensure you have sufficient system resources to run the chosen Ollama model. Larger models may require significant resources.