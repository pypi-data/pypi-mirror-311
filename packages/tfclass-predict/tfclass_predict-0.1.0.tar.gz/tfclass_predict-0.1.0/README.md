# TFClass Predict 

## Description

tfclass_predict can be used to predict transcription factor binding sites in ATAC-seq data on TFClass level using DNABERT.

## Package Workflow Structure

<div style="text-align:center">
<img src="https://gitlab.gwdg.de/hti/tfclass_dnabert/-/raw/main/workflow_schema.drawio.png" alt="./workflow_schema.drawio.png">
</div>

## Installation

Currently, only a pre-alpha version of the package is available. The package can be installed via pip: 
```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple tfclass-predict
```

To use the package the human genome (v38) and the DNABERT model (v1-06) are needed.

[DNABERT6](https://drive.google.com/file/d/1BJjqb5Dl2lNMg2warsFQ0-Xvn1xxfFXC/view) by jerryji1993

[HG38](http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz) from UCSC

Both downloads need to be **unzipped** so that the path to ```hg38.fa``` and 
the path to the directory ```6-new-12w-0``` can be passed to the command-line tool or ```PredictionManager```.

## Models

TFClass Predict currently allows to use only one hierarchy level (the class-level). The corresponding model needs to be downloaded in order to use the tool. 

[Classlevel](https://owncloud.gwdg.de/index.php/s/CqAl9Wex5tvVByO)

## Usage
The tool can be used from the command line with the following parameters:
```
usage: tfclass_predict [-h] bed_file hg_file tfclass_model dnabert output_dir

tfclass_predict allows to estimate transcription factor bindingsites in the TFClass hierarchy.

positional arguments:
  bed_file       Path to bed file of ATAC-seq or other NGS experiment.
  hg_file        Path to human genome reference (.fa).
  tfclass_model  Path to TFClass model (.h5).
  dnabert        Path to DNABERT model directory.
  output_dir     Path to output directory.

options:
  -h, --help     show this help message and exit   
```
Or directly in python scripts: 
```python
from tfclass_predict import PredictionManager

bed_file = 'tests/GSM6915056_P1_summits_100.bed'  # smaller bed file for testing
genome_file = "hg38.fa"
tfclass_model = "model/Classlevel.h5" #see Installation
bert_model = "model/6-new-12w-0" #see Intallation
res_dir = "tests/res"

pred_manager = PredictionManager(bed_file, genome_file, res_dir, bert_model, tfclass_model)
pred_manager.predict()
pred_manager.save_results()
```

## Further Documentation
Find more infromation about the API at [ReadTheDocs](https://tfclass-predict.readthedocs.io/en/v0.0.4/).


## Docker Image (under construction)
Includes the Dockerfile to install Docker.
**Go into the docker directory and run:**\
docker build -t "username_name_of_the_image" .  
  
**How to use the docker image?**\
docker run -it -u 2696:205 --gpus '"device=0,1,2,3,4,5,6,7"' -v /scratch/docker_hti/MultiModel_160523/:/AI_PLATFORM/ --rm --name hti hti_tfplatform:1.1\

Please change the -u or user id to your own. You can find your own user id by checking  "id -u <username>" form the terminal.
Specify the gpu devices you want to use and modify the scratch directory to where you have the files downloaded. Of course, also change the "hti" to your own username.
