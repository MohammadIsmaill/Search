from sentence_transformers import SentenceTransformer
import faiss
from spellchecker import SpellChecker
import numpy as np
import pandas as pd
import torch

model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3')
index = faiss.read_index("prod_dec.index")


df = pd.read_csv('products.csv')

def fetch_product_info(dataframe_idx):
    info = df[df['id']==dataframe_idx]
    meta_dict = dict()
    meta_dict['name'] = info['name']
    meta_dict['description'] = info['description'][:500]
    return meta_dict
    
def search(query, top_k=100, index=index, model=model):
    spell = SpellChecker()
    query_initial=query.split()
    query_corrected=[spell.correction(word) for word in query_initial]
    query=" ".join(query_corrected)
    query_vector = model.encode([query])
    top_k = index.search(query_vector, top_k)
    top_k_ids = top_k[1].tolist()[0]
    top_k_ids = list(np.unique(top_k_ids))
    results =  [fetch_product_info(idx) for idx in top_k_ids]
    # for result in results:
    # print(result)
    return results
