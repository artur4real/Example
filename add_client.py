import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QApplication, QWidget
import pymysql


class AddClientDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить клиента")

        layout = QVBoxLayout()

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Имя клиента")
        layout.addWidget(self.client_name_input)

        self.client_address_input = QLineEdit()
        self.client_address_input.setPlaceholderText("Адрес клиента")
        layout.addWidget(self.client_address_input)

        self.add_button = QPushButton("Добавить")
        layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_client)

        self.setLayout(layout)

    def add_client(self):
        """Добавление нового клиента"""
        client_name = self.client_name_input.text()
        client_address = self.client_address_input.text()
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "INSERT INTO Clients (FullName, Address) VALUES (%s, %s)"
        cursor.execute(query, (client_name, client_address))
        db.commit()
        db.close()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AddClientDialog()
    dialog.show()
    sys.exit(app.exec_())
