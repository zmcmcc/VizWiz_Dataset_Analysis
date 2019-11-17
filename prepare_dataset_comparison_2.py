#This script is used to generate results for Figure 4 in our paper.
#Note: This part should be run on Python2 since the joblib file was created with support only for Python2.
import json
import joblib

#COCO-Attribute Attributes
res = {}
cocottributes = joblib.load('cocottributes_eccv_version.jbl')
attr_details = sorted(cocottributes['attributes'], key=lambda x:x['id'])
attr_names = [item['name'] for item in attr_details]

for i in range(len(cocottributes['ann_vecs'])):
	coco_attr_id = cocottributes['ann_vecs'].keys()[i]
	instance_attrs = cocottributes['ann_vecs'][coco_attr_id]
	pos_attrs = [str(a) for ind, a in enumerate(attr_names) if instance_attrs[ind] > 0.5]
	for attr in pos_attrs:
		if attr not in res:
			res[attr] = 1
		else:
			res[attr] += 1

#Save file
json.dump(res,open('results/img_num_analysis/COCO-Attribute_image_per_attribute.json','w'))