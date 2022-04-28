import argparse
import json
from glob import glob
from typing import List, Dict

def load_and_sort_jsons(recalls_dir:str) -> List[Dict]:
    json_lines = []

    for json_file in glob(f'{recalls_dir}/**/*.json'):
        with open(json_file, 'r') as file:
            file_json = json.load(file)
            json_lines.append(file_json)

    json_lines.sort(key=lambda rec: f"{rec.get('start_date', '')}-{rec.get('end_date', '')}-{rec['id']}")
    return json_lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sorts the JSON and merges into a single ND-JSON file')
    parser.add_argument('--dir', type=str, help="The recalls directory to recursively scan")
    parser.add_argument('--dest', type=str, help="The destination ND-JSON file to write")
    args = parser.parse_args()

    lines = load_and_sort_jsons(args.dir)
    with open(args.dest, 'w') as file:
        for line in lines:
            file.write(f"{json.dumps(line)}\n")
