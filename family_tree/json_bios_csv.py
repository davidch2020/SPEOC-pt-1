import pandas as pd

def json_to_csv_simple(in_path, out_path):
    df = pd.read_json(in_path, lines=True)  # lines=True for JSONL
    df.to_csv(out_path, index=False)

# Example usage:
json_to_csv_simple('bios_scraping/wikitree_bios.jsonl', 'bios_scraping/wikitree_bios.csv')
