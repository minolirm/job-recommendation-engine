from preprocess import pre_process
from config import AP_ENGINE,AD_ENGINE
import spacy
nlp = spacy.load("en_core_web_lg")


def match_other_fields_for_applicants(applicant_df, advertisement_df):
    sim_score_list = []
    adv_score_dict = {}
    adv_ids = advertisement_df['_id'].tolist()
    if len(advertisement_df) != 0:
        advertisement_df = pre_process(advertisement_df, AD_ENGINE["primary"])
        app_skills_set = pre_process(applicant_df, AP_ENGINE["primary"])['curated_text'][0]
        sent_1 = nlp(app_skills_set)

        for row_idx,row in advertisement_df.iterrows():
            adv_skills_set = str(row['curated_text'])
            sent_2 = nlp(adv_skills_set)
            similarity = sent_1.similarity(sent_2)
            sim_score_list.append(similarity)

        adv_score_dict = dict(zip(adv_ids, sim_score_list))

    else:
            pass
    return adv_score_dict


def match_other_fields_for_advertisement(advertisement_df, applicant_df):
    sim_score_list = []
    app_score_dict = {}
    app_ids = applicant_df['_id'].tolist()
    if len(applicant_df) != 0:
        pri_ap_df = pre_process(applicant_df, AP_ENGINE["primary"])
        adv_skills_set = pre_process(advertisement_df, AD_ENGINE["primary"])['curated_text'][0]
        sent_1 = nlp(adv_skills_set)

        for row_idx,row in pri_ap_df.iterrows():
            app_skills_set = str(row['curated_text'])
            sent_2 = nlp(app_skills_set)
            similarity = sent_1.similarity(sent_2)
            sim_score_list.append(similarity)

            app_score_dict = dict(zip(app_ids, sim_score_list))

        else:
            pass
    else:
        pass
    return app_score_dict
