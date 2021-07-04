import sys
import os
import glob
import pandas as pd
import datetime

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from budget_gui_ui import Ui_MainWindow
import view_budget as vb
import budget_to_csv as b2c


class PlotLine:
    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        self.df = None

    def update(self):
        """Update matplotlib toolbar memory (such as Home button)."""
        self.ax.figure.canvas.toolbar.update()
        self.ax.figure.canvas.fig.tight_layout()
        self.ax.figure.canvas.draw()

    def make_plot(self, df, salary_df=None):
        self.ax.clear()
        expenses_df = df.loc[:, ["Date", "Price"]]
        expenses_df["Date"] = df["Date"].apply(vb.group_dates)
        expenses_df = group_df.groupby(["Date"]).agg({"Price": "sum"})
        retirement_df = df.loc[df["Category"] == "Retirement"]
        retirement_df["Date"] = retirement_df["Date"].apply(vb.group_dates)
        retirement_df = retirement_df.groupby(["Date"]).agg({"Price": "sum"})
        self.ax.plot(salary_df["Date"], salary_df["Salary"])

def debug_trace():
    '''Set a tracepoint in the Python debugger that works with Qt'''
    from PyQt5.QtCore import pyqtRemoveInputHook

    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()

class PlotArea:
    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        self.df = None

    def update(self):
        """Update matplotlib toolbar memory (such as Home button)."""
        self.ax.figure.canvas.toolbar.update()
        self.ax.figure.canvas.fig.tight_layout()
        self.ax.figure.canvas.draw()

    def fix_subset(self, subset):
        new_subset = []
        for sub in subset:
            new_sub = sub.replace("_", " ")
            new_subset.append(new_sub.title())
        return new_subset

    def make_plot(self, df, grouper, salary_df=None, subselect=None):
        self.ax.clear()
        if subselect is not None and subselect != []:
            subselect = self.fix_subset(subselect)
            if grouper == "Category":
                df = df.loc[df["Category"].isin(subselect)]
            elif grouper == "Tag":
                df = df.loc[df["Tag"].isin(subselect)]
        group_df = df.loc[:, ["Date", "Price", grouper]]
        group_df["Date"] = group_df["Date"].apply(vb.group_dates)
        group_df = group_df.groupby([grouper, "Date"]).agg({"Price": "sum"})
        try:
            group_df.unstack(level=0).plot.area(ax=self.ax)
        except ValueError as e:
            print("Negative value found for price, setting to 0")
            group_df = group_df.unstack(level=0)
            group_df.loc[group_df[("Price", "Gambling")] < 0, ("Price", "Gambling")] = 0
            group_df.plot.area(ax=self.ax)

        labels = self.ax.legend().get_texts()
        for label in labels:
            label.set_text(label.get_text().split(" ")[1][:-1])
        if salary_df is not None:
            self.ax.plot(salary_df["Date"], salary_df["Salary"])
        self.ax.grid(True)


class MainWindow(QMainWindow, Ui_MainWindow):
    """Primary GUI window."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.p_major = PlotArea(fig=self.mpl_major.canvas.fig,
                            ax=self.mpl_major.canvas.ax1)
        self.p_category = PlotArea(fig=self.mpl_category.canvas.fig,
                               ax=self.mpl_category.canvas.ax1)
        self.p_tag = PlotArea(fig=self.mpl_tag.canvas.fig,
                          ax=self.mpl_tag.canvas.ax1)
        self.p_frivolous = PlotArea(fig=self.mpl_frivolous.canvas.fig,
                                ax=self.mpl_frivolous.canvas.ax1)
        self.p_savings = PlotLine(fig=self.mpl_savings.canvas.fig,
                                  ax=self.mpl_savings.canvas.ax1)

        self.data_folder = "/home/p/Documents/Personal/Budget/"
        self.categories = []
        self.tags = []
        self.year_start = None
        self.year_end = None
        self.month_start = None
        self.month_end = None

        self.setup_gui()

    def setup_gui(self):
        self.actionData_Folder.triggered.connect(self.get_data_folder)
        self.sb_year_start.valueChanged.connect(self.get_year_start)
        self.get_year_start()
        self.sb_year_end.valueChanged.connect(self.get_year_end)
        self.get_year_end()
        self.sb_month_start.valueChanged.connect(self.get_month_start)
        self.get_month_start()
        self.sb_month_end.valueChanged.connect(self.get_month_end)
        self.get_month_end()
        self.cb_housing.stateChanged.connect(self.get_housing_chkbox)
        self.get_housing_chkbox()
        self.cb_utilities.stateChanged.connect(self.get_utilities_chkbox)
        self.get_utilities_chkbox()
        self.cb_cellular.stateChanged.connect(self.get_cellular_chkbox)
        self.get_cellular_chkbox()
        self.cb_insurance.stateChanged.connect(self.get_insurance_chkbox)
        self.get_insurance_chkbox()
        self.cb_grocery.stateChanged.connect(self.get_grocery_chkbox)
        self.get_grocery_chkbox()
        self.cb_transportation.stateChanged.connect(
            self.get_transportation_chkbox)
        self.get_transportation_chkbox()
        self.cb_entertainment.stateChanged.connect(
            self.get_entertainment_chkbox)
        self.get_entertainment_chkbox()
        self.cb_miscellaneous.stateChanged.connect(
            self.get_miscellaneous_chkbox)
        self.get_miscellaneous_chkbox()
        self.cb_health.stateChanged.connect(self.get_health_chkbox)
        self.get_health_chkbox()
        self.cb_retirement.stateChanged.connect(self.get_retirement_chkbox)
        self.get_retirement_chkbox()
        self.cb_alcohol.stateChanged.connect(self.get_alcohol_chkbox)
        self.get_alcohol_chkbox()
        self.cb_books.stateChanged.connect(self.get_books_chkbox)
        self.get_books_chkbox()
        self.cb_camping.stateChanged.connect(self.get_camping_chkbox)
        self.get_camping_chkbox()
        self.cb_climbing.stateChanged.connect(self.get_climbing_chkbox)
        self.get_climbing_chkbox()
        self.cb_dining.stateChanged.connect(self.get_dining_chkbox)
        self.get_dining_chkbox()
        self.cb_electronics.stateChanged.connect(self.get_electronics_chkbox)
        self.get_electronics_chkbox()
        self.cb_essentials.stateChanged.connect(self.get_essentials_chkbox)
        self.get_essentials_chkbox()
        self.cb_flight.stateChanged.connect(self.get_flight_chkbox)
        self.get_flight_chkbox()
        self.cb_games.stateChanged.connect(self.get_games_chkbox)
        self.get_games_chkbox()
        self.cb_gambling.stateChanged.connect(self.get_gambling_chkbox)
        self.get_gambling_chkbox()
        self.cb_golf.stateChanged.connect(self.get_golf_chkbox)
        self.get_golf_chkbox()
        self.cb_grocery_tag.stateChanged.connect(self.get_grocery_tag_chkbox)
        self.get_grocery_tag_chkbox()
        self.cb_gym.stateChanged.connect(self.get_gym_chkbox)
        self.get_gym_chkbox()
        self.cb_home_improvement.stateChanged.connect(self.get_home_improvement_chkbox)
        self.get_home_improvement_chkbox()
        self.cb_medical.stateChanged.connect(self.get_medical_chkbox)
        self.get_medical_chkbox()
        self.cb_museum.stateChanged.connect(self.get_museum_chkbox)
        self.get_museum_chkbox()
        self.cb_photography.stateChanged.connect(self.get_photography_chkbox)
        self.get_photography_chkbox()
        self.cb_presents.stateChanged.connect(self.get_presents_chkbox)
        self.get_presents_chkbox()
        self.cb_self_care.stateChanged.connect(self.get_self_care_chkbox)
        self.get_self_care_chkbox()
        self.cb_services.stateChanged.connect(self.get_services_chkbox)
        self.get_services_chkbox()
        self.cb_skiing.stateChanged.connect(self.get_skiing_chkbox)
        self.get_skiing_chkbox()
        self.cb_sports.stateChanged.connect(self.get_sports_chkbox)
        self.get_sports_chkbox()
        self.cb_transportation_tag.stateChanged.connect(
            self.get_transportation_tag_chkbox)
        self.get_transportation_tag_chkbox()
        self.cb_travel.stateChanged.connect(self.get_travel_chkbox)
        self.get_travel_chkbox()
        self.cb_retirement_tag.stateChanged.connect(self.get_retirement_tag_chkbox)
        self.get_retirement_tag_chkbox()
        self.pb_plot.clicked.connect(self.plot)
        self.pb_update_data.clicked.connect(self.update_data)

    def get_data_folder(self):
        fn = QFileDialog.getOpenFileName(None, u"Select File for Folder Path",
                                         "",
                                         "CSV files (*.csv)")[0]
        print(fn)
        self.data_folder = os.path.dirname(fn)
        return

    def get_housing_chkbox(self):
        checked = self.cb_housing.isChecked()
        if checked and "housing" not in self.categories:
            self.categories.append("housing")
        else:
            if "housing" in self.categories:
                self.categories.remove("housing")
        return

    def get_utilities_chkbox(self):
        checked = self.cb_utilities.isChecked()
        if checked and "utilities" not in self.categories:
            self.categories.append("utilities")
        else:
            if "utilities" in self.categories:
                self.categories.remove("utilities")
        return

    def get_cellular_chkbox(self):
        checked = self.cb_cellular.isChecked()
        if checked and "cellular" not in self.categories:
            self.categories.append("cellular")
        else:
            if "cellular" in self.categories:
                self.categories.remove("cellular")
        return

    def get_insurance_chkbox(self):
        checked = self.cb_insurance.isChecked()
        if checked and "insurance" not in self.categories:
            self.categories.append("insurance")
        else:
            if "insurance" in self.categories:
                self.categories.remove("insurance")
        return

    def get_grocery_chkbox(self):
        checked = self.cb_grocery.isChecked()
        if checked and "grocery" not in self.categories:
            self.categories.append("grocery")
        else:
            if "grocery" in self.categories:
                self.categories.remove("grocery")
        return

    def get_transportation_chkbox(self):
        checked = self.cb_transportation.isChecked()
        if checked and "transportation" not in self.categories:
            self.categories.append("transportation")
        else:
            if "transportation" in self.categories:
                self.categories.remove("transportation")
        return

    def get_entertainment_chkbox(self):
        checked = self.cb_entertainment.isChecked()
        if checked and "entertainment" not in self.categories:
            self.categories.append("entertainment")
        else:
            if "entertainment" in self.categories:
                self.categories.remove("entertainment")
        return

    def get_miscellaneous_chkbox(self):
        checked = self.cb_miscellaneous.isChecked()
        if checked and "miscellaneous" not in self.categories:
            self.categories.append("miscellaneous")
        else:
            if "miscellaneous" in self.categories:
                self.categories.remove("miscellaneous")
        return

    def get_health_chkbox(self):
        checked = self.cb_health.isChecked()
        if checked and "health" not in self.categories:
            self.categories.append("health")
        else:
            if "health" in self.categories:
                self.categories.remove("health")
        return

    def get_retirement_chkbox(self):
        checked = self.cb_health.isChecked()
        if checked and "retirement" not in self.categories:
            self.categories.append("retirement")
        else:
            if "retirement" in self.categories:
                self.categories.remove("retirement")
        return

    def get_alcohol_chkbox(self):
        checked = self.cb_alcohol.isChecked()
        if checked and "alcohol" not in self.tags:
            self.tags.append("alcohol")
        else:
            if "alcohol" in self.tags:
                self.tags.remove("alcohol")
        return

    def get_books_chkbox(self):
        checked = self.cb_books.isChecked()
        if checked and "books" not in self.tags:
            self.tags.append("books")
        else:
            if "books" in self.tags:
                self.tags.remove("books")
        return

    def get_camping_chkbox(self):
        checked = self.cb_camping.isChecked()
        if checked and "camping" not in self.tags:
            self.tags.append("camping")
        else:
            if "camping" in self.tags:
                self.tags.remove("camping")
        return

    def get_climbing_chkbox(self):
        checked = self.cb_climbing.isChecked()
        if checked and "climbing" not in self.tags:
            self.tags.append("climbing")
        else:
            if "climbing" in self.tags:
                self.tags.remove("climbing")
        return

    def get_dining_chkbox(self):
        checked = self.cb_dining.isChecked()
        if checked and "dining" not in self.tags:
            self.tags.append("dining")
        else:
            if "dining" in self.tags:
                self.tags.remove("dining")
        return

    def get_electronics_chkbox(self):
        checked = self.cb_electronics.isChecked()
        if checked and "electronics" not in self.tags:
            self.tags.append("electronics")
        else:
            if "electronics" in self.tags:
                self.tags.remove("electronics")
        return

    def get_essentials_chkbox(self):
        checked = self.cb_essentials.isChecked()
        if checked and "essentials" not in self.tags:
            self.tags.append("essentials")
        else:
            if "essentials" in self.tags:
                self.tags.remove("essentials")
        return

    def get_flight_chkbox(self):
        checked = self.cb_flight.isChecked()
        if checked and "flight" not in self.tags:
            self.tags.append("flight")
        else:
            if "flight" in self.tags:
                self.tags.remove("flight")
        return

    def get_games_chkbox(self):
        checked = self.cb_games.isChecked()
        if checked and "games" not in self.tags:
            self.tags.append("games")
        else:
            if "games" in self.tags:
                self.tags.remove("games")
        return

    def get_gambling_chkbox(self):
        checked = self.cb_gambling.isChecked()
        if checked and "gambling" not in self.tags:
            self.tags.append("gambling")
        else:
            if "gambling" in self.tags:
                self.tags.remove("gambling")
        return

    def get_golf_chkbox(self):
        checked = self.cb_golf.isChecked()
        if checked and "golf" not in self.tags:
            self.tags.append("golf")
        else:
            if "golf" in self.tags:
                self.tags.remove("golf")
        return

    def get_grocery_tag_chkbox(self):
        checked = self.cb_grocery.isChecked()
        if checked and "grocery" not in self.tags:
            self.tags.append("grocery")
        else:
            if "grocery" in self.tags:
                self.tags.remove("grocery")
        return

    def get_gym_chkbox(self):
        checked = self.cb_gym.isChecked()
        if checked and "gym" not in self.tags:
            self.tags.append("gym")
        else:
            if "gym" in self.tags:
                self.tags.remove("gym")
        return

    def get_home_improvement_chkbox(self):
        checked = self.cb_home_improvement.isChecked()
        if checked and "Home_Improvement" not in self.tags:
            self.tags.append("Home_Improvement")
        else:
            if "home_improvement" in self.tags:
                self.tags.remove("Home_Improvement")
        return

    def get_medical_chkbox(self):
        checked = self.cb_medical.isChecked()
        if checked and "medical" not in self.tags:
            self.tags.append("medical")
        else:
            if "medical" in self.tags:
                self.tags.remove("medical")
        return

    def get_museum_chkbox(self):
        checked = self.cb_museum.isChecked()
        if checked and "museum" not in self.tags:
            self.tags.append("museum")
        else:
            if "museum" in self.tags:
                self.tags.remove("museum")
        return

    def get_photography_chkbox(self):
        checked = self.cb_photography.isChecked()
        if checked and "photography" not in self.tags:
            self.tags.append("photography")
        else:
            if "photography" in self.tags:
                self.tags.remove("photography")
        return

    def get_presents_chkbox(self):
        checked = self.cb_presents.isChecked()
        if checked and "presents" not in self.tags:
            self.tags.append("presents")
        else:
            if "presents" in self.tags:
                self.tags.remove("presents")
        return

    def get_self_care_chkbox(self):
        checked = self.cb_self_care.isChecked()
        if checked and "Self_Care" not in self.tags:
            self.tags.append("Self_Care")
        else:
            if "Self_Care" in self.tags:
                self.tags.remove("Self_Care")
        return

    def get_services_chkbox(self):
        checked = self.cb_services.isChecked()
        if checked and "services" not in self.tags:
            self.tags.append("services")
        else:
            if "services" in self.tags:
                self.tags.remove("services")
        return

    def get_skiing_chkbox(self):
        checked = self.cb_skiing.isChecked()
        if checked and "skiing" not in self.tags:
            self.tags.append("skiing")
        else:
            if "skiing" in self.tags:
                self.tags.remove("skiing")
        return

    def get_sports_chkbox(self):
        checked = self.cb_sports.isChecked()
        if checked and "sports" not in self.tags:
            self.tags.append("sports")
        else:
            if "sports" in self.tags:
                self.tags.remove("sports")
        return

    def get_transportation_tag_chkbox(self):
        checked = self.cb_transportation_tag.isChecked()
        if checked and "transportation" not in self.tags:
            self.tags.append("transportation")
        else:
            if "transportation" in self.tags:
                self.tags.remove("transportation")
        return

    def get_travel_chkbox(self):
        checked = self.cb_travel.isChecked()
        if checked and "travel" not in self.tags:
            self.tags.append("travel")
        else:
            if "travel" in self.tags:
                self.tags.remove("travel")
        return

    def get_retirement_tag_chkbox(self):
        checked = self.cb_health.isChecked()
        if checked and "retirement" not in self.categories:
            self.categories.append("retirement")
        else:
            if "retirement" in self.categories:
                self.categories.remove("retirement")
        return

    def get_month_start(self):
        self.month_start = int(self.sb_month_start.value())
        return

    def get_month_end(self):
        self.month_end = int(self.sb_month_end.value())
        return

    def get_year_start(self):
        self.year_start = int(self.sb_year_start.value())
        return

    def get_year_end(self):
        self.year_end = int(self.sb_year_end.value())
        return

    def plot(self):
        if self.year_start < self.year_end:
            years = [*range(self.year_start, self.year_end+1)]
        else:
            years = [self.year_end]
        salary_df = vb.get_salary(years, self.data_folder)
        dfs = []
        for year in years:
            fn = glob.glob(os.path.join(self.data_folder, f"{year}.csv"))[0]
            dfs.append(pd.read_csv(fn))

        df = dfs[0]
        for i in range(1, len(years)):
            df = df.append(dfs[i])
        df = df.reset_index(drop=True)
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
        date_start = datetime.datetime(self.year_start, self.month_start, 1)
        date_end = datetime.datetime(self.year_end, self.month_end, 30)
        df = df.loc[(df["Date"] > date_start) & (df["Date"] < date_end)]
        df = vb.group_major(df)
        self.p_category.make_plot(df, "Category", salary_df, self.categories)
        self.p_category.update()
        self.p_tag.make_plot(df, "Tag", salary_df, self.tags)
        self.p_tag.update()
        self.p_major.make_plot(df, "Major", salary_df)
        self.p_major.update()
        df_frivolous = df.loc[(df.Major == "Frivolous"), :]
        self.p_frivolous.make_plot(df_frivolous, "Tag")
        self.p_frivolous.update()
        return

    def update_data(self):
        if self.year_start < self.year_end:
            years = [*range(self.year_start, self.year_end+1)]
        else:
            years = [self.year_end]
        df_year = pd.DataFrame(columns=[
            "Place", "Date", "Category",
            "Price", "Description", "Tag"])

        for year in years:
            f = glob.glob(os.path.join(self.data_folder, f"*{year}.xlsx"))[0]
            df_year = b2c.import_odf(f, year)
            df_year.to_csv(os.path.join(self.data_folder, f"{year}.csv"),
                           index=False)
        return

def main():
    """Main entry point for Plot RCS app."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowTitle("Budget")
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
