import os
from datasets import load_dataset
import json

def download_dataset(output_base: str = "output") -> None:

    output_path = os.path.join(output_base, f"aozora_clean.jsonl")

    with open(output_path, 'w', encoding='utf-8') as o:
        ds = load_dataset('globis-university/aozorabunko-clean')
        ds = ds.filter(lambda row: row['meta']['文字遣い種別'] == '新字新仮名')  # 新字新仮名に限定
        books = ds['train']
        for book in books:
            for line in book['text'].splitlines():
                if len(line) > 0:
                    sentence_dict = {'text': line}
                    o.write(json.dumps(sentence_dict, ensure_ascii=False) + '\n')
