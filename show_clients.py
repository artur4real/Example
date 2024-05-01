import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QApplication
import pymysql


class ShowClientsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Показ клиентов")

        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.refresh_button = QPushButton("Обновить")
        layout.addWidget(self.refresh_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.refresh_button.clicked.connect(self.refresh_clients)

    def refresh_clients(self):
        """Отображение списка клиентов в таблице"""
        self.result_table.setRowCount(0)
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "SELECT * FROM Clients"
        cursor.execute(query)
        clients = cursor.fetchall()
        if clients:
            self.result_table.setColumnCount(len(clients[0]))
            self.result_table.setHorizontalHeaderLabels(["ID клиента", "ФИО", "Адрес"])
            for row_number, client in enumerate(clients):
                self.result_table.insertRow(row_number)
                for column_number, data in enumerate(client):
                    self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShowClientsWindow()
    window.show()
    sys.exit(app.exec_())
