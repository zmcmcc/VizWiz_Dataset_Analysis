#This script is used to generate results for Figure 4 in our paper.

import json
import pandas as pd
import numpy as np
from scipy.io import loadmat
import requests
import nltk
from nltk.corpus import stopwords


#MSCOCO Objects
data = json.load(open('annotations/Objects/instances_train2017.json'))
cats = pd.DataFrame(data['categories'])
num_ann = len(data['annotations'])
res = {}

for i in range(0,num_ann,5):
	cat_id = data['annotations'][i]['category_id']
	cat_name = cats[cats.id == cat_id]['name'].values[0]
	if cat_name not in res.keys():
		res[cat_name] = 1
	else:
		res[cat_name] += 1

json.dump(res,open('results/img_num_analysis/MSCOCO_image_per_object.json','w'))


#ImageNet Objects
data = pd.read_csv('annotations/Objects/LOC_train_solution.csv')
with open('annotations/Objects/LOC_synset_mapping.txt') as f:
	id_map_list = f.readlines()
cat_names = [' '.join(row.split()[1:]).lower() for row in id_map_list]
cat_ids = [row.split()[0] for row in id_map_list]
id_name_map = {}
res = {}

for name,id in zip(cat_names,cat_ids):
	id_name_map[id] = name
img_ids = list(data['ImageId'])

for img in img_ids:
	img_id = img.split('_')[0]
	cat_name = id_name_map[img_id]
	if cat_name not in res:
		res[cat_name] = 1
	else:
		res[cat_name] += 1

json.dump(res,open('results/img_num_analysis/ImageNet_image_per_object.json','w'))


#Place-205 Scenes
place_train = pd.read_csv('annotations/Scenes/train_places205.csv',header=None)
place_val = pd.read_csv('annotations/Scenes/val_places205.csv',header=None)
place_205 = {}

for i in range(len(place_train)):
	cat = place_train.iloc[i,0].split('/')[1]
	if cat in place_205:
		place_205[cat] += 1
	else:
		place_205[cat] = 1

for i in range(len(place_val)):
	cat = place_train.iloc[i,0].split('/')[1]
	if cat in place_205:
		place_205[cat] += 1
	else:
		place_205[cat] = 1

json.dump(place_205,open('results/img_num_analysis/Place-205_image_per_scene.json','w'))


#Sun Scenes
res = {}
with open('annotations/Scenes/Sun-scenes.txt') as f:
	data = f.readlines()

for d in data:
	cat_name = d.split('(')[0][:-1].strip().lower()
	cat_num = d.split('(')[1].split(')')[0]
	res[cat_name] = int(cat_num)

json.dump(res,open('results/img_num_analysis/Sun_image_per_scene.json','w'))


#Sun-attribute attributes
attributes = list(loadmat('annotations/Attributes/attributes.mat')['attributes'])
imgs = list(loadmat('annotations/Attributes/attributeLabels_continuous.mat')['labels_cv'])
res = {}

for score_array in imgs:
	attr_ids = np.where(score_array>=0.5)[0].tolist()
	for attr in attr_ids:
		attr_name = attributes[attr][0][0]
		if attr_name not in res:
			res[attr_name] = 1
		else:
			res[attr_name] += 1

json.dump(res,open('results/img_num_analysis/Sun-attribute_image_per_attribute.json','w'))


