#!/usr/bin/env python3
import argparse
import csv
import json


def convert_ndjson_to_csv(json_path: str, csv_path: str):
    fieldnames = ['start_date', 'end_date', 'id', 'title', 'url', 'reasons', 'status', 'risk_level',
    'establishment_id', 'establishment_slug', 'establishment_name', 'establishment_address',
    'establishment_telephone', 'establishment_grant_date', 'establishment_activities', 'products',
    'quantity_recovered', 'quantity_unit', 'states']

    with open(json_path, 'r') as jsonfile:
        with open(csv_path, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile,fieldnames=fieldnames, extrasaction='ignore', dialect='unix')
            csvwriter.writeheader()

            for line in jsonfile.readlines():
                parsed = json.loads(line)

                # Some preprocessing
                parsed['summary'] = parsed['summary'].replace('\n', '')

                if parsed['states']:
                    parsed['states'] = ', '.join(parsed['states'])

                parsed['reasons'] = ', '.join(parsed['reasons'])

                if parsed.get('establishment', None) is not None:
                    for key in parsed['establishment'].keys():
                        parsed[f'establishment_{key}'] = parsed['establishment'][key]

                    parsed['establishment_address'] = parsed['establishment_address'].strip().replace('\n', '')

                csvwriter.writerow(parsed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert the recalls NDJSON to a CSV')
    parser.add_argument('--json', type=str, help='The source ND JSON file')
    parser.add_argument('--csv', type=str, help='The destination CSV file')
    args = parser.parse_args()

    convert_ndjson_to_csv(args.json, args.csv)
