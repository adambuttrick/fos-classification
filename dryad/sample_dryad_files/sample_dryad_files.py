import json
import random
import argparse
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Sample records from a JSON file.")
    parser.add_argument("-i", "--input_file",
                        help="Path to the input JSON file")
    parser.add_argument("-o", "--output_file",
                        help="Path to the output JSON file (or base name for train/test/validation files)")
    parser.add_argument(
        "-m", "--mode", choices=["all", "main", "sub", "categories", "train"], help="Sampling mode")
    parser.add_argument("-n", "--num_samples", type=int,
                        help="Number of samples to draw (not used in 'train' mode)")
    parser.add_argument("-c", "--class_value",
                        help="Class value for 'main' or 'sub' mode")
    args = parser.parse_args()
    if args.mode != "train" and args.num_samples is None:
        parser.error("--num_samples is required for all modes except 'train'")
    if args.mode in ["main", "sub"] and not args.class_value:
        parser.error("--class_value is required when mode is 'main' or 'sub'")
    return args


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in input file: {file_path}")


def save_json(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    except IOError:
        raise IOError(f"Error writing to output file: {file_path}")


def sample_all(data, num_samples):
    if num_samples > len(data):
        raise ValueError(f"Not enough records to sample {num_samples} items")
    return random.sample(data, num_samples)


def sample_by_class(data, num_samples, class_type, class_value):
    filtered_data = [record for record in data if record.get(
        class_type) == class_value]
    if num_samples > len(filtered_data):
        raise ValueError(f"Not enough records in {class_type} '{class_value}' to sample {num_samples} items")
    return random.sample(filtered_data, num_samples)


def sample_categories(data, num_samples):
    categories = defaultdict(list)
    for record in data:
        categories[record.get("main-class")].append(record)
    samples = []
    sampled_identifiers = set()
    category_keys = list(categories.keys())
    while len(samples) < num_samples and category_keys:
        for category in category_keys[:]:
            if len(samples) >= num_samples:
                break
            records = categories[category]
            if not records:
                category_keys.remove(category)
                continue
            # Try to find a record that hasn't been sampled yet
            for _ in range(len(records)):
                record = random.choice(records)
                if record['identifier'] not in sampled_identifiers:
                    samples.append(record)
                    sampled_identifiers.add(record['identifier'])
                    records.remove(record)
                    break
            else:
                # If we've exhausted all records in this category, remove it
                category_keys.remove(category)
    return samples


def sample_records(data, num_samples, mode, class_value=None):
    if mode == "all":
        return sample_all(data, num_samples)
    elif mode in ["main", "sub"]:
        return sample_by_class(data, num_samples, f"{mode}-class", class_value)
    elif mode == "categories":
        return sample_categories(data, num_samples)
    else:
        raise ValueError(f"Invalid sampling mode: {mode}")


def split_train_test_validation(data):
    random.shuffle(data)
    total = len(data)
    train_end = int(0.8 * total)
    test_end = int(0.9 * total)

    return {
        'train': data[:train_end],
        'test': data[train_end:test_end],
        'validation': data[test_end:]
    }


def main():
    args = parse_arguments()
    data = load_json(args.input_file)
    try:
        if args.mode == "train":
            splits = split_train_test_validation(data)
            for split_name, split_data in splits.items():
                if args.output_file:
                    output_file = f"{args.output_file}_{split_name}.json"
                else:
                    output_file = f"{split_name}.json"
                save_json(split_data, output_file)
                print(f"Successfully saved {len(split_data)} records to {output_file}")
        else:
            sampled_data = sample_records(
                data, args.num_samples, args.mode, args.class_value)
            save_json(sampled_data, args.output_file)
            print(f"Successfully sampled {len(sampled_data)} records to {args.output_file}")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except IOError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
