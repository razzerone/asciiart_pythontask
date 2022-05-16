import sys

from PyQt6.QtWidgets import QMainWindow, QApplication

from ASCIIArtGUI.start_widget import StartWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            'ASCII-art program by Sopegin Kirill and Kondratov Daniil'
        )
        self.move(300, 300)
        self.resize(300, 300)

        central_widget = StartWidget()
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()
    win.setStyleSheet(
            "QWidget {background-color: rgba(126,41,59,255);} "
            "QScrollBar:horizontal "
            "{width: 1px; height: 1px; background-color: rgba(0,41,59,255);} "
            "QScrollBar:vertical "
            "{width: 1px; height: 1px; background-color: rgba(0,41,59,255);}"
            "QPushButton { background-color: #b5e6e1 }"
            "QPushButton:pressed { background-color: #51FFFF }"
    )
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
