import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox
import pymysql


class AddEditClientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Изменить клиента")

        layout = QVBoxLayout()

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Имя клиента")
        layout.addWidget(self.client_name_input)

        self.client_address_input = QLineEdit()
        self.client_address_input.setPlaceholderText("Адрес клиента")
        layout.addWidget(self.client_address_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(layout)

    def get_data(self):
        """Получить данные, введенные пользователем"""
        return self.client_name_input.text(), self.client_address_input.text()


class AddEditWorkerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Изменить работника")

        layout = QVBoxLayout()

        self.worker_name_input = QLineEdit()
        self.worker_name_input.setPlaceholderText("Имя работника")
        layout.addWidget(self.worker_name_input)

        self.worker_qualification_input = QLineEdit()
        self.worker_qualification_input.setPlaceholderText("Квалификация работника")
        layout.addWidget(self.worker_qualification_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(layout)

    def get_data(self):
        """Получить данные, введенные пользователем"""
        return self.worker_name_input.text(), self.worker_qualification_input.text()


class AddEditOrderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Изменить заказ")

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

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(layout)

    def get_data(self):
        """Получить данные, введенные пользователем"""
        return self.client_id_input.text(), self.worker_id_input.text(), self.work_type_input.text(), self.payment_input.text()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление автомастерской")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Создание кнопок для отображения клиентов, работников и заказов
        self.client_button = QPushButton("Показать клиентов")
        self.client_button.clicked.connect(self.show_clients)
        layout.addWidget(self.client_button)

        self.worker_button = QPushButton("Показать работников")
        self.worker_button.clicked.connect(self.show_workers)
        layout.addWidget(self.worker_button)

        self.order_button = QPushButton("Показать заказы")
        self.order_button.clicked.connect(self.show_orders)
        layout.addWidget(self.order_button)

        # Создание таблицы для отображения результатов
        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        # Кнопки для добавления, изменения и удаления клиентов, работников и заказов
        self.add_client_button = QPushButton("Добавить клиента")
        self.add_client_button.clicked.connect(self.add_client)
        layout.addWidget(self.add_client_button)

        self.edit_client_button = QPushButton("Изменить клиента")
        self.edit_client_button.clicked.connect(self.edit_client)
        layout.addWidget(self.edit_client_button)

        self.delete_client_button = QPushButton("Удалить клиента")
        self.delete_client_button.clicked.connect(self.delete_client)
        layout.addWidget(self.delete_client_button)

        self.add_worker_button = QPushButton("Добавить работника")
        self.add_worker_button.clicked.connect(self.add_worker)
        layout.addWidget(self.add_worker_button)

        self.edit_worker_button = QPushButton("Изменить работника")
        self.edit_worker_button.clicked.connect(self.edit_worker)
        layout.addWidget(self.edit_worker_button)

        self.delete_worker_button = QPushButton("Удалить работника")
        self.delete_worker_button.clicked.connect(self.delete_worker)
        layout.addWidget(self.delete_worker_button)

        self.add_order_button = QPushButton("Добавить заказ")
        self.add_order_button.clicked.connect(self.add_order)
        layout.addWidget(self.add_order_button)

        self.edit_order_button = QPushButton("Изменить заказ")
        self.edit_order_button.clicked.connect(self.edit_order)
        layout.addWidget(self.edit_order_button)

        self.delete_order_button = QPushButton("Удалить заказ")
        self.delete_order_button.clicked.connect(self.delete_order)
        layout.addWidget(self.delete_order_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключение к базе данных
        self.db_connection = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        self.cursor = self.db_connection.cursor()

    # Методы для работы с клиентами, работниками и заказами
    def show_clients(self):
        """Отображение списка клиентов в таблице"""
        self.result_table.setRowCount(0)
        query = "SELECT * FROM Clients"
        self.cursor.execute(query)
        clients = self.cursor.fetchall()
        if clients:
            self.result_table.setColumnCount(len(clients[0]))
            self.result_table.setHorizontalHeaderLabels(["ID клиента", "ФИО", "Адрес"])
            for row_number, client in enumerate(clients):
                self.result_table.insertRow(row_number)
                for column_number, data in enumerate(client):
                    self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def show_workers(self):
        """Отображение списка работников в таблице"""
        self.result_table.setRowCount(0)
        query = "SELECT * FROM Workers"
        self.cursor.execute(query)
        workers = self.cursor.fetchall()
        if workers:
            self.result_table.setColumnCount(len(workers[0]))
            self.result_table.setHorizontalHeaderLabels(["ID работника", "ФИО", "Квалификация"])
            for row_number, worker in enumerate(workers):
                self.result_table.insertRow(row_number)
                for column_number, data in enumerate(worker):
                    self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def show_orders(self):
        """Отображение списка заказов в таблице"""
        self.result_table.setRowCount(0)
        query = "SELECT * FROM Orders"
        self.cursor.execute(query)
        orders = self.cursor.fetchall()
        if orders:
            self.result_table.setColumnCount(len(orders[0]))
            self.result_table.setHorizontalHeaderLabels(["ID заказа", "ID клиента", "ID работника", "Тип работы", "Оплата"])
            for row_number, order in enumerate(orders):
                self.result_table.insertRow(row_number)
                for column_number, data in enumerate(order):
                    self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    # Методы для добавления, изменения и удаления клиентов, работников и заказов
    def add_client(self):
        """Добавление нового клиента"""
        dialog = AddEditClientDialog()
        if dialog.exec_() == QDialog.Accepted:
            client_name, client_address = dialog.get_data()
            query = "INSERT INTO Clients (FullName, Address) VALUES (%s, %s)"
            self.cursor.execute(query, (client_name, client_address))
            self.db_connection.commit()
            self.show_clients()

    def edit_client(self):
        """Изменение информации о клиенте"""
        row = self.result_table.currentRow()
        if row != -1:
            dialog = AddEditClientDialog()
            client_id = self.result_table.item(row, 0).text()
            client_name = self.result_table.item(row, 1).text()
            client_address = self.result_table.item(row, 2).text()
            dialog.client_name_input.setText(client_name)
            dialog.client_address_input.setText(client_address)
            if dialog.exec_() == QDialog.Accepted:
                new_client_name, new_client_address = dialog.get_data()
                query = "UPDATE Clients SET FullName = %s, Address = %s WHERE ClientID = %s"
                self.cursor.execute(query, (new_client_name, new_client_address, client_id))
                self.db_connection.commit()
                self.show_clients()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите клиента для изменения.")

    def delete_client(self):
        """Удаление клиента"""
        row = self.result_table.currentRow()
        if row != -1:
            client_id = self.result_table.item(row, 0).text()
            reply = QMessageBox.question(self, 'Удалить клиента', 'Вы уверены, что хотите удалить этого клиента?',
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                query = "DELETE FROM Clients WHERE ClientID = %s"
                self.cursor.execute(query, (client_id,))
                self.db_connection.commit()
                self.show_clients()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите клиента для удаления.")

    def add_worker(self):
        """Добавление нового работника"""
        dialog = AddEditWorkerDialog()
        if dialog.exec_() == QDialog.Accepted:
            worker_name, worker_qualification = dialog.get_data()
            query = "INSERT INTO Workers (FullName, Qualification) VALUES (%s, %s)"
            self.cursor.execute(query, (worker_name, worker_qualification))
            self.db_connection.commit()
            self.show_workers()

    def edit_worker(self):
        """Изменение информации о работнике"""
        row = self.result_table.currentRow()
        if row != -1:
            dialog = AddEditWorkerDialog()
            worker_id = self.result_table.item(row, 0).text()
            worker_name = self.result_table.item(row, 1).text()
            worker_qualification = self.result_table.item(row, 2).text()
            dialog.worker_name_input.setText(worker_name)
            dialog.worker_qualification_input.setText(worker_qualification)
            if dialog.exec_() == QDialog.Accepted:
                new_worker_name, new_worker_qualification = dialog.get_data()
                query = "UPDATE Workers SET FullName = %s, Qualification = %s WHERE WorkerID = %s"
                self.cursor.execute(query, (new_worker_name, new_worker_qualification, worker_id))
                self.db_connection.commit()
                self.show_workers()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите работника для изменения.")

    def delete_worker(self):
        """Удаление работника"""
        row = self.result_table.currentRow()
        if row != -1:
            worker_id = self.result_table.item(row, 0).text()
            reply = QMessageBox.question(self, 'Удалить работника', 'Вы уверены, что хотите удалить этого работника?',
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                query = "DELETE FROM Workers WHERE WorkerID = %s"
                self.cursor.execute(query, (worker_id,))
                self.db_connection.commit()
                self.show_workers()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите работника для удаления.")

    def add_order(self):
        """Добавление нового заказа"""
        dialog = AddEditOrderDialog()
        if dialog.exec_() == QDialog.Accepted:
            client_id, worker_id, work_type, payment = dialog.get_data()
            query = "INSERT INTO Orders (ClientID, WorkerID, WorkType, Payment) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (client_id, worker_id, work_type, payment))
            self.db_connection.commit()
            self.show_orders()

    def edit_order(self):
        """Изменение информации о заказе"""
        row = self.result_table.currentRow()
        if row != -1:
            dialog = AddEditOrderDialog()
            order_id = self.result_table.item(row, 0).text()
            client_id = self.result_table.item(row, 1).text()
            worker_id = self.result_table.item(row, 2).text()
            work_type = self.result_table.item(row, 3).text()
            payment = self.result_table.item(row, 4).text()
            dialog.client_id_input.setText(client_id)
            dialog.worker_id_input.setText(worker_id)
            dialog.work_type_input.setText(work_type)
            dialog.payment_input.setText(payment)
            if dialog.exec_() == QDialog.Accepted:
                new_client_id, new_worker_id, new_work_type, new_payment = dialog.get_data()
                query = "UPDATE Orders SET ClientID = %s, WorkerID = %s, WorkType = %s, Payment = %s WHERE OrderID = %s"
                self.cursor.execute(query, (new_client_id, new_worker_id, new_work_type, new_payment, order_id))
                self.db_connection.commit()
                self.show_orders()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите заказ для изменения.")

    def delete_order(self):
        """Удаление заказа"""
        row = self.result_table.currentRow()
        if row != -1:
            order_id = self.result_table.item(row, 0).text()
            reply = QMessageBox.question(self, 'Удалить заказ', 'Вы уверены, что хотите удалить этот заказ?',
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                query = "DELETE FROM Orders WHERE OrderID = %s"
                self.cursor.execute(query, (order_id,))
                self.db_connection.commit()
                self.show_orders()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите заказ для удаления.")

    def closeEvent(self, event):
        """Закрытие приложения и отключение от базы данных"""
        self.db_connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
