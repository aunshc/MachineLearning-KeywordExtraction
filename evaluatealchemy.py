

import pickle
import numpy as np
from keywordextraction import get_crowdd500_data,evaluate_keywords


def main():
  top_k = 15
  verbose = 1

  # load saved alchemy api responses
  alchemy_keywords = pickle.load(open('saved/alchemy_crowd500_keywords.pkl','rb'))

  # evaluate on Crowd500 test set
  testdata = get_crowdd500_data('test')
  num_docs = len(testdata['documents'])
  
  performance_data = np.zeros((num_docs,3))
  for doc_idx in xrange(num_docs):
    true_keyphrases = testdata['keywords'][doc_idx]
    
    true_keywords = []
    for phrase in true_keyphrases:
      true_keywords.extend(phrase.lower().split())

    suggested_keywords = []
    for (keyword,score) in alchemy_keywords[doc_idx]:
      suggested_keywords.extend(keyword.lower().split())

    # take top k unique keywords rather than top k keywords (alchemy ranks related phrases similarly)
    top_k_suggestions = []
    i = 0
    while (i < len(suggested_keywords)-1) and (len(top_k_suggestions) < top_k):
        if suggested_keywords[i] not in top_k_suggestions:
            top_k_suggestions.append(suggested_keywords[i])            
        i += 1

    (precision,recall,f1score) = evaluate_keywords(top_k_suggestions,true_keywords)
    performance_data[doc_idx,0] = precision
    performance_data[doc_idx,1] = recall
    performance_data[doc_idx,2] = f1score
    if verbose == 1:
      print 'Document %d of %d: f1-score for top-%d keywords extracted by model = %.4f' % (doc_idx+1,num_docs,top_k,f1score)

 

if __name__ == '__main__':
  main()