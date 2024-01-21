from textblob import TextBlob
import streamlit as stream

import pandas as pd

stream.header('Sentiment Analysis')
with stream.expander('Analze Text'):
    text = stream.text_input('Text here: ')
    if text:
        blob = TextBlob(text)
        stream.write('Polarity:',round(blob.sentiment.polarity,2))
        stream.write('subjectivity:',round(blob.sentiment.subjectivity,2))
with stream.expander('Analyze CSV'):
    upl_file = stream.file_uploader('Upload file')
    def score(x):
        blob = TextBlob(x)
        return blob.polarity