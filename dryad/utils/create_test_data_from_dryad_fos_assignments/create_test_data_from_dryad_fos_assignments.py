import json
import argparse
import sys
import re


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Classify scientific publications based on field of science.")
    parser.add_argument(
        "-i", "--input_file", help="Path to the input JSON file containing publication metadata")
    parser.add_argument("-c", "--classification_file",
                        help="Path to the JSON file containing the classification system")
    parser.add_argument("-o", "--output_file",
                        help="Path to the output JSON file")
    parser.add_argument(
        "-u", "--unmatched_file", default="unmatched.json", help="Path to the output JSON file for unmatched records")
    return parser.parse_args()


def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file.")
        sys.exit(1)
    except IOError:
        print(f"Error: Unable to read file {file_path}.")
        sys.exit(1)


def normalize_string(s):
    return re.sub(r'[^\w\s]', '', s).lower().strip()


def build_classification_lookup(classification_data):
    lookup = {}
    for main_class, data in classification_data.items():
        for sub_class in data['sub']:
            lookup[normalize_string(sub_class)] = main_class
    return lookup


def classify_record(record, classification_lookup):
    if 'fieldOfScience' not in record:
        return record, False
    field_of_science = record['fieldOfScience']
    normalized_field = normalize_string(field_of_science)
    main_class = classification_lookup.get(normalized_field)
    if main_class:
        record['main-class'] = main_class
        record['sub-class'] = field_of_science
        return record, True
    else:
        return record, False


def process_records(records, classification_lookup):
    matched_records = []
    unmatched_records = []
    for record in records:
        classified_record, is_matched = classify_record(
            record, classification_lookup)
        if is_matched:
            matched_records.append(classified_record)
        else:
            unmatched_records.append(classified_record)
    print(f"Matched {len(matched_records)} records.")
    print(f"Unmatched {len(unmatched_records)} records.")
    return matched_records, unmatched_records


def write_json_file(data, file_path):
    try:
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=2)
        print(f"Successfully wrote records to {file_path}")
    except IOError:
        print(f"Error: Unable to write to file {file_path}.")
        sys.exit(1)


def main():
    args = parse_arguments()
    publication_data = load_json_file(args.input_file)
    classification_data = load_json_file(args.classification_file)
    classification_lookup = build_classification_lookup(classification_data)
    matched_records, unmatched_records = process_records(
        publication_data, classification_lookup)
    write_json_file(matched_records, args.output_file)
    write_json_file(unmatched_records, args.unmatched_file)


if __name__ == "__main__":
    main()
