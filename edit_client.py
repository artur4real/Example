import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem,QApplication, QDialog, QLineEdit
import pymysql


class ShowClientsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Показ клиентов")

        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.edit_button = QPushButton("Изменить клиента")
        layout.addWidget(self.edit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.edit_button.clicked.connect(self.edit_client_dialog)
        self.show_clients()

    def show_clients(self):
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

    def edit_client_dialog(self):
        """Отображение диалогового окна для редактирования клиента"""
        selected_row = self.result_table.currentRow()
        if selected_row != -1:
            client_id = int(self.result_table.item(selected_row, 0).text())
            client_name = self.result_table.item(selected_row, 1).text()
            client_address = self.result_table.item(selected_row, 2).text()
            dialog = EditClientDialog(client_id, client_name, client_address)
            dialog.exec_()
            self.show_clients()


class EditClientDialog(QDialog):
    def __init__(self, client_id, client_name, client_address):
        super().__init__()
        self.setWindowTitle("Изменить информацию о клиенте")

        layout = QVBoxLayout()

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Имя клиента")
        self.client_name_input.setText(client_name)
        layout.addWidget(self.client_name_input)

        self.client_address_input = QLineEdit()
        self.client_address_input.setPlaceholderText("Адрес клиента")
        self.client_address_input.setText(client_address)
        layout.addWidget(self.client_address_input)

        self.save_button = QPushButton("Сохранить")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.edit_client)

        self.client_id = client_id

        self.setLayout(layout)

    def edit_client(self):
        """Изменение информации о клиенте"""
        new_client_name = self.client_name_input.text()
        new_client_address = self.client_address_input.text()
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "UPDATE Clients SET FullName = %s, Address = %s WHERE ClientID = %s"
        cursor.execute(query, (new_client_name, new_client_address, self.client_id))
        db.commit()
        db.close()
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShowClientsWindow()
    window.show()
    sys.exit(app.exec_())
