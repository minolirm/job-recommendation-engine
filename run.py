import json
import os

import pandas as pd

from calculate_overall_score import get_final_cf_score_for_advertisement, get_final_cf_score_for_applicant


from flask import Flask,render_template



app = Flask(__name__, template_folder='templates')
from flask_pymongo import PyMongo
mongo = PyMongo()

with open(os.path.join(os.getcwd(), 'secret/keys.json')) as profile_json:
    keys = json.loads(profile_json.read())

mongoUsername = keys["mongo"]["username"]
mongoPassword = keys["mongo"]["password"]
mongoHost = "localhost"  # Public IP: 54.177.36.96  Private IP: 10.0.2.27
mongoPort = "27017"

mongoDB = "JobPlatformQA"
app.config["MONGO_URI"] = "mongodb://{username}:{password}@{host}:{port}/{db}?authSource=admin".format(
    username=mongoUsername, password=mongoPassword,
    host=mongoHost, port=mongoPort,
    db=mongoDB
)
mongo.init_app(app)


#skill based
@app.route("/recommendations/advertisement/<ad_id>", methods=["GET"])
def get_applicants_for_ad(ad_id):
    from process_data.get_data import get_advertisements_by_id, load_all_applicants, get_applicant_by_id
    new_ad = get_advertisements_by_id(ad_id)

    if new_ad is None:
        return {'error':'cannot find the job'}
    new_ad_df = pd.DataFrame(new_ad,index=[0])

    adv_df = new_ad_df
    applicants = load_all_applicants()
    ap_df = pd.DataFrame(applicants)
    final_dict = get_final_cf_score_for_advertisement(
        adv_df, ap_df)
    final_result = final_dict



    return {'final_result':final_result}

@app.route("/recommendations/advertisement/<ad_id>/ui", methods=["GET"])
def get_applicants_for_ad_ui(ad_id):
    from process_data.get_data import get_advertisements_by_id, load_all_applicants, get_applicant_by_id
    new_ad = get_advertisements_by_id(ad_id)

    if new_ad is None:
        return {'error':'cannot find the job'}
    new_ad_df = pd.DataFrame(new_ad,index=[0])

    adv_df = new_ad_df
    applicants = load_all_applicants()
    ap_df = pd.DataFrame(applicants)
    final_dict = get_final_cf_score_for_advertisement(
        adv_df, ap_df)
    final_result = []



    for key, val in final_dict.items():
        res = {
                'applicant_data': get_applicant_by_id(key),
                'final_score': val
            }

        final_result.append(res)


    return render_template('ad_ui.html',data = final_result, list_length = len(final_result),advertisement = new_ad)


@app.route("/recommendations/applicant/<ap_id>", methods=["GET"])
def get_jobs_for_ap(ap_id):
    from process_data.get_data import get_advertisements_by_id, get_active_jobs, get_applicant_by_id

    all_ads = get_active_jobs()
    ad_df = pd.DataFrame(all_ads)

    adv_df = ad_df

    applicants = get_applicant_by_id(ap_id)
    new_ap_df = pd.DataFrame(applicants)
    final_dict = get_final_cf_score_for_applicant(
        new_ap_df, adv_df)
    final_result = final_dict

    return {'final_result':final_result}

@app.route("/recommendations/applicant/<ap_id>/ui", methods=["GET"])
def get_jobs_for_ap_ui(ap_id):
    from process_data.get_data import get_advertisements_by_id, get_active_jobs, get_applicant_by_id

    all_ads = get_active_jobs()
    ad_df = pd.DataFrame(all_ads)

    adv_df = ad_df

    applicants = get_applicant_by_id(ap_id)
    new_ap_df = pd.DataFrame(applicants)
    final_dict = get_final_cf_score_for_applicant(
        new_ap_df, adv_df)
    final_result = []


    for key, val in final_dict.items():
        res = {
                'adv_data': get_advertisements_by_id(key),
                'final_score': val
            }

        final_result.append(res)

    return render_template('ap_ui.html',data = final_result, list_length = len(final_result),applicant = applicants)

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8989)), debug=True)

