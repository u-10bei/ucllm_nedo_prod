import datasets

hug_base = "JINIAC/"
input_base = "/persistentshare/storage/team_nakamura/member/horie/dataset/"

dataset_type = "aozora"
filter_type = "before"

if dataset_type == "aozora":
  if filter_type == "filter":
    hug_repo = hug_base + "aozorabunko_filter"
    input_path = input_base + "merge/aozora_filter.jsonl"
  elif filter_type == "before":
    hug_repo = hug_base + "aozorabunko_prefilter"        
    input_path = input_base + "aozora/aozora_clean.jsonl"          
elif dataset_type == "ja_wiki":
  if filter_type == "filter":
    hug_repo = hug_base + "ja_wiki_20240301_filter"
    input_path = input_base + "merge/jawiki_filter.jsonl"
  elif filter_type == "before":
    hug_repo = hug_base + "ja_wiki_20240301_prefilter"        
    input_path = input_base + "json/jawiki/jawiki.jsonl"              
elif dataset_type == "ja_law":
  if filter_type == "filter":
    hug_repo = hug_base + "ja_law_20240330_filter"
    input_path = input_base + "merge/jalaw_filter.jsonl"
  elif filter_type == "before":
    hug_repo = hug_base + "ja_law_20240330_prefilter"        
    input_path = input_base + "json/jalaw/jalaw.jsonl"            

dataset = datasets.load_dataset("json", data_files = input_path)
dataset.push_to_hub(hug_repo)