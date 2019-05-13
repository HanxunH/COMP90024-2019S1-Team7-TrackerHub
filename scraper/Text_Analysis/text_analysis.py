from keywords import NOUN, VERB, ADJ
import nltk
nltk.download('punkt')
nltk.download('wordnet')
import re
from profanity import profanity
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob 


def getScore(synset, w, num, string):

	score = synset.wup_similarity(wn.synset( w + "." + string +".01"))
	lst = [score,num]
	return max(lst)


def lust_similarity_check(maxval, synset, string):

	num = maxval

	if string == "n":

		for w in NOUN:
			if num < getScore(synset, w, num, string):
				num = getScore(synset, w, num, string)


	elif string == "v":

		for w in VERB:
			if num < getScore(synset, w, num, string):
				num = getScore(synset, w, num, string)

	elif string == "a":

		for w in ADJ:
			if num < getScore(synset, w, num, string):
				num = getScore(synset, w, num, string)

	return num


# check if the word is relevant to lust
def check_lust(word):
	maxval_n= 0 
	maxval_v= 0
	maxval_a= 0 
	lemmatizer = WordNetLemmatizer()
	word_n = lemmatizer.lemmatize(word, 'n')
	for synset in wn.synsets(word_n,'n'):
		maxval_n= lust_similarity_check(maxval_n, synset, "n")

	
	word_v = lemmatizer.lemmatize(word, 'v')
	for synset in wn.synsets(word_v, 'v'):
		maxval_v= lust_similarity_check(maxval_v, synset, "v")

	word_a = lemmatizer.lemmatize(word, 's')
	for synset in wn.synsets(word_a, 's'):
		maxval_a= lust_similarity_check(maxval_a, synset, "s")

	temp = [maxval_n, maxval_v, maxval_a]
	return max(temp)


def lust_analysis(text):
	text = re.sub('([#])|([^a-zA-Z])',' ',text )
	tokens = nltk.word_tokenize(text.lower())
	rating=0.0
	for token in tokens:
		if rating <check_lust(token):
			rating=check_lust(token)

	if rating>0.8:
		return 1
	else:
		return 0


# check if the sentence have a profanity word.
def profanity_analysis(text):
	text = re.sub('([#])|([^a-zA-Z])',' ',text )
	tokens=nltk.word_tokenize(text.lower())
	contain_profanity=profanity.contains_profanity(text)
	return contain_profanity


def sentiment_analysis(text):
	text = re.sub('([#])|([^a-zA-Z])',' ',text )
	analysis = TextBlob(text)
	# set sentiment 
	if analysis.sentiment.polarity > 0: 
		return 'positive'

	elif analysis.sentiment.polarity == 0: 
		return 'neutral'

	else:
		return 'negative'


























