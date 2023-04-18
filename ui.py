import os
import sys
from threading import Thread

from PySide6.QtCore import Qt
from PySide6 import QtCore, QtWidgets

import read_csv
import config
import log


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        config.load()
        api_key = config.get_api_key()

        # 创建 Api Key 标签和输入框
        apikey_label = QtWidgets.QLabel("Please input your API key:", self)
        apikey_label.setGeometry(50, 50, 200, 30)
        self.apikey_input = QtWidgets.QLineEdit(self)
        # 将API密钥输入框设置为密码模式
        self.apikey_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.apikey_input.setGeometry(50, 80, 300, 30)

        self.apikey_input.setText(api_key)

        # 创建选择CSV文件按钮和标签
        self.select_csv_button = QtWidgets.QPushButton("Select CSV file", self)
        self.select_csv_button.setGeometry(50, 150, 140, 30)
        self.select_csv_button.clicked.connect(
            self.on_select_csv_button_clicked)

        self.selected_csv_label = QtWidgets.QLabel(self)
        self.selected_csv_label.setGeometry(200, 150, 250, 30)
        self.selected_csv_label.setAlignment(Qt.AlignLeft)
        # self.selected_csv_label.setStyleSheet("background-color: white;")

        self.button = QtWidgets.QPushButton("启动", self)
        self.button.setGeometry(50, 200, 80, 30)
        self.button.clicked.connect(self.start)

    def on_select_csv_button_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select CSV file", "",
            "CSV Files (*.csv)", options=options)
        if file_name:
            self.selected_csv_label.setText(os.path.basename(file_name))

    def save_config(self):
        api_key = self.apikey_input.text()
        config.set_api_key(api_key)
        config.save()

    @QtCore.Slot()
    def start(self):
        api_key = self.apikey_input.text()
        csv_file_path = self.selected_csv_label.text()
        if not csv_file_path:
            msg = "请选择一个csv文件"
            log.logger.warning(msg)
            self.showMessageBox(msg)
            return
        try:
            questions = read_csv.read_questions(csv_file_path)
        except Exception as e:
            msg = f"An error occurred while reading the CSV file: {e}"
            log.logger.warning(msg)
            self.showMessageBox(msg)
            return
        # log.logger.info(f'一共读取到{len(questions)}组问题')

        from main import start
        t = Thread(target=start, args=(api_key, csv_file_path), daemon=True)
        t.start()
        log.logger.info('启动')

        self.save_config()
        self.button.setEnabled(False)
        self.select_csv_button.setEnabled(False)
        self.apikey_input.setEnabled(False)

    def showMessageBox(self, msg):
        log.logger.warnning(msg)
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(msg)
        msgBox.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    widget.setWindowTitle("auto-42share")
    # 设置窗口置顶
    # widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    log.logger.info('程序启动')
    sys.exit(app.exec())
