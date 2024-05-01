import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QApplication
import pymysql


class AddOrderDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить заказ")

        layout = QVBoxLayout()

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("ID клиента")
        layout.addWidget(self.client_id_input)

        self.worker_id_input = QLineEdit()
        self.worker_id_input.setPlaceholderText("ID работника")
        layout.addWidget(self.worker_id_input)

        self.work_type_input = QLineEdit()
        self.work_type_input.setPlaceholderText("Тип работы")
        layout.addWidget(self.work_type_input)

        self.payment_input = QLineEdit()
        self.payment_input.setPlaceholderText("Оплата")
        layout.addWidget(self.payment_input)

        self.add_button = QPushButton("Добавить")
        layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_order)

        self.setLayout(layout)

    def add_order(self):
        """Добавление нового заказа"""
        client_id = self.client_id_input.text()
        worker_id = self.worker_id_input.text()
        work_type = self.work_type_input.text()
        payment = self.payment_input.text()
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "INSERT INTO Orders (ClientID, WorkerID, WorkType, Payment) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (client_id, worker_id, work_type, payment))
        db.commit()
        db.close()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AddOrderDialog()
    dialog.show()
    sys.exit(app.exec_())
