from transformers import pipeline
import pandas as pd

from flask import g, session

def init_pipeline():
    if 'pipe' not in g:
        g.pipe = pipeline("table-question-answering", model="google/tapas-base-finetuned-sqa")

def queryable_data(data):
    table = pd.DataFrame.from_dict(data)
    g.table = table.astype(str)
    
def query(question):
    if 'pipe' not in g:
        init_pipeline()
    table = pd.DataFrame.from_dict(session['filedata'])
    answer = g.pipe(query=question,table=table)
    return answer['answer']
