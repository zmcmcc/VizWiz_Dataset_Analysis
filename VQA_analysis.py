#This script is used to generate part of the results for Table 2 in our paper.
import json
import pandas as pd

data_vqa_v2_val = json.load(open('annotations/VizWiz/VizWiz_VQA_v2_val.json'))
data_vqa_v2_train = json.load(open('annotations/VizWiz/VizWiz_VQA_v2_train.json'))

question_answers = []
for data in [data_vqa_v2_train,data_vqa_v2_val]:
	for img in data:
		temp = {}
		if 'answerable' in img:
			if img['answerable'] == 1:
				temp['image_id'] = int(img['image'].split('_')[-1].split('.')[0])
				temp['question'] = img['question']
				ans_list = {}
				for ans in img['answers']:
					if ans['answer_confidence'] == 'yes':
						if ans['answer'] not in ans_list:
							ans_list[ans['answer']] = 1
						else:
							ans_list[ans['answer']] += 1
				temp['answer'] = sorted(ans_list.items(),key=lambda x:x[1],reverse=True)[0][0]
				question_answers.append(temp)

			else:
				temp['image_id'] = int(img['image'].split('_')[-1].split('.')[0])
				temp['question'] = img['question']
				temp['answer'] = 'unanswerable'
				question_answers.append(temp)
				
		else:
			count_yes = 0
			for ans in img['answers']:
				if ans['answer_confidence'] == 'yes':
					count_yes += 1
			if count_yes >= 5:
				ans_list = {}
				for ans in img['answers']:
					if ans['answer_confidence'] == 'yes':
						if ans['answer'] not in ans_list:
							ans_list[ans['answer']] = 1
						else:
							ans_list[ans['answer']] += 1
				most_answer = sorted(ans_list.items(),key=lambda x:x[1],reverse=True)[0][0]
				if most_answer != 'unanswerable':
					temp = {}
					temp['image_id'] = int(img['image'].split('_')[-1].split('.')[0])
					temp['question'] = img['question']
					temp['answer'] = most_answer
					question_answers.append(temp)

json.dump(question_answers,open('results/VQA/VizWiz_VQA_v2_popular_answers.json','w'))


vqa_img_list = [vqa['image_id'] for vqa in question_answers]
cap_train = json.load(open('annotations/VizWiz/VizWiz_Captions_v1_train_updated.json'))['annotations']
cap_val = json.load(open('annotations/VizWiz/VizWiz_Captions_v1_val_updated.json'))['annotations']
img_train = json.load(open('annotations/VizWiz/VizWiz_Captions_v1_train_updated.json'))['images']
img_val = json.load(open('annotations/VizWiz/VizWiz_Captions_v1_val_updated.json'))['images']
cap_img_list = [cap['id'] for cap in (img_train+img_val)]
common_ids = [w for w in vqa_img_list if w in cap_img_list]

caps = pd.DataFrame(cap_train+cap_val).groupby('image_id')['caption'].apply(list)

count = 0
for quest in question_answers:
	img_id = quest['image_id']
	answer = quest['answer'].lower()
	if img_id in cap_img_list:
		captions = caps[img_id]
		for cap in captions:
			if (len(answer.split()) >1 and answer in cap.lower()) or (len(answer.split())==1 and answer in cap.lower().split()):
				count += 1
				break

print('There are {} images contained in both the VQA dataset and the caption dataset.'.format(len(common_ids)))
print('There are',count,'images which have at least one caption containing the answer to the question.')

count_yesno_vqa = 0
count_yesno_cap = 0
for quest in question_answers:
	img_id = quest['image_id']
	question = quest['question'].lower()
	answer = quest['answer'].lower()
	
	unsuitabale_dict = ['what','who','which','or','how much','how']
	suitable_dict = ['is there','are there','is this','are they','are these','it is','is it','there is','there are','this is','is that','it is','there is','there are','this is','they are','these are','that is']
	if not any(w in question for w in unsuitabale_dict) and len(question.split()) > 2:
		if answer == 'yes' or answer == 'no':
			count_yesno_vqa += 1
			if img_id in cap_img_list:
				captions = caps[img_id]
				for cap in captions:
					if answer in cap.lower().split():
						count_yesno_cap += 1
						break
print('There are',count_yesno_cap,'out of',count_yesno_vqa,'images which have at least one caption containing the yes/no answer to the question.')

count_counting_vqa = 0
count_counting_cap = 0
for quest in question_answers:
	img_id = quest['image_id']
	question = quest['question'].lower()
	answer = quest['answer'].lower()
	
	unsuitabale_dict = ['what','who','which','or','how']
	suitable_dict = ['how many','how much']
	if  len(question.split()) > 2:
		if any(w in question for w in suitable_dict):
			count_counting_vqa += 1
			if img_id in cap_img_list:
				captions = caps[img_id]
				for cap in captions:
					if answer in cap.lower().split():
						count_counting_cap += 1
						break
print('There are',count_counting_cap,'out of',count_counting_vqa,'images which have at least one caption containing the counting answer to the question.')