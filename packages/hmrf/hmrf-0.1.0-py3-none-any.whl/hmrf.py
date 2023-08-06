import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.multiclass import unique_labels
import pandas as pd
import nltk
from scipy.stats import hmean
from nltk.corpus import stopwords
from scipy.stats import norm
import  math
from sklearn.preprocessing import LabelEncoder
from iso639 import Lang as LangIso


class Hmrf():
	def __init__(self, lang='english', positive_class=1, n=50, phrases=False, n_phrases=20, phrases_by='PMI'):
		self.lang = lang
		self.positive_class = positive_class
		self.n = n
		self.phrases = phrases
		self.n_phrases = n_phrases
		self.phrases_by = phrases_by

	def get_phrases(self, data, labels, kw_list):
		text = ' '.join([t.strip() for i,t in enumerate(data) if labels[i] == 1])
		tokens = nltk.wordpunct_tokenize(text)

		bigrams_measure = nltk.collocations.BigramAssocMeasures()
		trigrams_measure = nltk.collocations.TrigramAssocMeasures()

		bigramFinder = nltk.collocations.BigramCollocationFinder.from_words(tokens)
		bigramFinder.apply_word_filter(lambda w: w not in kw_list or w.lower() in stopwords.words(self.lang))
		trigramFinder = nltk.collocations.TrigramCollocationFinder.from_words(tokens)
		trigramFinder.apply_word_filter(lambda w: w not in kw_list or w.lower() in stopwords.words(self.lang))

		if not (len(bigramFinder.ngram_fd.items()) and len(trigramFinder.ngram_fd.items())):
			return kw_list

		if self.phrases_by == 'Freq':
			bigram_freq = bigramFinder.ngram_fd.items()
			bigrams = pd.DataFrame(list(bigram_freq), columns=['bigram','freq']).sort_values(by='freq', ascending=False)
			trigram_freq = trigramFinder.ngram_fd.items()
			trigrams = pd.DataFrame(list(trigram_freq), columns=['trigram','freq']).sort_values(by='freq', ascending=False)
		elif self.phrases_by == 'PMI':
			bigrams = pd.DataFrame(list(bigramFinder.score_ngrams(bigrams_measure.pmi)), columns=['bigram','PMI']).sort_values(by='PMI', ascending=False)
			trigrams = pd.DataFrame(list(trigramFinder.score_ngrams(trigrams_measure.pmi)), columns=['trigram','PMI']).sort_values(by='PMI', ascending=False)
		elif self.phrases_by == 'TTEST':
			bigrams = pd.DataFrame(list(bigramFinder.score_ngrams(bigrams_measure.student_t)), columns=['bigram','t']).sort_values(by='t', ascending=False)
			trigrams = pd.DataFrame(list(trigramFinder.score_ngrams(trigrams_measure.student_t)), columns=['trigram','t']).sort_values(by='t', ascending=False)
		elif self.phrases_by == 'CHI':
			bigrams = pd.DataFrame(list(bigramFinder.score_ngrams(bigrams_measure.chi_sq)), columns=['bigram','chi']).sort_values(by='chi', ascending=False)
			trigrams = pd.DataFrame(list(trigramFinder.score_ngrams(trigrams_measure.chi_sq)), columns=['trigram','chi']).sort_values(by='chi', ascending=False)

		if not bigrams.empty: bigrams = [bi[0]+' '+bi[1] for bi in bigrams['bigram']]
		if not trigrams.empty: trigrams = [tri[0]+' '+tri[1]+' '+tri[2] for tri in trigrams['trigram']]

		cant_bi = len(bigrams)
		cant_tri = len(trigrams)

		if len(bigrams) != 0 and len(trigrams) != 0:
			cant_bi = min(cant_bi, int(self.n_phrases/(1 + cant_tri/cant_bi)))
			cant_tri = min(cant_tri, self.n_phrases - cant_bi)

		bigrams = bigrams[:cant_bi]
		trigrams = trigrams[:cant_tri]
		kw_list.extend(bigrams)
		kw_list.extend(trigrams)

		return kw_list


	def normcdf(self, x):
		return norm.cdf(x, x.mean(), x.std())

	def hmrf(self, texts, labels):
	
		le = LabelEncoder()
		le.fit(labels)
		labels = le.transform(labels)
		self.positive_class = le.transform([self.positive_class])[0]
	
		labels = np.array(labels)
		labels=labels.astype('int')
		cvec = CountVectorizer()
		document_matrix = cvec.fit_transform(texts)
		ulabels = unique_labels(labels)
		cant_labels = []
		for ul in ulabels:
			cant_labels.append(np.sum(document_matrix[np.where(labels == ul)[0]].toarray(),axis=0))

		term_freq_df = pd.DataFrame(cant_labels,columns=cvec.get_feature_names()).transpose()
		
		total = term_freq_df.sum(axis=1)

		for ul in ulabels:	
			term_freq_df['freq_'+str(ul)]=term_freq_df[ul]*1.
			term_freq_df['rate_'+str(ul)]=term_freq_df[ul]*1./total
			term_freq_df['rate_pct_'+str(ul)]=term_freq_df[ul]*1./term_freq_df['rate_'+str(ul)].sum()
			term_freq_df['rate_normcdf_'+str(ul)] = self.normcdf(term_freq_df['rate_'+str(ul)])
			term_freq_df['rate_pct_normcdf_'+str(ul)] = self.normcdf(term_freq_df['rate_pct_'+str(ul)])
			try: 
				term_freq_df['normcdf_hmean_'+str(ul)] = hmean([term_freq_df['rate_normcdf_'+str(ul)], term_freq_df['rate_pct_normcdf_'+str(ul)]])
			except:
				arr = [term_freq_df['rate_normcdf_'+str(ul)], term_freq_df['rate_pct_normcdf_'+str(ul)]]
				term_freq_df['normcdf_hmean_'+str(ul)] = len(arr) / np.sum(1.0/np.array(arr)) 
				for i,elem in enumerate(term_freq_df['normcdf_hmean_'+str(ul)]):
					if math.isnan(float(elem)):
						term_freq_df['normcdf_hmean_'+str(ul)][i] = 0

		lists_keywords = []
		words_sorted = list(term_freq_df.sort_values(by=f'normcdf_hmean_{self.positive_class}', ascending=False).index)
		for i, tok in enumerate(words_sorted):
			langIso = self.lang[0].upper()+self.lang[1:]
			langIso = LangIso(langIso).pt3
			if nltk.pos_tag([tok], lang = langIso)[0][1] in ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS'] and tok not in stopwords.words(self.lang):
				lists_keywords.append(tok)
			if len(lists_keywords) == self.n: break

		if self.phrases:
			lists_keywords = self.get_phrases(texts, labels, lists_keywords)

		return lists_keywords


