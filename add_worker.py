import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QApplication
import pymysql


class AddWorkerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить работника")

        layout = QVBoxLayout()

        self.worker_name_input = QLineEdit()
        self.worker_name_input.setPlaceholderText("Имя работника")
        layout.addWidget(self.worker_name_input)

        self.worker_qualification_input = QLineEdit()
        self.worker_qualification_input.setPlaceholderText("Квалификация работника")
        layout.addWidget(self.worker_qualification_input)

        self.add_button = QPushButton("Добавить")
        layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_worker)

        self.setLayout(layout)

    def add_worker(self):
        """Добавление нового работника"""
        worker_name = self.worker_name_input.text()
        worker_qualification = self.worker_qualification_input.text()
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "INSERT INTO Workers (FullName, Qualification) VALUES (%s, %s)"
        cursor.execute(query, (worker_name, worker_qualification))
        db.commit()
        db.close()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AddWorkerDialog()
    dialog.show()
    sys.exit(app.exec_())
