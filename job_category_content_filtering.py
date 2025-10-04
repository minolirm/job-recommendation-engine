import spacy
from sklearn.feature_extraction.text import CountVectorizer

from preprocess import preprocess_string
from config import JOB_CATEGORY_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT,JOB_CATEGORY_RECOMMENDER_THRESHOLD_FOR_APPLICANT


nlp = spacy.load("en_core_web_lg")
vectorizer = CountVectorizer()


def match_ap_job_category_for_advertisement(advertisement_df, applicant_df):
    sim_score_list = []
    app_recommender_dict = {}
    app_list = applicant_df['_id'].tolist()

    adv_job_category_set = preprocess_string(str(advertisement_df['job_category'][0]))
    sent_1 = nlp(adv_job_category_set)

    for row_idx, row in applicant_df.iterrows():
        app_job_category_set = preprocess_string(str(row['interested_industries']))

        app_job_category = app_job_category_set.split(',')
        if adv_job_category_set in app_job_category:
            app_job_category = adv_job_category_set
        else:
            app_job_category = app_job_category_set
        sent_2 = nlp(app_job_category)
        similarity = sent_1.similarity(sent_2)
        sim_score_list.append(similarity)

    app_score_dict = dict(zip(app_list,sim_score_list))
    for k, v in app_score_dict.items():
        if float(v) > JOB_CATEGORY_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT:
            app_recommender_dict[k] = v
        else:
            pass

    return app_score_dict,app_recommender_dict


def match_ad_job_category_for_applicant(applicant_df, advertisement_df):
    sim_score_list = []
    adv_jc_recommender_dict = {}
    adv_list = advertisement_df['_id'].tolist()

    app_skills_set = preprocess_string(str(applicant_df['interested_industries'][0]))
    sent_1 = nlp(app_skills_set)

    for row_idx,row in advertisement_df.iterrows():
        adv_skills_set = preprocess_string(str(row['job_category'])).replace(',',' ')
        sent_2 = nlp(adv_skills_set)
        similarity = sent_1.similarity(sent_2)
        sim_score_list.append(similarity)

    adv_jc_score_dict = dict(zip(adv_list,sim_score_list))
    for k, v in adv_jc_score_dict.items():
        if float(v) > JOB_CATEGORY_RECOMMENDER_THRESHOLD_FOR_APPLICANT:
            adv_jc_recommender_dict[k] = v
        else:
            pass

    return adv_jc_score_dict,adv_jc_recommender_dict