"""
Util functions for the app
"""

from pandas import DataFrame
from babylab import api
from babylab import calendar


def get_participants_table(records: api.Records, **kwargs) -> DataFrame:
    """Get participants table

    Args:
        records (api.Records): _description_

    Returns:
        pd.DataFrame: Table of partcicipants.
    """
    cols = ["name", "age_now_months", "age_now_days", "sex", "comments", "date_added"]
    if records.participants.records:
        new_age_months = []
        new_age_days = []
        for _, v in records.participants.records.items():
            age = calendar.get_age(
                birth_date=calendar.get_birth_date(
                    age=f"{v.data["age_now_months"]}:{v.data["age_now_days"]}"
                )
            )
            new_age_months.append(int(age[0]))
            new_age_days.append(int(age[1]))
        df = records.participants.to_df()
        df["age_now_months"] = new_age_months
        df["age_now_days"] = new_age_days
        # dicts = api.get_data_dict()
        # for col_name, col_values in df.items():
        #     key = "participant_" + col_name
        #     print(col_name)
        #     if key in dicts:
        #         print(key)
        #         df[col_name] = [dicts[key][v] for v in col_values]
        return df
    return DataFrame(records.participants.records, columns=cols)


def get_appointments_table(records: api.Records, **kwargs) -> DataFrame:
    """Get appointments table.

    Args:
        records (api.Records): _description_

    Returns:
        pd.DataFrame: Table of appointments.
    """
    cols = [
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
    if records.appointments.records:
        df = records.appointments.to_df().sort_values("date", ascending=False)
        dicts = api.get_data_dict(**kwargs)
        for col_name, col_values in df.items():
            key = "appointment_" + col_name
            if key in dicts:
                df[col_name] = [dicts[key][v] for v in col_values]
        return df
    return DataFrame(records.appointments.records, columns=cols)
