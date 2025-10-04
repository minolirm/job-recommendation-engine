import spacy
from sklearn.feature_extraction.text import CountVectorizer

from config import SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT, \
    SKILL_RECOMMENDER_THRESHOLD_FOR_APPLICANT

nlp = spacy.load("en_core_web_lg")
vectorizer = CountVectorizer()


def match_ap_skills_for_advertisement(advertisement_df, applicant_df):
    sim_score_list = []
    app_recommender_dict = {}
    app_list = applicant_df['_id'].tolist()

    adv_skills_set = str(advertisement_df['job_skills'][0]).replace(',', ' ')
    sent_1 = nlp(adv_skills_set)

    for row_idx, row in applicant_df.iterrows():
        app_skills_set = str(row['skills']).replace(',', ' ')
        sent_2 = nlp(app_skills_set)

        similarity = sent_1.similarity(sent_2)
        sim_score_list.append(similarity)

    app_score_dict = dict(zip(app_list, sim_score_list))
    for k, v in app_score_dict.items():
        if (float(v)) > SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT:
            app_recommender_dict[k] = v
        else:
            pass

    return app_score_dict, app_recommender_dict


def match_ad_skills_for_applicant(applicant_df, advertisement_df):
    sim_score_list = []
    adv_skill_recommender_dict = {}
    adv_list = advertisement_df['_id'].tolist()

    app_skills_set = str(applicant_df['skills'][0]).replace(',', ' ')
    sent_1 = nlp(app_skills_set)

    for row_idx, row in advertisement_df.iterrows():
        adv_skills_set = str(row['job_skills']).replace(',', ' ')
        sent_2 = nlp(adv_skills_set)
        similarity = sent_1.similarity(sent_2)
        sim_score_list.append(similarity)

    adv_skill_score_dict = dict(zip(adv_list, sim_score_list))
    for k, v in adv_skill_score_dict.items():
        if (float(v)) > SKILL_RECOMMENDER_THRESHOLD_FOR_APPLICANT:
            adv_skill_recommender_dict[k] = v
        else:
            pass

    return adv_skill_score_dict, adv_skill_recommender_dict
