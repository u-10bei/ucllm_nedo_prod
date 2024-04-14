from fugashi import Tagger
import json

tagger = Tagger('-Owakati')

json_path = '/persistentshare/storage/team_nakamura/member/horie/dataset/aozora/aozora_clean.jsonl'
mabiki_path = '/persistentshare/storage/team_nakamura/member/horie/dataset/mabiki_a/aozora_mabiki.jsonl'

input = 0
flag =  0
output = 0
with open(mabiki_path, 'w', encoding='utf-8') as o:
  with open(json_path, 'r', encoding='utf-8') as f:
    for line in f:
      input += 1
      text = json.loads(line)['text']
      for word in tagger(text):
        if word.feature.lForm == None:
          flag += 1
      if flag == 0:
        o.write(line)
        output += 1
      flag = 0
      if input % 100000 == 0:
        print(f'input: {input}, output: {output}, rate: {output / input}')
print(f'input: {input}, output: {output}, rate: {output / input}')