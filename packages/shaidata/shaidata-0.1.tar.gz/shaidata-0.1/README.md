Shinhan AI Data Pipeline
========================

> 신한 AI에서 수집한 각종 Data를 DW로 제공하기 위한 Framework

## 1. Commands

```commandline
python3 
```

# 2. pack env
```commandline
cd /home/kaydash/anaconda3/envs
conda install -c conda-forge conda-pack
conda pack -n pipeline -o pipeline.tar.gz
```
# 3. ingestion example
```commandline
python shaidata.py ingestion list
python shaidata.py ingestion info IGT003001
python shaidata.py ingestion update IGT002017 IGT000021_update.json
python shaidata.py ingestion add IGT000021_add.json
python shaidata.py ingestion delete IGT002017
python shaidata.py ingestion exec IGT004002
```
# 4. server example
```commandline
python shaidata.py server add server_add.json
python shaidata.py server info dac1d
```