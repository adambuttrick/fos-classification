import json
import csv
import argparse
from collections import Counter, defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze Dryad JSON data for FOS class distributions")
    parser.add_argument("-i", "--input_file", type=str, required=True,
                        help="Path to the input JSON file")
    parser.add_argument("-o", "--output_file", type=str, default="output.csv",
                        help="Path to the output CSV file")
    return parser.parse_args()


def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON file should contain a list of objects")
        return data
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}")
        exit(1)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        exit(1)


def process_data(data):
    main_class_counts = Counter()
    sub_class_counts = defaultdict(Counter)
    for item in data:
        main_class = item.get('main-class')
        sub_class = item.get('sub-class')
        if main_class:
            main_class_counts[main_class] += 1
            if sub_class:
                sub_class_counts[main_class][sub_class] += 1
    return main_class_counts, sub_class_counts


def generate_summary_statistics(main_class_counts, sub_class_counts):
    all_sub_classes = [sub for subs in sub_class_counts.values()
                       for sub in subs]
    total_entries = sum(main_class_counts.values())
    return {
        "total_entries": total_entries,
        "unique_main_classes": len(main_class_counts),
        "unique_sub_classes": len(set(all_sub_classes)),
        "most_common_main_class": main_class_counts.most_common(1)[0] if main_class_counts else None,
        "most_common_sub_class": Counter(all_sub_classes).most_common(1)[0] if all_sub_classes else None,
        "least_common_main_class": main_class_counts.most_common()[-1] if main_class_counts else None,
        "least_common_sub_class": Counter(all_sub_classes).most_common()[-1] if all_sub_classes else None
    }


def print_summary_statistics(stats):
    print("Summary Statistics:")
    print(f"Total entries: {stats['total_entries']}")
    print(f"Unique main classes: {stats['unique_main_classes']}")
    print(f"Unique sub-classes: {stats['unique_sub_classes']}")
    if stats['most_common_main_class']:
        print(f"Most common main class: {stats['most_common_main_class'][0]} ({stats['most_common_main_class'][1]} occurrences)")
    if stats['most_common_sub_class']:
        print(f"Most common sub-class: {stats['most_common_sub_class'][0]} ({stats['most_common_sub_class'][1]} occurrences)")
    if stats['least_common_main_class']:
        print(f"Least common main class: {stats['least_common_main_class'][0]} ({stats['least_common_main_class'][1]} occurrences)")
    if stats['least_common_sub_class']:
        print(f"Least common sub-class: {stats['least_common_sub_class'][0]} ({stats['least_common_sub_class'][1]} occurrences)")


def write_csv(output_file, main_class_counts, sub_class_counts):
    try:
        with open(output_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['main-class', 'sub-class', 'count'])
            for main_class, count in main_class_counts.items():
                writer.writerow([main_class, '', count])
                for sub_class, sub_count in sub_class_counts[main_class].items():
                    writer.writerow([main_class, sub_class, sub_count])

        print(f"CSV file written successfully: {output_file}")
    except IOError:
        print(f"Error: Unable to write to file {output_file}")
        exit(1)


def main():
    args = parse_arguments()
    data = load_data(args.input_file)
    main_class_counts, sub_class_counts = process_data(data)
    stats = generate_summary_statistics(main_class_counts, sub_class_counts)
    print_summary_statistics(stats)
    write_csv(args.output_file, main_class_counts, sub_class_counts)


if __name__ == "__main__":
    main()
