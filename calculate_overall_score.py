from job_category_content_filtering import match_ap_job_category_for_advertisement, \
    match_ad_job_category_for_applicant
from job_position_content_filtering import match_ap_job_position_for_advertisement, \
    match_ad_job_positions_for_applicant
from other_content_filtering import match_other_fields_for_advertisement, \
    match_other_fields_for_applicants
from skill_content_filtering import match_ap_skills_for_advertisement, \
    match_ad_skills_for_applicant
from config import WEIGHTED_THRESHOLD_FOR_NEW_APPLICANT, WEIGHTED_THRESHOLD_FOR_NEW_ADVERTISEMENT, \
    SKILLS_RECOMMENDER_THRESHOLD_FOR_APPLICANT_l1, SKILLS_RECOMMENDER_THRESHOLD_FOR_APPLICANT_l2, \
    SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT_l1, SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT_l2, \
    SKILLS_RECOMMENDER_THRESHOLD_FOR_APPLICANT_l3, SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT_l3


def get_final_cf_score_for_advertisement(adv_df, app_df):
    weighted_dict = {}
    recommendations_dict = {}
    app_skill_score_dict, app_skill_recommender_dict = match_ap_skills_for_advertisement(advertisement_df=adv_df,
                                                                                         applicant_df=app_df)
    app_jp_score_dict, app_jp_recommender_dict = match_ap_job_position_for_advertisement(advertisement_df=adv_df,
                                                                                         applicant_df=app_df)
    app_jc_score_dict, app_jc_recommender_dict = match_ap_job_category_for_advertisement(advertisement_df=adv_df,
                                                                                         applicant_df=app_df)

    rec_jp_ids = list(app_jp_recommender_dict.keys())
    rec_skill_ids = list(app_skill_recommender_dict.keys())
    rec_jc_ids = list(app_jc_recommender_dict.keys())

    rec_ids_1 = [value for value in rec_skill_ids if value in rec_jp_ids]
    rec_ids_2 = [value for value in rec_ids_1 if value in rec_jc_ids]
    new_app_df = app_df[app_df['_id'].isin(rec_ids_2)]
    app_oth_score_dict = match_other_fields_for_advertisement(adv_df, new_app_df)
    for k, v in app_skill_score_dict.items():
        if k in app_oth_score_dict:

            if float(v) >= SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT_l1:
                weighted_dict[k] = "{:.2f}".format(
                    (app_oth_score_dict[k] * 0.1) + app_skill_score_dict[k] * 0.45 + app_jp_score_dict[k] * 0.3 +
                    app_jc_score_dict[k] * 0.1)

            elif SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT_l1 > float(
                    v) >= SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT_l2:
                weighted_dict[k] = "{:.2f}".format(
                    (app_oth_score_dict[k] * 0.1) + app_skill_score_dict[k] * 0.4 + app_jp_score_dict[k] * 0.25 +
                    app_jc_score_dict[k] * 0.1)

            elif SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT_l2 > float(
                    v) >= SKILLS_RECOMMENDER_THRESHOLD_FOR_ADVERTISEMENT_l3:
                weighted_dict[k] = "{:.2f}".format(
                    (app_oth_score_dict[k] * 0.1) + app_skill_score_dict[k] * 0.35 + app_jp_score_dict[k] * 0.2 +
                    app_jc_score_dict[k] * 0.1)

            else:
                weighted_dict[k] = "{:.2f}".format(
                    (app_oth_score_dict[k] * 0.1) + app_skill_score_dict[k] * 0.3 + app_jp_score_dict[k] * 0.15 +
                    app_jc_score_dict[k] * 0.1)


        else:
            weighted_dict[k] = "{:.2f}".format(
                app_skill_score_dict[k] * 0.3 + app_jp_score_dict[k] * 0.3)
    weighted_dict = dict(sorted(weighted_dict.items(), key=lambda x: x[1], reverse=True))

    for k, v in weighted_dict.items():
        if float(v) > WEIGHTED_THRESHOLD_FOR_NEW_ADVERTISEMENT:
            recommendations_dict[k] = v
        else:
            pass
    return recommendations_dict


def get_final_cf_score_for_applicant(app_df, adv_df):
    weighted_dict = {}
    recommendations_dict = {}
    adv_skill_score_dict, adv_skill_recommender_dict = match_ad_skills_for_applicant(applicant_df=app_df,
                                                                                     advertisement_df=adv_df)
    adv_jp_score_dict, adv_jp_recommender_dict = match_ad_job_positions_for_applicant(applicant_df=app_df,
                                                                                      advertisement_df=adv_df)

    adv_jc_score_dict, adv_jc_recommender_dict = match_ad_job_category_for_applicant(applicant_df=app_df,
                                                                                     advertisement_df=adv_df)

    rec_skill_ids = list(adv_skill_recommender_dict.keys())
    rec_jp_ids = list(adv_jp_recommender_dict.keys())
    rec_jc_ids = list(adv_jc_recommender_dict.keys())

    rec_ids_1 = [value for value in rec_skill_ids if value in rec_jp_ids]
    rec_ids_2 = [value for value in rec_ids_1 if value in rec_jc_ids]
    new_adv_df = adv_df[adv_df['_id'].isin(rec_ids_2)]

    adv_oth_score_dict = match_other_fields_for_applicants(app_df, new_adv_df)
    for k, v in adv_skill_score_dict.items():
        if k in adv_oth_score_dict:
            if float(v) >= SKILLS_RECOMMENDER_THRESHOLD_FOR_APPLICANT_l1:
                weighted_dict[k] = "{:.2f}".format(
                    (adv_oth_score_dict[k] * 0.1) + adv_skill_score_dict[k] * 0.45 + adv_jp_score_dict[k] * 0.3 +
                    adv_jc_score_dict[k] * 0.1)

            elif SKILLS_RECOMMENDER_THRESHOLD_FOR_APPLICANT_l1 > float(
                    v) >= SKILLS_RECOMMENDER_THRESHOLD_FOR_APPLICANT_l2:
                weighted_dict[k] = "{:.2f}".format(
                    (adv_oth_score_dict[k] * 0.1) + adv_skill_score_dict[k] * 0.4 + adv_jp_score_dict[k] * 0.25 +
                    adv_jc_score_dict[k] * 0.1)

            elif SKILLS_RECOMMENDER_THRESHOLD_FOR_APPLICANT_l2 > float(
                    v) >= SKILLS_RECOMMENDER_THRESHOLD_FOR_APPLICANT_l3:
                weighted_dict[k] = "{:.2f}".format(
                    (adv_oth_score_dict[k] * 0.1) + adv_skill_score_dict[k] * 0.35 + adv_jp_score_dict[k] * 0.2 +
                    adv_jc_score_dict[k] * 0.1)

            else:
                weighted_dict[k] = "{:.2f}".format(
                    (adv_oth_score_dict[k] * 0.1) + adv_skill_score_dict[k] * 0.3 + adv_jp_score_dict[k] * 0.15 +
                    adv_jc_score_dict[k] * 0.1)

        else:
            weighted_dict[k] = "{:.2f}".format(
                adv_skill_score_dict[k] * 0.3 + adv_jp_score_dict[k] * 0.3)
    weighted_dict = dict(sorted(weighted_dict.items(), key=lambda x: x[1], reverse=True))

    for k, v in weighted_dict.items():
        if float(v) > WEIGHTED_THRESHOLD_FOR_NEW_APPLICANT:
            recommendations_dict[k] = v
        else:
            pass
        return recommendations_dict
