# Tokenizer
ucllm-nedo-dev配下に配置されることを想定しています。

## GCPでの実行手順
```bash
#実行環境
$ srun --gpus-per-node=0 --time=06:00:00 --nodes=1 --pty bash -i
#condaを有効化。
$ source ~/miniconda3/etc/profile.d/conda.sh
# Python仮想環境を有効化。
$ conda activate .venv_data

# トーク内座の作業ディレクトリへ移動
$ cd ~/ucllm_nedo_dev/tokenizer
```

## 1. Download datasets

### [日本語wikipedia dump](https://dumps.wikimedia.org/jawiki/)
```bash
$ python -m preprocessing.download_dataset --split=20240301 --language=ja --output_base=/persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer
```
### [英語wikipedia dump](https://dumps.wikimedia.org/enwiki/)
```bash
$ python -m preprocessing.download_dataset --split=20240301 --language=en --output_base=/persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer
```

## 2. データ整形

### 事前準備
```bash
# Python仮想環境を有効化。
$ conda deactivate
# Python仮想環境を有効化。（wikiextractorはpython3.10でしか動かない）
$ conda activate .venv
$ pip install wikiextractor
```
### 日本語
```bash
$ python -m wikiextractor.WikiExtractor -o /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/prefilter/ja/ --no-templates /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/tmp/wikipedia/20240301/ja/jawiki-20240301-pages-articles-multistream.xml.bz2
```
### 英語
```bash
$ python -m wikiextractor.WikiExtractor -o /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/prefilter/en/ --no-templates /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/tmp/wikipedia/20240301/en/enwiki-20240301-pages-articles-multistream.xml.bz2
```

## 3. jsonl作成（英語は乱択）

### 事前準備
```bash
# Python仮想環境を有効化。
$ conda deactivate
# Python仮想環境を有効化。
$ conda activate .venv_data
```
### 日本語
```bash
$ python -m preprocessing.t01_delete_spaceline \
    --language ja \
    --input_base /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/prefilter/ \
    --output_base /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/jsonl/
```
### 英語
```bash
$ python -m preprocessing.t01_delete_spaceline \
    --language en \
    --input_base /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/prefilter/ \
    --output_base /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/jsonl/
```

## 4. cleaning and text作成

```bash
$ python -m preprocessing.filtering \
    --input_dir /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/jsonl/ \
    --output_dir /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/filter/
```

## 5. 未知語の間引き（日本語のみ）

### 事前準備
```bash
pip install fugashi[unidic]
python -m  unidic download
```
### 日本語
```bash
$ python -m preprocessing.t02_mabiki \
    --input /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/filter/ja_wiki/filtering.txt \
    --output /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/text/ja_wiki_mabiki.txt
```

## 6. 分かち書き（日本語のみ）

### 日本語
```bash
$ python -m preprocessing.t03_wakachi \
    --input /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/text/ja_wiki_mabiki.txt \
    --output /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/text/jawiki_newline_mecab.txt
```

## 7. 言語ごとのトークナイズ

### 事前準備
```bash
# Python仮想環境を有効化。
$ conda deactivate
# Python仮想環境を有効化。
$ conda activate .venv
```
### 日本語
```bash
$ python -m train_tokenizer.train_sentencepiece_tokenizer \
    --input /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/text/jawiki_newline_mecab.txt \
    --model_prefix JINIAC_V0_9_ja60000 \
    --vocab_size 60000 \
    --num_threads 24 \
    --pretokenization_delimiter "||||"
```
### 英語
```bash
$ python -m train_tokenizer.train_sentencepiece_tokenizer \
    --input /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/filter/en_wiki/filtering.txt \
    --model_prefix JINIAC_V0_9_en13000 \
    --vocab_size 13000 \
    --num_threads 24 \
    --max_sentencepiece_length 16
```

## 8. prefixと重複の削除

### 日本語
```bash
$ python train_tokenizer/specialSymbolRemove.py \
    JINIAC_V0_9_ja60000.vocab > JINIAC_V0_9_ja60000.vocab.symbolRemoved
```
### 英語
```bash
$ python train_tokenizer/specialSymbolRemove4symbols.py \
    JINIAC_V0_9_en13000.vocab > JINIAC_V0_9_en13000.vocab.symbolRemoved
```

## 9. 日英データマージ

### 事前準備
```bash
# llm-jp-tokenizerのclone
$ git clone https://github.com/llm-jp/llm-jp-tokenizer.git
```
### 処理
```bash
$ python llm-jp-tokenizer/scripts/mergeVocab.py \
    llm-jp-tokenizer/models/ver2.1/specialTokens.vocab \
    JINIAC_V0_9_ja60000.vocab.symbolRemoved \
    JINIAC_V0_9_en13000.vocab.symbolRemoved > JINIAC_V0_9_ja42K_en13K.merged.vocab
```

## 10. 再推定

### 事前準備
```bash
# llm-jp-tokenizerのclone
$ cd llm-jp-tokenizer/scripts
$ git clone https://github.com/tatHi/multigram.git
$ pip install scipy numba
```
### 処理
```bash
$ cat /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/text/ja_wiki_mabiki.txt \
    /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/filter/en_wiki/filtering.txt > /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/text/merged.txt
$ python reestimateScore.py \
    --vocab /home/ext_u10bei_github_io_gmail_com/ucllm_nedo_dev/tokenizer/JINIAC_V0_9_ja42K_en13K.merged.vocab \
    --data /persistentshare/storage/team_nakamura/member/horie/dataset/tokenizer/text/merged.txt \
    --output /home/ext_u10bei_github_io_gmail_com/ucllm_nedo_dev/tokenizer/JINIAC_V0_9.vocab \
    --trainingMode EM \
    --maxEpoch 2