from config import AP_ENGINE, AD_ENGINE
from pre_processor import primary_pre_process
from sklearn.feature_extraction.text import CountVectorizer
from similarity_measure import jaccard_similarity

""""Pass one advertisement to match with multiple applicants"""
vectorizer = CountVectorizer()


def calculate_primary_sim_for_adv(ap_df, ad_df):
    score_list = []
    id_list = ap_df["_id"].tolist()
    pre_ap_df = primary_pre_process(ap_df, AP_ENGINE["primary"])
    pre_ad_df = primary_pre_process(ad_df, AD_ENGINE["primary"])
    ap_text = pre_ap_df["curated_text"]
    ad_text = pre_ad_df['curated_text'][0]

    ad_word_set = ad_text.split()
    for ap_idx,ap in pre_ap_df.iterrows():
        ap_word_set = ap_text[ap_idx].split()
        similarity = jaccard_similarity(ad_word_set,ap_word_set)*100
        score_list.append(similarity)

    pri_score_dict = dict(zip(id_list,score_list))
    return pri_score_dict


""""Pass one applicant to match with multiple advertisements"""


def calculate_primary_sim_for_app(ap_df, ad_df):
    score_list = []
    id_list = ad_df["_id"].tolist()

    pre_ap_df = primary_pre_process(ap_df, AP_ENGINE["primary"])
    pre_ad_df = primary_pre_process(ad_df, AD_ENGINE["primary"])
    ap_text = pre_ap_df["curated_text"][0]
    ad_text = pre_ad_df['curated_text']

    ap_word_set = ap_text.split()
    for ad_idx,ad in pre_ad_df.iterrows():
        ad_word_set = ad_text[ad_idx].split()
        similarity = jaccard_similarity(ap_word_set,ad_word_set)*100
        score_list.append(similarity)

    pri_score_dict = dict(zip(id_list, score_list))
    return pri_score_dict



