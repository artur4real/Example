import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QApplication
import pymysql


class ShowWorkersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Показ работников")

        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.refresh_button = QPushButton("Обновить")
        layout.addWidget(self.refresh_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.refresh_button.clicked.connect(self.refresh_workers)

    def refresh_workers(self):
        """Отображение списка работников в таблице"""
        self.result_table.setRowCount(0)
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "SELECT * FROM Workers"
        cursor.execute(query)
        workers = cursor.fetchall()
        if workers:
            self.result_table.setColumnCount(len(workers[0]))
            self.result_table.setHorizontalHeaderLabels(["ID работника", "ФИО", "Квалификация"])
            for row_number, worker in enumerate(workers):
                self.result_table.insertRow(row_number)
                for column_number, data in enumerate(worker):
                    self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShowWorkersWindow()
    window.show()
    sys.exit(app.exec_())
