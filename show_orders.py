import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QApplication
import pymysql


class ShowOrdersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Показ заказов")

        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.refresh_button = QPushButton("Обновить")
        layout.addWidget(self.refresh_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.refresh_button.clicked.connect(self.refresh_orders)

    def refresh_orders(self):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShowOrdersWindow()
    window.show()
    sys.exit(app.exec_())
