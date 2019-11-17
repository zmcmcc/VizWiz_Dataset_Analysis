#This script is used to generate part of the results for Table 1 in our paper.
import json
import pandas as pd
import json
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords

#If error occurs about the nltk package, try to uncomment the following lines.
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

#read all colors of XKCD https://xkcd.com/color/rgb.txt
color_list = []
with open('tools/colors.txt') as color_file:
	for line in color_file:
		color_list.append(line.strip().split('\t')[0])

#If you want to use stop words, uncomment the following.
'''
stop_words = set(stopwords.words('english')) 
spa_rel_list = ['above','accross','along','among','around','at','before','behind','below','beneath','beside','between','beyond','by','down','from','in','near','of','on','through','to','with']
for spa in spa_rel_list:
	if spa in stop_words:
		stop_words.remove(spa)
'''
stop_words = []

#1. MSCOCO-ALL
def generate_description_analysis_mscoco_all():   
	res = {}
	res['Word'] = 0
	res['Noun'] = 0
	res['Verb'] = 0
	res['Color'] = 0
	res['Spatial_Relation'] = 0
	res['Adj'] = 0
	 
	data_train = json.load(open('annotations/MSCOCO/captions_train2017.json'))
	data_val = json.load(open('annotations/MSCOCO/captions_val2017.json')) 

	ann_train = data_train['annotations']
	ann_val = data_val['annotations']
	ann = pd.DataFrame(ann_train+ann_val)
	
	for i in range(len(ann)):
		question = ann['caption'][i].lower()
		image_id = ann['image_id'][i]
		
		word_tokens = nltk.word_tokenize(question.lower()) 
		words = [w for w in word_tokens if not w in stop_words]
		#numWords = len(set(words))

		for word in words:
			if word in color_list:
				res['Color'] += 1

		# https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
		partsOfSpeechTags = nltk.pos_tag(words)
		partsOfSpeech = [wordResult[1] for wordResult in partsOfSpeechTags]
		tag_fd = nltk.FreqDist(partsOfSpeech)

		res['Noun'] += tag_fd['NN'] #noun, singular 'desk'
		res['Noun'] += tag_fd['NNS']  #noun plural	'desks'

		res['Spatial_Relation'] += tag_fd['IN']#preposition/subordinating conjunction
 
		res['Adj'] += tag_fd['JJ'] #adjective	'big'
		res['Adj'] += tag_fd['JJR']# bigger
		res['Adj'] += tag_fd['JJS']#biggest

		res['Verb'] += tag_fd['VB']#verb do
		res['Verb'] += tag_fd['VBD']#verb did
		res['Verb'] += tag_fd['VBG']#doing
		res['Verb'] += tag_fd['VBZ']#done

		res['Word'] += len(words)
			
	length = len(ann)
	res['Word'] = res['Word']/length
	res['Noun'] = res['Noun']/length
	res['Verb'] = res['Verb']/length
	res['Color'] = res['Color']/length
	res['Adj'] = res['Adj']/length
	res['Spatial_Relation'] = res['Spatial_Relation']/length
	
	json.dump(res, open('results/description_analysis/MSCOCO_description_word_result_per_image_all.json', 'w'))


def unique_count_mscoco_all():
	res_uni = {}
	res_uni['Word'] = 0
	res_uni['Noun'] = 0
	res_uni['Adj'] = 0
	res_uni['Verb'] = 0
	res_uni['Spatial_Relation'] = 0
	res_uni['2-Gram'] = 0
	res_uni['3-Gram'] = 0
	
	word_uni = set()
	noun_uni = set()
	adj_uni = set()
	verb_uni = set()
	spa_rel_uni = set()
	two_gram_uni = set()
	three_gram_uni = set()

	data_train = json.load(open('annotations/MSCOCO/captions_train2017.json'))
	data_val = json.load(open('annotations/MSCOCO/captions_val2017.json'))

	ann_train = data_train['annotations']
	ann_val = data_val['annotations']
	ann = pd.DataFrame(ann_train+ann_val)
	
	for i in range(len(ann)):
		question = ann['caption'][i].lower()
		word_tokens = nltk.word_tokenize(question) 
		words = [w for w in word_tokens if not w in stop_words]
		
		partsOfSpeechTags = nltk.pos_tag(words)
		partsOfSpeech = [wordResult[1] for wordResult in partsOfSpeechTags]
		
		for i,pos in enumerate(partsOfSpeech):
			if pos == 'JJ' or pos == 'JJR' or pos == 'JJS':
				adj_uni.add(partsOfSpeechTags[i][0])
			if pos == 'NN' or pos == 'NNS':
				noun_uni.add(partsOfSpeechTags[i][0])
			if pos == 'VB' or pos == 'VBG' or pos == 'VBD' or pos == 'VBZ':
				verb_uni.add(partsOfSpeechTags[i][0])
			if pos == 'IN':
				spa_rel_uni.add(partsOfSpeechTags[i][0])
				
		bgs = nltk.ngrams(words,2)
		tgs = nltk.ngrams(words,3)
		fdist = nltk.FreqDist(bgs)
		fdist3 = nltk.FreqDist(tgs)
		for k,v in fdist.items():
			two_gram_uni.add(k)
		for k,v in fdist3.items():
			three_gram_uni.add(k)
		for word in words:
			word_uni.add(word)        
			
	res_uni['Noun'] = len(noun_uni)
	res_uni['Adj'] = len(adj_uni)
	res_uni['Verb'] = len(verb_uni)
	res_uni['Spatial_Relation'] = len(spa_rel_uni)
	res_uni['Word'] = len(word_uni)
	res_uni['2-Gram'] = len(two_gram_uni)
	res_uni['3-Gram'] = len(three_gram_uni)
			
	json.dump(res_uni, open('results/description_analysis/MSCOCO_description_word_result_unique_all.json', 'w'))


generate_description_analysis_mscoco_all()
unique_count_mscoco_all()