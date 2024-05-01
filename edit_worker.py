import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QApplication, QDialog, QLineEdit
import pymysql


class ShowWorkersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Показ работников")

        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.edit_button = QPushButton("Изменить работника")
        layout.addWidget(self.edit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.edit_button.clicked.connect(self.edit_worker_dialog)
        self.show_workers()

    def show_workers(self):
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

    def edit_worker_dialog(self):
        """Отображение диалогового окна для редактирования работника"""
        selected_row = self.result_table.currentRow()
        if selected_row != -1:
            worker_id = int(self.result_table.item(selected_row, 0).text())
            worker_name = self.result_table.item(selected_row, 1).text()
            worker_qualification = self.result_table.item(selected_row, 2).text()
            dialog = EditWorkerDialog(worker_id, worker_name, worker_qualification)
            dialog.exec_()
            self.show_workers()


class EditWorkerDialog(QDialog):
    def __init__(self, worker_id, worker_name, worker_qualification):
        super().__init__()
        self.setWindowTitle("Изменить информацию о работнике")

        layout = QVBoxLayout()

        self.worker_name_input = QLineEdit()
        self.worker_name_input.setPlaceholderText("Имя работника")
        self.worker_name_input.setText(worker_name)
        layout.addWidget(self.worker_name_input)

        self.worker_qualification_input = QLineEdit()
        self.worker_qualification_input.setPlaceholderText("Квалификация работника")
        self.worker_qualification_input.setText(worker_qualification)
        layout.addWidget(self.worker_qualification_input)

        self.save_button = QPushButton("Сохранить")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.edit_worker)

        self.worker_id = worker_id

        self.setLayout(layout)

    def edit_worker(self):
        """Изменение информации о работнике"""
        new_worker_name = self.worker_name_input.text()
        new_worker_qualification = self.worker_qualification_input.text()
        db = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = db.cursor()
        query = "UPDATE Workers SET FullName = %s, Qualification = %s WHERE WorkerID = %s"
        cursor.execute(query, (new_worker_name, new_worker_qualification, self.worker_id))
        db.commit()
        db.close()
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShowWorkersWindow()
    window.show()
    sys.exit(app.exec_())
