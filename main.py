import matplotlib.pyplot as plt
import networkx as nx
import PyQt6

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        self.setMinimumSize(QSize(400,300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)
        
    def the_button_was_clicked(self):
        print("The button was clicked!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()