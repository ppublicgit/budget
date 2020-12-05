import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from budget_ui import Ui_MplMainWindow
import view_budget as vb


class MainWindow(QMainWindow, Ui_MplMainWindow):
    """Primary GUI window."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.data_folder = None
        self.categories = []
        self.tags = []

        self.setup_gui()

    def setup_gui(self):
        self.actionData_Folder.triggered.connect(self.get_data_folder)
        self.cb_housing.stateChanged.connect(self.get_housing_chkbox)
        self.cb_utilities.stateChanged.connect(self.get_utilities_chkbox)
        self.cb_cellular.stateChanged.connect(self.get_cellular_chkbox)
        self.cb_insurance.stateChanged.connect(self.get_insurance_chkbox)
        self.cb_grocery.stateChanged.connect(self.get_grocery_chkbox)
        self.cb_transportation.stateChanged.connect(self.get_transportation_chkbox)
        self.cb_entertainment.stateChanged.connect(self.get_entertainment_chkbox)
        self.cb_miscellaneous.stateChanged.connect(self.get_miscellaneous_chkbox)
        self.cb_health.stateChanged.connect(self.get_health_chkbox)
        self.cb_alcohol.stateChanged.connect(self.get_alcohol_chkbox)
        self.cb_books.stateChanged.connect(self.get_books_chkbox)
        self.cb_camping.stateChanged.connect(self.get_camping_chkbox)
        self.cb_climbing.stateChanged.connect(self.get_climbing_chkbox)
        self.cb_dining.stateChanged.connect(self.get_dining_chkbox)
        self.cb_electronics.stateChanged.connect(self.get_electronics_chkbox)
        self.cb_essentials.stateChanged.connect(self.get_essentials_chkbox)
        self.cb_flight.stateChanged.connect(self.get_flight_chkbox)
        self.cb_games.stateChanged.connect(self.get_games_chkbox)
        self.cb_gambling.stateChanged.connect(self.get_gambling_chkbox)
        self.cb_golf.stateChanged.connect(self.get_golf_chkbox)
        self.cb_grocery.stateChanged.connect(self.get_grocery_chkbox)
        self.cb_gym.stateChanged.connect(self.get_gym_chkbox)
        self.cb_home_improvement.stateChanged.connect(self.get_home_improvement_chkbox)
        self.cb_medical.stateChanged.connect(self.get_medical_chkbox)
        self.cb_museum.stateChanged.connect(self.get_museum_chkbox)
        self.cb_photography.stateChanged.connect(self.get_photography_chkbox)
        self.cb_presents.stateChanged.connect(self.get_presents_chkbox)
        self.cb_self_care.stateChanged.connect(self.get_self_care_chkbox)
        self.cb_services.stateChanged.connect(self.get_services_chkbox)
        self.cb_skiing.stateChanged.connect(self.get_skiing_chkbox)
        self.cb_sports.stateChanged.connect(self.get_sports_chkbox)
        self.cb_transportation_tag.stateChanged.connect(self.get_transportation_tag_chkbox)
        self.cb_travel.stateChanged.connect(self.get_travel_chkbox)


    def get_data_folder(self):
        fn = QFileDialog.getOpenFileName(None, u"Select File for Folder Path", "",
                                         "CSV files (*.csv)")

        self.data_folder = os.path.basename(fn)
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
        if checked and "books" not in self.ta:
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


    def get_grocery_chkbox(self):
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
        if checked and "home_improvement" not in self.tags:
            self.tags.append("home_improvement")
        else:
            if "home_improvement" in self.tags:
                self.tags.remove("home_improvement")
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
        if checked and "self_care" not in self.tags:
            self.tags.append("self_care")
        else:
            if "self_care" in self.tags:
                self.tags.remove("self_care")
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
        if checked and "transportation_tag" not in self.tags:
            self.tags.append("transportation_tag")
        else:
            if "transportation_tag" in self.tags:
                self.tags.remove("transportation_tag")
        return


    def get_travel_chkbox(self):
        checked = self.cb_travel.isChecked()
        if checked and "travel" not in self.tags:
            self.tags.append("travel")
        else:
            if "travel" in self.tags:
                self.tags.remove("travel")
        return



def main():
    """Main entry point for Plot RCS app."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowTitle("Plot RCS")
    main_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
