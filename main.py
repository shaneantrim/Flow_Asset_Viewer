import shotgun_api3
from pprint import pprint # useful for debugging

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox
from shotgun_api3 import Shotgun

# Configuration information to connect to the Flow site
SHOTGUN_URL = "https://shane-shotgrid.shotgrid.autodesk.com"
SCRIPT_NAME = "Asset_Data_Tool"
SCRIPT_KEY = "Inlsjiyni1jcmpuq*jzxkmhgu"

# Function to try connecting to the Flow site
def get_shotgun_connection():
    try:
        sg = Shotgun(SHOTGUN_URL, SCRIPT_NAME, SCRIPT_KEY)
        print("Successfully connected to Shotgun.")
        return sg
    except Exception as e:
        print("Error connecting to Shotgun:", e)
        raise

# Function to fetch project ID by name
def fetch_project_id(sg, project_name):
    try:
        filters = [['name', 'is', project_name]]
        fields = ['id']
        projects = sg.find('Project', filters, fields)
        if projects:
            project_id = projects[0]['id']
            print(f"Project ID for '{project_name}':", project_id)
            return project_id
        else:
            print(f"No project found with the name '{project_name}'")
            return None
    except Exception as e:
        print("Error fetching project ID:", e)
        raise

# Function to fetch all assets for project ID
def fetch_all_assets_for_project(sg, project_id):
    try:
        filters = [['project', 'is', {'type': 'Project', 'id': project_id}]]
        fields = ['id', 'code', 'sg_asset_type', 'description']
        assets = sg.find('Asset', filters, fields)
        print(f"Assets for project ID {project_id}:", assets)
        return assets
    except Exception as e:
        print("Error fetching assets:", e)
        raise

# Main window class to display PySide window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shotgun Asset Viewer")
        self.setGeometry(1500, 1500, 1500, 1600)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Name", "Type", "Description"])

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def populate_table(self, data):
        self.table_widget.setRowCount(len(data))
        for row_num, asset in enumerate(data):
            self.table_widget.setItem(row_num, 0, QTableWidgetItem(str(asset['id'])))
            self.table_widget.setItem(row_num, 1, QTableWidgetItem(asset['code']))
            self.table_widget.setItem(row_num, 2, QTableWidgetItem(asset.get('sg_asset_type', 'N/A')))
            self.table_widget.setItem(row_num, 3, QTableWidgetItem(asset.get('description', 'N/A')))
        self.table_widget.resizeColumnsToContents()

# Main function to fetch assets for project ID and populate table
def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    try:
        sg = get_shotgun_connection()
        project_name = "Demo: Animation"
        sequence_id = 2  # Example sequence ID
        project_id = fetch_project_id(sg, project_name)
        if project_id:
            asset_data = fetch_all_assets_for_project(sg, project_id)
            print("Asset data received in main.py:", asset_data)
            main_window.populate_table(asset_data)
        else:
            print(f"Project '{project_name}' not found.")
    except Exception as e:
        print("Error fetching data in main.py:", e)

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
