# VizWiz_Dataset_Analysis
### Author: Meng Zhang Email: mengzhang@utexas.edu
This repository is part of the codes for our paper 


## 1. Download raw dataset files
Due to the maximum file size limitation of GitHub, not all of the dataset files needed are included.
* Download captions_train2017.json, captions_val2017.json, and instances_train2017.json on http://cocodataset.org/#download. Put the first two files at annotations/MSCOCO (you need to create a folder named 'MSCOCO'), and put the last file at annotations/Objects.
* Download train_places205.csv and val_places205.csv on http://data.csail.mit.edu/places/places205/trainvalsplit_places205.tar.gz. Put them at annotations/Scenes.

## 2. Create results folders
GitHub ignores empty folders when uploading files, so please create a folder named 'results', and create three folders in this folder named 'description_analysis', 'img_num_analysis' and 'VQA'. 
Alternatively, you can modify the locations of result files in the codes.

## 3. Run the codes
* Run prepare_dataset_comparison.py and prepare_dataset_comparison_2.py (must in Python 2), and then see compare_datasets.ipynb to reproduce the result of Figure 2 in our paper.
* Run description_analysis_mscoco.py to reproduce some of the results of Table 1 in our paper. The numbers may slightly differ from printed in our paper due to NLTK's features.
* Run VQA_analysis.py to reproduce the result of Table 3 in our paper.
