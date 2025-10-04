import numpy as np
from nltk.stem import  WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.porter import *

stopwords = stopwords.words('english')
stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()


def remove_stopwords(text):
    clean_text = ' '.join([word for word in text.split() if word not in stopwords])
    return clean_text


def get_unique_words(text):
    clean_text = ' '.join(set(text.split()))
    return clean_text


def pre_process(df, ENGINE_TYPE):
    df_copy = df.copy()

    df_copy = df_copy.replace(np.nan, '', regex=True)
    df_copy['curated_text'] = df_copy[ENGINE_TYPE].apply(lambda x: ', '.join(x.astype(str)), axis=1)
    df_copy['curated_text'] = df_copy['curated_text'].str.lower().replace('[^a-zA-Z]', ' ', regex=True)
    df_copy['curated_text'] = df_copy['curated_text'].apply(lambda text:get_unique_words(text))
    df_copy['curated_text'] = df_copy['curated_text'].apply(lambda text: remove_stopwords(text))
    df_copy['curated_text'] = df_copy['curated_text'].apply(lambda x: x.split())
    df_copy['curated_text'] = df_copy['curated_text'].apply(lambda x: [lemmatiser.lemmatize(i) for i in x])
    df_copy['curated_text'] = df_copy['curated_text'].apply(lambda x: ' '.join([w for w in x]))

    return df_copy


def preprocess_string(a):
    if len(max(a.split(' '), key=len)) == 1:
        str_a = ''.join(a.split(' '))

    else:
        str_a = a
    return str_a

