"""
Auto-generated config writer for job_configs.csv with fixed and variable fields.
Generates all combinations across all fields.
"""
import argparse
import csv
import os
import json
import itertools
try:
    import yaml
except ImportError:
    yaml = None  # YAML support is optional


# === Option 1: Fill manually ===
config = {
    'dataset_name': ['conflux', 'conflux-100k', 'conflux-1M'],
    'temperature': ['0.0', '0.1'],
    'gas': ['B', 'A', 'C'],
}

# === Fixed values ===
fixed_values = {
    'model': 'gpt2',
    'epsilon': '4',
}

variable_fields = ['temperature']


# === Option 2: Load from JSON or YAML ===
def load_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")
    
    ext = os.path.splitext(file_path)[-1].lower()
    with open(file_path, 'r') as f:
        if ext == '.json':
            return json.load(f)
        elif ext in ['.yaml', '.yml']:
            if yaml is None:
                raise ImportError("PyYAML is not installed. Run `pip install pyyaml`.") 
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format. Use .json or .yaml/.yml")

def validate_config(config):
    for k, v in config.items():
        if not isinstance(v, list):
            raise ValueError(f"Config value for '{k}' must be a list")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file_path", type=str, help="Path to write the CSV", default="job_configs.csv")
    parser.add_argument("--config_file", type=str, help="Path to a JSON/YAML config file")
    args = parser.parse_args()

    if args.config_file:
        config = load_from_file(args.config_file)
    
    validate_config(config)

    # Fields to combine (everything that's not fixed)
    all_config_fields = list(config.keys())

    # Generate Cartesian product
    all_combinations = list(itertools.product(*[config[k] for k in all_config_fields]))

    rows = []
    for values in all_combinations:
        row = dict(zip(all_config_fields, values))
        row.update(fixed_values)
        rows.append(row)

    # === Write to CSV ===
    with open(args.output_file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['dataset_name', 'temperature', 'gas', 'model', 'epsilon'])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"✅ {args.output_file_path} written successfully.")
