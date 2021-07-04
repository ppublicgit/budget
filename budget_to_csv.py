import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime

MONTHS = {"January": 1,
          "February": 2,
          "March": 3,
          "April": 4,
          "May": 5,
          "June": 6,
          "July": 7,
          "August": 8,
          "September": 9,
          "October": 10,
          "November": 11,
          "December": 12
          }



def extract_living(df):
    df_living = df.iloc[:, [0, 1, 2]].dropna()
    df = pd.DataFrame(columns=["Place", "Date",
                               "Category", "Price",
                               "Description", "Tag"])

    info = {
        "Apartment": [
            "Addison Park", "Housing", "Rent", "Essentials"
        ],
        "Utilities": [
            "Utilities", "Utilities", "Water/Electric", "Essentials"
        ],
        "Internet": [
            "Comcast", "Utilities", "Internet", "Essentials"
        ],
        "Cellular": [
            "MintMobile", "Cellular", "Cellular", "Essentials"
        ],
        "Insurance (Car+Renters)": [
            "Geico", "Insurance", "Home/Auto", "Essentials"
        ]
        }

    for key in info.keys():
        if key in df_living["Living"].values:
            sub_df = df_living.loc[df_living["Living"] == key]
            row = {"Place": info[key][0],
                   "Date": sub_df.iloc[0, 1],
                   "Category": info[key][1],
                   "Price": sub_df.iloc[0, 2],
                   "Description": info[key][2],
                   "Tag": info[key][3]
                   }
            df = df.append(row, ignore_index=True)
    return df


def extract_groceries(df):
    df_grocery = df.iloc[:, [3, 4, 5]].dropna()
    df = pd.DataFrame(columns=["Place", "Date",
                               "Category", "Price",
                               "Description", "Tag"])

    for index, row in df_grocery.iterrows():
        observation = {
            "Place": row.iloc[0],
            "Date": row.iloc[1],
            "Category": "Grocery",
            "Price": row.iloc[2],
            "Description": "",
            "Tag": "Grocery"
        }
        df = df.append(observation, ignore_index=True)

    return df


def extract_transportation(df):
    df_transport = df.iloc[:, [6, 7, 8]].dropna()
    df = pd.DataFrame(columns=["Place", "Date",
                               "Category", "Price",
                               "Description", "Tag"])

    for index, row in df_transport.iterrows():
        observation = {
            "Place": row.iloc[0],
            "Date": row.iloc[1],
            "Category": "Transportation",
            "Price": row.iloc[2],
            "Description": "",
            "Tag": "Transportation"
        }
        df = df.append(observation, ignore_index=True)

    return df


def extract_dining(df):
    df_dining = df.iloc[:, [9, 10, 11]].dropna()
    df = pd.DataFrame(columns=["Place", "Date",
                               "Category", "Price",
                               "Description", "Tag"])

    for index, row in df_dining.iterrows():
        observation = {
            "Place": row.iloc[0],
            "Date": row.iloc[1],
            "Category": "Entertainment",
            "Price": row.iloc[2],
            "Description": "",
            "Tag": "Dining"
        }
        df = df.append(observation, ignore_index=True)

    return df


def extract_entertainment(df):
    df_entertainment = df.iloc[:, [12, 13, 14, 15, 16]].dropna()
    df = pd.DataFrame(columns=["Place", "Date",
                               "Category", "Price",
                               "Description", "Tag"])

    for index, row in df_entertainment.iterrows():
        if row.iloc[4] == "Alocohol":
            pass#breakpoint()
        if row.iloc[4] == "Photgraphy":
            pass#breakpoint()
        observation = {
            "Place": row.iloc[0],
            "Date": row.iloc[1],
            "Category": "Entertainment",
            "Price": row.iloc[3],
            "Description": row.iloc[2],
            "Tag": row.iloc[4]
        }
        df = df.append(observation, ignore_index=True)

    return df


def extract_miscellaneous(df):
    df_miscellaneous = df.iloc[:, [17, 18, 19, 20, 21]].dropna()
    df = pd.DataFrame(columns=["Place", "Date",
                               "Category", "Price",
                               "Description", "Tag"])

    for index, row in df_miscellaneous.iterrows():
        observation = {
            "Place": row.iloc[0],
            "Date": row.iloc[1],
            "Category": "Miscellaneous",
            "Price": row.iloc[3],
            "Description": row.iloc[2],
            "Tag": row.iloc[4]
        }
        df = df.append(observation, ignore_index=True)

    return df


def extract_health_and_fitness(df):
    df_health = df.iloc[:, [22, 23, 24, 25, 26]].dropna()
    df = pd.DataFrame(columns=["Place", "Date",
                               "Category", "Price",
                               "Description", "Tag"])

    for index, row in df_health.iterrows():
        observation = {
            "Place": row.iloc[0],
            "Date": row.iloc[1],
            "Category": "Health",
            "Price": row.iloc[3],
            "Description": row.iloc[2],
            "Tag": row.iloc[4]
        }
        df = df.append(observation, ignore_index=True)

    return df


def extract_flight_school(df):
    if len(df.columns) < 31:
        return
    df_flight = df.iloc[:, [27, 28, 29, 30]].dropna()
    df = pd.DataFrame(columns=["Place", "Date",
                               "Category", "Price",
                               "Description", "Tag"])

    for index, row in df_flight.iterrows():
        observation = {
            "Place": row.iloc[0],
            "Date": row.iloc[1],
            "Category": "Entertainment",
            "Price": row.iloc[3],
            "Description": row.iloc[2],
            "Tag": "Flight"
        }
        df = df.append(observation, ignore_index=True)

    return df


def extract_retirement(filename, year):
    #breakpoint()
    df_retirement_months = pd.read_excel(filename,
                                         sheet_name=None,
                                         usecols=list(range(3)),
                                         skiprows=38,
                                         nrows=13,
                                         engine="openpyxl")
    del df_retirement_months["Total"]
    months = df_retirement_months.keys()
    df_retirement = pd.DataFrame(columns=["Place", "Date",
                                          "Category", "Price",
                                          "Description", "Tag"])
    for month in months:
        ret_date = datetime.datetime(int(year), MONTHS[month], 1)
        for ret_account in ["401k", "Roth IRA"]:
            observation = {
                "Place": ret_account,
                "Date": ret_date,
                "Category": "Retirement",
                "Price": 0,
                "Description": f"{ret_account} Retirement Contribution",
                "Tag": "Retirement"
            }
            df_retirement = df_retirement.append(observation, ignore_index=True)

    return df_retirement


def fix_month(month, year, date):
    MONTHS = {"January": 1, "February": 2, "March": 3,
              "April": 4, "May": 5, "June": 6,
              "July": 7, "August": 8, "September": 9,
              "October": 10, "November": 11, "December": 12
              }
    try:
        if date.month != MONTHS[month]:
            date = date.replace(month=MONTHS[month])
        if date.year != year:
            date = date.replace(year=year)
    except AttributeError as e:
        print(month, year, date)
        print(e)
        raise ValueError("Bad Date")

    return date


def import_odf(filename, year):
    df_months = pd.read_excel(filename,
                              sheet_name=None,
                              usecols=list(range(2, 33)),
                              nrows=30,
                              engine="openpyxl")
    del df_months["Total"]
    months = df_months.keys()
    df_all_months = pd.DataFrame(columns=["Place", "Date",
                                          "Category", "Price",
                                          "Description", "Tag"])
    for month in months:
        df = df_months[month]
        df_month = pd.DataFrame(columns=[
            "Place", "Date", "Category",
            "Price", "Description", "Tag"])

        living_df = extract_living(df)
        grocery_df = extract_groceries(df)
        transportation_df = extract_transportation(df)
        dining_df = extract_dining(df)
        entertainment_df = extract_entertainment(df)
        miscellaneous_df = extract_miscellaneous(df)
        health_df = extract_health_and_fitness(df)
        flight_df = extract_flight_school(df)
        df_month = df_month.append([living_df,
                                    grocery_df,
                                    transportation_df,
                                    dining_df,
                                    entertainment_df,
                                    miscellaneous_df,
                                    health_df,
                                    flight_df],
                                   ignore_index=True)

        df_month["Date"] = df_month["Date"].apply(
            lambda x: fix_month(month, year, x)
        )

        df_all_months = df_all_months.append(df_month)
    df_retirement = extract_retirement(filename, year)
    df_all_months = df_all_months.append(df_retirement)
    return df_all_months.reset_index(drop=True)


def main():
    years = [2019, 2020]
    df_year = pd.DataFrame(columns=[
            "Place", "Date", "Category",
            "Price", "Description", "Tag"])

    for year in years:
        f = glob.glob(os.path.join(os.getcwd(), f"../*{year}.xlsx"))[0]
        breakpoint()
        df_year = import_odf(f, year)
        df_year.to_csv(os.path.join(os.getcwd(), f"{year}.csv"), index=False)
    return


if __name__ == "__main__":
    main()
