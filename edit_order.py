import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, \
    QApplication, QDialog, QLineEdit
import pymysql


class ShowOrdersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Показ заказов")

        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.edit_button = QPushButton("Изменить заказ")
        layout.addWidget(self.edit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.edit_button.clicked.connect(self.edit_order_dialog)
        self.show_orders()

    def show_orders(self):
        """Отображение списка заказов в таблице"""
        self.result_table.setRowCount(0)
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "SELECT * FROM Orders"
        cursor.execute(query)
        orders = cursor.fetchall()
        if orders:
            self.result_table.setColumnCount(len(orders[0]))
            self.result_table.setHorizontalHeaderLabels(
                ["ID заказа", "ID клиента", "ID работника", "Тип работы", "Оплата"])
            for row_number, order in enumerate(orders):
                self.result_table.insertRow(row_number)
                for column_number, data in enumerate(order):
                    self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        db.close()

    def edit_order_dialog(self):
        """Отображение диалогового окна для редактирования заказа"""
        selected_row = self.result_table.currentRow()
        if selected_row != -1:
            order_id = int(self.result_table.item(selected_row, 0).text())
            client_id = self.result_table.item(selected_row, 1).text()
            worker_id = self.result_table.item(selected_row, 2).text()
            work_type = self.result_table.item(selected_row, 3).text()
            payment = self.result_table.item(selected_row, 4).text()
            dialog = EditOrderDialog(order_id, client_id, worker_id, work_type, payment)
            dialog.exec_()
            self.show_orders()


class EditOrderDialog(QDialog):
    def __init__(self, order_id, client_id, worker_id, work_type, payment):
        super().__init__()
        self.setWindowTitle("Изменить информацию о заказе")

        layout = QVBoxLayout()

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("ID клиента")
        self.client_id_input.setText(client_id)
        layout.addWidget(self.client_id_input)

        self.worker_id_input = QLineEdit()
        self.worker_id_input.setPlaceholderText("ID работника")
        self.worker_id_input.setText(worker_id)
        layout.addWidget(self.worker_id_input)

        self.work_type_input = QLineEdit()
        self.work_type_input.setPlaceholderText("Тип работы")
        self.work_type_input.setText(work_type)
        layout.addWidget(self.work_type_input)

        self.payment_input = QLineEdit()
        self.payment_input.setPlaceholderText("Оплата")
        self.payment_input.setText(payment)
        layout.addWidget(self.payment_input)

        self.save_button = QPushButton("Сохранить")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.edit_order)

        self.order_id = order_id

        self.setLayout(layout)

    def edit_order(self):
        """Изменение информации о заказе"""
        new_client_id = self.client_id_input.text()
        new_worker_id = self.worker_id_input.text()
        new_work_type = self.work_type_input.text()
        new_payment = self.payment_input.text()
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "UPDATE Orders SET ClientID = %s, WorkerID = %s, WorkType = %s, Payment = %s WHERE OrderID = %s"
        cursor.execute(query, (new_client_id, new_worker_id, new_work_type, new_payment, self.order_id))
        db.commit()
        db.close()
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShowOrdersWindow()
    window.show()
    sys.exit(app.exec_())
