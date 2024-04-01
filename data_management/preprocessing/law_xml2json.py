import os
import json
from xml.etree import ElementTree as ET

input_path = "/persistentshare/storage/team_nakamura/member/horie/dataset/lawdata"
json_path = "/persistentshare/storage/team_nakamura/member/horie/dataset/json/jalaw.jsonl"

num = 0
in_path = input_path
out_path = json_path
with open(out_path, 'w', encoding='utf-8') as o:
  for root, _, files in os.walk(in_path):
    for file in files:
      if file.endswith('.xml'):
        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
          tree = ET.parse(f)
          root = tree.getroot()
          for e in root.iter('Sentence'):
            if e.text is not None:
              sentence_dict = {'text': e.text}
              o.write(json.dumps(sentence_dict, ensure_ascii=False) + '\n')
              num += 1
              if num % 10000 == 0:
                print(f'num: {num}')
# 最後の改行を削除する必要がある場合は、ファイルの末尾からそれを削除するロジックを追加することも可能ですが、
# 通常はそのままで問題ない場合が多いです。