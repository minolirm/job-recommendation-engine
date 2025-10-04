import spacy
from sklearn.feature_extraction.text import CountVectorizer
from config import JOB_POSITION_RECOMMENDER_THRESHOLD_FOR_APPLICANT,JOB_POSITION_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT
from preprocess import preprocess_string

nlp = spacy.load("en_core_web_lg")
vectorizer = CountVectorizer()


def match_ap_job_position_for_advertisement(advertisement_df, applicant_df):
    sim_score_list = []
    app_recommender_dict = {}
    app_list = applicant_df['_id'].tolist()

    adv_job_position_set = preprocess_string(str(advertisement_df['position'][0]))
    sent_1 = nlp(adv_job_position_set)

    for row_idx, row in applicant_df.iterrows():
        app_job_positions_set = preprocess_string(str(row['interested_job_positions']))

        app_job_position = app_job_positions_set.split(',')
        if adv_job_position_set in app_job_position:
            app_job_position = adv_job_position_set
        else:
            app_job_position = app_job_positions_set
        sent_2 = nlp(app_job_position)
        similarity = sent_1.similarity(sent_2)
        sim_score_list.append(similarity)

    app_score_dict = dict(zip(app_list,sim_score_list))
    for k, v in app_score_dict.items():
        if float(v) > JOB_POSITION_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT:
            app_recommender_dict[k] = v
        else:
            pass

    return app_score_dict,app_recommender_dict


def match_ad_job_positions_for_applicant(applicant_df, advertisement_df):
    sim_score_list = []
    adv_jp_recommender_dict = {}
    adv_list = advertisement_df['_id'].tolist()

    app_skills_set = preprocess_string(str(applicant_df['interested_job_positions'][0]))
    sent_1 = nlp(app_skills_set)

    for row_idx,row in advertisement_df.iterrows():
        adv_skills_set = preprocess_string(str(row['position'])).replace(',',' ')
        sent_2 = nlp(adv_skills_set)
        similarity = sent_1.similarity(sent_2)
        sim_score_list.append(similarity)

    adv_jp_score_dict = dict(zip(adv_list,sim_score_list))
    for k, v in adv_jp_score_dict.items():
        if float(v) > JOB_POSITION_RECOMMENDER_THRESHOLD_FOR_APPLICANT:
            adv_jp_recommender_dict[k] = v
        else:
            pass

    return adv_jp_score_dict,adv_jp_recommender_dict