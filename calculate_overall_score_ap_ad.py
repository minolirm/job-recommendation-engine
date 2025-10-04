""""New Adv --- Applicant Score Calculation"""""


def calculate_overall_score_for_adv_rec(pri_score_dict, sec_score_dict):
    weighted_dict = dict()
    for k, v in sec_score_dict.items():
        weighted_dict[k] = "{:.2f}".format((pri_score_dict[k] * 0.9) + v * 0.1)
    return weighted_dict


""""New App --- Advertisement Score Calculation"""""


def calculate_overall_score_for_app_rec(pri_score_dict, sec_score_dict):
    weighted_dict = dict()
    for k, v in sec_score_dict.items():
        weighted_dict[k] = "{:.2f}".format((pri_score_dict[k] * 0.9) + v * 0.1)
    return weighted_dict



