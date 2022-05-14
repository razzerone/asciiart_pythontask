import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

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
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
