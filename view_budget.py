import os
import glob
import matplotlib.pyplot as plt
import pandas as pd


def get_salary(years):
    salary_df = pd.DataFrame(columns=["Date", "Salary"])
    for year in years:
        fn = glob.glob(os.path.join(os.getcwd(), f"{year}.xlsx"))[0]
        df = pd.read_excel(fn, sheet_name=None)
        del df["Total"]
        months = df.keys()
        for month in months:
            df_mth = df[month]
            row = {"Date": f"{month}-01-{year}",
                   "Salary": df_mth.loc[(df_mth.Totals == "Salary")].iloc[0, 1]
                   }
            salary_df = salary_df.append(row, ignore_index=True)
    salary_df = salary_df.reset_index(drop=True)
    salary_df["Date"] = pd.to_datetime(salary_df["Date"], format="%B-%d-%Y")
    return salary_df


def group_dates(datetime):
    datetime = datetime.replace(day=1)
    return datetime


def group_major(df):

    major_tags = {"Housing": "Essentials",
                  "Utilities": "Essentials",
                  "Cellular": "Essentials",
                  "Grocery": "Essentials",
                  "Health": "Essentials",
                  "Insurance": "Essentials",
                  "Entertainment": "Frivolous",
                  "Transportation": "Essentials",
                  "Miscellaneous": "Miscellaneous",
                  "Flight": "Frivolous"}
    minor_tags = {"Alcohol": "Frivolous",
                  "Electronics": "Essentials",
                  "Home Improvement": "Essentials",
                  "Photography": "Frivolous",
                  "Presents": "Essentials",
                  "Self Care": "Essentials",
                  "Services": "Essentials",
                  "Travel": "Frivolous",
                  "Frivolous": "Frivolous",
                  "Essentials": "Essentials"}
    df["Major"] = df["Category"].apply(lambda x: major_tags[x])
    df.loc[(df.Major == "Miscellaneous"), "Major"] = df.loc[
        (df.Major == "Miscellaneous"), "Tag"]
    df["Major"] = df["Major"].apply(lambda x: minor_tags[x])
    return df


def plot_area(df, grouper, salary_df=None):
    group_df = df.loc[:, ["Date", "Price", grouper]]
    group_df["Date"] = group_df["Date"].apply(group_dates)
    group_df = group_df.groupby([grouper, "Date"]).agg({"Price": "sum"})
    ax = group_df.unstack(level=0).plot.area()
    labels = ax.legend().get_texts()
    for label in labels:
        label.set_text(label.get_text().split(" ")[1][:-1])
    if salary_df is not None:
        breakpoint()
        ax.plot(salary_df["Date"], salary_df["Salary"])
    plt.show(block=False)


def main():
    years = [2019, 2020]
    dfs = []
    salary_df = get_salary(years)
    for year in years:
        fn = glob.glob(os.path.join(os.getcwd(), f"{year}.csv"))[0]
        dfs.append(pd.read_csv(fn))

    df = dfs[0]
    for i in range(1, len(years)):
        df = df.append(dfs[i])
    df = df.reset_index(drop=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df = group_major(df)
    plot_area(df, "Category", salary_df)
    plot_area(df, "Tag", salary_df)
    plot_area(df, "Major", salary_df)
    df_frivolous = df.loc[(df.Major == "Frivolous"), :]
    plot_area(df_frivolous, "Tag")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
