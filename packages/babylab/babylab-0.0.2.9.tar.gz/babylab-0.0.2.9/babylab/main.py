"""
Babylab database Fask application
"""

import os
import collections
from functools import wraps
import datetime
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from babylab import api
from babylab import utils

app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = datetime.timedelta(minutes=10)

app.config["API_URL"] = "https://apps.sjdhospitalbarcelona.org/redcap/api/"
app.config["API_KEY"] = ""


def token_required(f):
    """Require login"""

    @wraps(f)
    def decorated(*args, **kwargs):
        redcap_version = api.get_redcap_version(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
        if redcap_version:
            return f(*args, **kwargs)
        flash("Access restricted. Please, log in", "error")
        return redirect(url_for("index", redcap_version=redcap_version))

    return decorated


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index(redcap_version: str = None):
    if not redcap_version:
        redcap_version = api.get_redcap_version(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
    """Index page"""
    if request.method == "POST":
        finput = request.form
        app.config["API_KEY"] = finput["apiToken"]
        redcap_version = api.get_redcap_version(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
        if redcap_version:
            flash("Logged in", "success")
            return render_template("index.html", redcap_version=redcap_version)
        flash("Incorrect token", "error")
    return render_template("index.html", redcap_version=redcap_version)


@app.route("/dashboard")
@token_required
def dashboard(records: api.Records = None):
    """Dashboard page"""
    redcap_version = api.get_redcap_version(
        url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    if records is None:
        try:
            records = api.Records(
                url=app.config["API_URL"], token=app.config["API_KEY"]
            )
        except Exception:  # pylint: disable=broad-exception-caught
            return redirect(url_for("index", redcap_version=redcap_version))
    ppts = utils.get_participants_table(
        records, url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    apts = utils.get_appointments_table(
        records, url=app.config["API_URL"], token=app.config["API_KEY"]
    )

    age_dist = (
        (ppts["age_now_days"] + (ppts["age_now_months"] * 30.437))
        .astype(int)
        .value_counts()
        .to_dict()
    )
    age_dist = {"Missing" if not k else k: v for k, v in age_dist.items()}
    sex_dist = ppts["sex"].value_counts().to_dict()
    sex_dist = {"Missing" if not k else k: v for k, v in sex_dist.items()}

    date_added = ppts["date_added"].value_counts().to_dict()
    date_added = collections.OrderedDict(sorted(date_added.items()))
    for idx, (k, v) in enumerate(date_added.items()):
        if idx > 0:
            date_added[k] = v + list(date_added.values())[idx - 1]
    n_ppts = ppts.shape[0]

    n_apts = apts.shape[0]
    date_made = apts["date_made"].value_counts().to_dict()
    date_made = collections.OrderedDict(sorted(date_made.items()))
    for idx, (k, v) in enumerate(date_made.items()):
        if idx > 0:
            date_made[k] = v + list(date_made.values())[idx - 1]
    return render_template(
        "dashboard.html",
        n_ppts=n_ppts,
        n_apts=n_apts,
        age_dist_labels=list(age_dist.keys()),
        age_dist_values=list(age_dist.values()),
        sex_dist_labels=list(sex_dist.keys()),
        sex_dist_values=list(sex_dist.values()),
        date_added_labels=list(date_added.keys()),
        date_added_values=list(date_added.values()),
        date_made_labels=list(date_made.keys()),
        date_made_values=list(date_made.values()),
    )


@app.route("/participants/")
@token_required
def participants(records: api.Records = None):
    """Participants database"""
    if records is None:
        records = api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
    df = utils.get_participants_table(
        records, url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    classes = "table table-striped table-hover table-sm dt-responsive nowrap w-100 data-toggle='table'"  # pylint: disable=line-too-long
    df["record_id"] = [f"<a href=/participants/{str(i)}>{str(i)}</a>" for i in df.index]
    df.index = df.index.astype(int)
    df = df.sort_index(ascending=False)
    df = df[
        [
            "record_id",
            "name",
            "age_now_months",
            "age_now_days",
            "sex",
            "comments",
            "date_added",
        ]
    ]
    df = df.rename(
        columns={
            "record_id": "ID",
            "name": "Name",
            "age_now_months": "Age (months)",
            "age_now_days": "Age (days)",
            "sex": "Sex",
            "comments": "Comments",
            "date_added": "Added on",
        }
    )
    return render_template(
        "participants.html",
        table=df.to_html(
            classes=classes,
            escape=False,
            justify="left",
            index=False,
            bold_rows=True,
        ),
    )


@app.route("/participants/<string:ppt_id>")
@token_required
def record_id(records: api.Records = None, ppt_id: str = None):
    """Show the record_id for that participant"""
    if records is None:
        records = api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
        data = records.participants.records[ppt_id].data
        dicts = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
        for k, v in data.items():
            dict_key = "participant_" + k
            if dict_key in dicts and v:
                data[k] = dicts[dict_key][v]
    data["age_now_months"] = (
        str(data["age_now_months"]) if data["age_now_months"] else ""
    )
    data["age_now_days"] = str(data["age_now_days"]) if data["age_now_days"] else ""
    classes = "table table-striped table-hover table-sm table-condensed"
    appts = utils.get_appointments_table(
        records.participants.records[ppt_id],
        url=app.config["API_URL"],
        token=app.config["API_KEY"],
    )
    appts["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in appts.index]
    appts["appointment_id"] = [
        f"<a href=/appointments/{i}>{i}</a>" for i in appts["appointment_id"]
    ]
    appts = appts[
        [
            "record_id",
            "appointment_id",
            "study",
            "date",
            "date_made",
            "taxi_address",
            "taxi_isbooked",
            "status",
            "comments",
        ]
    ]
    appts = appts.rename(
        columns={
            "record_id": "Participant ID",
            "appointment_id": "Appointment ID",
            "study": "Study",
            "date": "Date",
            "date_made": "Made on the",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "status": "Status",
            "comments": "Comments:",
        }
    )
    appts = appts.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )
    return render_template(
        "record_id.html", ppt_id=ppt_id, data=data, appointments=appts
    )


@app.route("/participant_new", methods=["GET", "POST"])
@token_required
def participant_new():
    """New participant page"""
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": "0",
            "participant_date_added": date_now,
            "participant_name": finput["inputName"],
            "participant_age_now_months": finput["inputAgeMonths"],
            "participant_age_now_days": finput["inputAgeDays"],
            "participant_sex": finput["inputSex"],
            "participant_twin": finput["inputTwinID"],
            "participant_parent1_name": finput["inputParent1Name"],
            "participant_parent1_surname": finput["inputParent1Surname"],
            "participant_parent2_name": finput["inputParent2Name"],
            "participant_parent2_surname": finput["inputParent2Surname"],
            "participant_email1": finput["inputEmail1"],
            "participant_phone1": finput["inputPhone1"],
            "participant_email2": finput["inputEmail2"],
            "participant_phone2": finput["inputPhone2"],
            "participant_address": finput["inputAddress"],
            "participant_city": finput["inputCity"],
            "participant_postcode": finput["inputPostcode"],
            "participant_birth_type": finput["inputDeliveryType"],
            "participant_gest_weeks": finput["inputGestationalWeeks"],
            "participant_birth_weight": finput["inputBirthWeight"],
            "participant_head_circumference": finput["inputHeadCircumference"],
            "participant_apgar1": finput["inputApgar1"],
            "participant_apgar2": finput["inputApgar2"],
            "participant_apgar3": finput["inputApgar3"],
            "participant_hearing": finput["inputNormalHearing"],
            "participant_diagnoses": finput["inputDiagnoses"],
            "participant_comments": finput["inputComments"],
            "participants_complete": "2",
        }
        api.add_participant(data, modifying=False)
        try:
            flash("Participant added!", "success")
            return redirect(url_for("participants"))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return redirect(url_for("participant_new"))
    return render_template("participant_new.html")


@app.route("/participants/<string:ppt_id>/participant_modify", methods=["GET", "POST"])
@token_required
def participant_modify(ppt_id: str, records: api.Records = None, data: dict = None):
    """Modify participant page"""
    if records is None:
        data = (
            api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
            .participants.records[ppt_id]
            .data
        )
        dicts = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
        for k, v in data.items():
            dict_key = "participant_" + k
            if dict_key in dicts and v:
                data[k] = dicts[dict_key][v]
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": ppt_id,
            "participant_date_added": date_now,
            "participant_name": finput["inputName"],
            "participant_age_now_months": finput["inputAgeMonths"],
            "participant_age_now_days": finput["inputAgeDays"],
            "participant_sex": finput["inputSex"],
            "participant_twin": finput["inputTwinID"],
            "participant_parent1_name": finput["inputParent1Name"],
            "participant_parent1_surname": finput["inputParent1Surname"],
            "participant_parent2_name": finput["inputParent2Name"],
            "participant_parent2_surname": finput["inputParent2Surname"],
            "participant_email1": finput["inputEmail1"],
            "participant_phone1": finput["inputPhone1"],
            "participant_email2": finput["inputEmail2"],
            "participant_phone2": finput["inputPhone2"],
            "participant_address": finput["inputAddress"],
            "participant_city": finput["inputCity"],
            "participant_postcode": finput["inputPostcode"],
            "participant_birth_type": finput["inputDeliveryType"],
            "participant_gest_weeks": finput["inputGestationalWeeks"],
            "participant_birth_weight": finput["inputBirthWeight"],
            "participant_head_circumference": finput["inputHeadCircumference"],
            "participant_apgar1": finput["inputApgar1"],
            "participant_apgar2": finput["inputApgar2"],
            "participant_apgar3": finput["inputApgar3"],
            "participant_hearing": finput["inputNormalHearing"],
            "participant_diagnoses": finput["inputDiagnoses"],
            "participant_comments": finput["inputComments"],
            "participants_complete": "2",
        }
        try:
            api.add_participant(data, modifying=True)
            flash("Participant modified!", "success")
            return redirect(url_for("record_id", ppt_id=ppt_id))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return redirect(url_for("participant_modify"))
    return render_template("participant_modify.html", ppt_id=ppt_id, data=data)


@app.route("/appointments/")
@token_required
def appointments(records: api.Records = None):
    """Appointments database"""
    redcap_version = api.get_redcap_version(
        url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    if records is None:
        try:
            records = api.Records(
                url=app.config["API_URL"], token=app.config["API_KEY"]
            )
        except Exception:  # pylint: disable=broad-exception-caught
            return render_template("index.html", redcap_version=redcap_version)
    df = utils.get_appointments_table(
        records, url=app.config["API_URL"], token=app.config["API_KEY"]
    )
    classes = "table table-striped table-hover table-sm table-condensed"
    df["appointment_id"] = [
        f"<a href=/appointments/{i}>{i}</a>" for i in df["appointment_id"]
    ]
    df["record_id"] = [f"<a href=/participants/{i}>{i}</a>" for i in df.index]
    df = df[
        [
            "appointment_id",
            "record_id",
            "study",
            "date",
            "date_made",
            "taxi_address",
            "taxi_isbooked",
            "status",
            "comments",
        ]
    ]
    df = df.rename(
        columns={
            "appointment_id": "Appointment ID",
            "record_id": "Participant ID",
            "study": "Study",
            "date": "Date",
            "date_made": "Made on the",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "status": "Appointment status",
            "comments": "Comments",
        }
    )
    df = df.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )
    return render_template("appointments.html", table=df)


@app.route("/appointments/<string:appt_id>")
@token_required
def appointment_id(
    records: api.Records = None,
    appt_id: str = None,
):
    """Show the record_id for that appointment"""
    if records is None:
        try:
            records = api.Records(
                url=app.config["API_URL"], token=app.config["API_KEY"]
            )
        except Exception:  # pylint: disable=broad-exception-caught
            return render_template("index.html", login_status="incorrect")
    data = records.appointments.records[appt_id].data
    dicts = api.get_data_dict(url=app.config["API_URL"], token=app.config["API_KEY"])
    for k, v in data.items():
        dict_key = "appointment_" + k
        if dict_key in dicts and v:
            data[k] = dicts[dict_key][v]
    participant = records.participants.records[data["record_id"]].data
    participant["age_now_months"] = str(participant["age_now_months"])
    participant["age_now_days"] = str(participant["age_now_days"])
    return render_template(
        "appointment_id.html",
        appt_id=appt_id,
        ppt_id=data["record_id"],
        data=data,
        participant=participant,
    )


@app.route("/participants/<string:ppt_id>/appointment_new", methods=["GET", "POST"])
@token_required
def appointment_new(ppt_id: str):
    """New appointment page"""
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": ppt_id,
            "redcap_repeat_instance": "new",
            "redcap_repeat_instrument": "appointments",
            "appointment_study": finput["inputStudy"],
            "appointment_date_made": date_now,
            "appointment_date": finput["inputDate"],
            "appointment_taxi_address": finput["inputTaxiAddress"],
            "appointment_taxi_isbooked": (
                "1" if "inputTaxiIsbooked" in finput.keys() else "0"
            ),
            "appointment_status": finput["inputStatus"],
            "appointment_comments": finput["inputComments"],
            "appointments_complete": "2",
        }
        try:
            api.add_appointment(data)
            flash("Appointment added!", "success")
            records = api.Records(
                url=app.config["API_URL"], token=app.config["API_KEY"]
            )
            return redirect(url_for("appointments", records=records))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return render_template(
                "appointment_new.html",
                ppt_id=ppt_id,
            )
    return render_template("appointment_new.html", ppt_id=ppt_id)


@app.route(
    "/participants/<string:ppt_id>/<string:appt_id>/appointment_modify",
    methods=["GET", "POST"],
)
@token_required
def appointment_modify(
    appt_id: str,
    ppt_id: str,
    records: api.Records = None,
):
    """Modify appointment page"""
    if records is None:
        data = (
            api.Records(url=app.config["API_URL"], token=app.config["API_KEY"])
            .appointments.records[appt_id]
            .data
        )
        dicts = api.get_data_dict(
            url=app.config["API_URL"], token=app.config["API_KEY"]
        )
        for k, v in data.items():
            dict_key = "appointment_" + k
            if dict_key in dicts and v:
                data[k] = dicts[dict_key][v]
    if request.method == "POST":
        finput = request.form
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = {
            "record_id": ppt_id,
            "redcap_repeat_instance": appt_id.split(":")[1],
            "redcap_repeat_instrument": "appointments",
            "appointment_study": finput["inputStudy"],
            "appointment_date_made": date_now,
            "appointment_date": finput["inputDate"],
            "appointment_taxi_address": finput["inputTaxiAddress"],
            "appointment_taxi_isbooked": (
                "1" if "inputTaxiIsbooked" in finput.keys() else "0"
            ),
            "appointment_status": finput["inputStatus"],
            "appointment_comments": finput["inputComments"],
            "appointments_complete": "2",
        }
        try:
            api.add_appointment(data, modifying=True)
            flash("Appointment modified!", "success")
            return redirect(url_for("appointments"))
        except requests.exceptions.HTTPError as e:
            flash(f"Something went wrong! {e}", "error")
            return render_template("appointments.html", ppt_id=ppt_id, appp_id=appt_id)
    return render_template(
        "appointment_modify.html", ppt_id=ppt_id, appp_id=appt_id, data=data
    )
