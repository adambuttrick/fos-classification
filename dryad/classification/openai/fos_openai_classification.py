import os
import re
import csv
import json
import openai
import argparse
from tqdm import tqdm
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Classify research papers using OpenAI.")
    parser.add_argument("-t", "--test_data", required=True,
                        help="Path to the JSON file containing test data")
    parser.add_argument("-o", "--output", required=True,
                        help="Path to save the classification results")
    parser.add_argument("-m", "--model", required=True,
                        help="OpenAI model to use for classification (e.g., gpt-4, gpt-3.5)")
    parser.add_argument("-p", "--prompt_file", required=True,
                        help="Path to the file containing the classification prompt")
    parser.add_argument("-s", "--system_prompt_file",
                        help="Path to the file containing the system prompt (optional)")
    parser.add_argument("-l", "--true_label",
                        help="Key in the test data to use for the true label")
    parser.add_argument("--temperature", type=float, default=0.1,
                        help="Temperature for the OpenAI model (default: 0.1)")
    parser.add_argument("--max_tokens", type=int, default=500,
                        help="Max tokens for the OpenAI model (default: 500)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--metrics_file",
                        help="Path to save the metrics CSV file (default: {input_file_name}_metrics.csv)")
    return parser.parse_args()


def normalize_string(s):
    return re.sub(r'[^\w\s]', '', s).lower().strip()


def load_prompt(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()


def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def classify_record(record_data, model, system_prompt, prompt_template, temperature, max_tokens):
    prompt = prompt_template.format(
        title=record_data['title'],
        abstract=record_data['abstract'])
    messages = [{"role": "user", "content": prompt}]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return None


def calculate_overall_metrics(true_labels, predicted_labels):
    tp = sum(1 for t, p in zip(true_labels, predicted_labels) if t == p)
    fp = sum(1 for t, p in zip(true_labels, predicted_labels) if t != p)
    fn = sum(1 for t, p in zip(true_labels, predicted_labels) if t != p)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision +
                                     recall) if (precision + recall) > 0 else 0
    accuracy = tp / len(true_labels) if len(true_labels) > 0 else 0
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def write_metrics_to_csv(metrics, file_path):
    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Metric', 'Value'])
        for metric, value in metrics.items():
            writer.writerow([metric.capitalize(), f"{value:.4f}"])


def classify_records(test_data, model, system_prompt, prompt_template, true_label, temperature, max_tokens, verbose, output_path, metrics_file):
    true_labels = []
    predicted_labels = []
    with open(output_path, 'w') as f:
        f.write('[\n')
        first_item = True
        for record in tqdm(test_data, disable=not verbose):
            predicted_label = classify_record(
                record, model, system_prompt, prompt_template, temperature, max_tokens)
            if predicted_label is None:
                continue  # Skip in case of API errors
            normalized_predicted = normalize_string(predicted_label)
            record_label = record.get(true_label)
            if record_label:
                normalized_actual = normalize_string(record_label)
                is_match = normalized_predicted == normalized_actual
                true_labels.append(normalized_actual)
                predicted_labels.append(normalized_predicted)
            else:
                is_match = None
            if verbose:
                print(f"Identifier: {record['identifier']}")
                print(f"Title: {record['title']}")
                print(f"Prediction: {predicted_label}")
                if record_label:
                    print(f"Actual: {record_label}")
                    print(f"Match: {is_match}")
                print("---")
            result = {
                "identifier": record['identifier'],
                "predicted_label": predicted_label,
                "true_label": record_label,
                "is_match": is_match
            }
            if not first_item:
                f.write(',\n')
            json.dump(result, f, indent=2)
            first_item = False
        f.write('\n]')
    if len(true_labels) > 0:
        metrics = calculate_overall_metrics(true_labels, predicted_labels)
        write_metrics_to_csv(metrics, metrics_file)
        if verbose:
            print(f"Overall metrics:")
            for metric, value in metrics.items():
                print(f"  {metric.capitalize()}: {value:.4f}")
            print(f"Metrics saved to: {metrics_file}")
    elif verbose:
        print(f"No predictions were made (no actual classes provided in the test data under the key '{true_label}').")
    return metrics if len(true_labels) > 0 else None


def main():
    args = parse_arguments()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if openai.api_key is None:
        raise ValueError(
            "OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    test_data = load_json_data(args.test_data)
    prompt_template = load_prompt(args.prompt_file)
    system_prompt = load_prompt(
        args.system_prompt_file) if args.system_prompt_file else None
    if args.metrics_file:
        metrics_file = args.metrics_file
    else:
        base_name = os.path.splitext(os.path.basename(args.test_data))[0]
        metrics_file = f"{base_name}_metrics.csv"
    if args.verbose:
        print("\nStarting classification...")
    metrics = classify_records(
        test_data, args.model, system_prompt, prompt_template, args.true_label,
        args.temperature, args.max_tokens, args.verbose, args.output, metrics_file)
    if args.verbose:
        print(f"Classification complete. Results saved to {args.output}")
        print(f"Metrics saved to {metrics_file}")
        if metrics:
            print(f"Final accuracy: {metrics['accuracy']:.2%}")
            print(f"Final F1-score: {metrics['f1']:.4f}")


if __name__ == "__main__":
    main()
