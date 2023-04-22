import os
import sys
from threading import Thread

from PySide6.QtCore import Qt
from PySide6 import QtCore, QtWidgets, QtGui

import read_csv
import config
import log

import __version__
APP_NAME = f'auto-42share-{__version__.VERSION}'


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        config.load()
        api_key = config.get_api_key()
        interval = config.get_send_message_interval()

        # 创建 Api Key 标签和输入框
        apikey_label = QtWidgets.QLabel("请输入API key:", self)
        apikey_label.setGeometry(50, 50, 200, 30)
        self.apikey_input = QtWidgets.QLineEdit(self)
        # 将API密钥输入框设置为密码模式
        self.apikey_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.apikey_input.setGeometry(50, 80, 300, 30)
        self.apikey_input.setText(api_key)

        # 创建选择CSV文件按钮和标签
        self.input_filepath = ''
        self.select_csv_button = QtWidgets.QPushButton("请选择csv文件", self)
        self.select_csv_button.setGeometry(50, 150, 140, 30)
        self.select_csv_button.clicked.connect(
            self.on_select_csv_button_clicked)

        self.selected_csv_label = QtWidgets.QLabel(self)
        self.selected_csv_label.setGeometry(200, 150, 250, 30)
        self.selected_csv_label.setAlignment(Qt.AlignLeft)
        # self.selected_csv_label.setStyleSheet("background-color: white;")

        interval_label = QtWidgets.QLabel("提问间隔（单位秒）", self)
        interval_label.setGeometry(50, 200, 100, 30)
        self.interval_input = QtWidgets.QLineEdit(self)
        validator = QtGui.QIntValidator()
        validator.setBottom(0)
        self.interval_input.setValidator(validator)
        self.interval_input.setGeometry(200, 200, 80, 30)
        self.interval_input.setText(interval)

        self.button = QtWidgets.QPushButton("启动", self)
        self.button.setGeometry(50, 250, 80, 30)
        self.button.clicked.connect(self.start)

    def on_select_csv_button_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "请选择csv文件", "",
            "CSV Files (*.csv)", options=options)
        if file_name:
            self.input_filepath = file_name
            self.selected_csv_label.setText(os.path.basename(file_name))

    def save_config(self):
        api_key = self.apikey_input.text()
        interval = self.interval_input.text()
        config.set_api_key(api_key)
        config.set_send_message_interval(interval or '20')
        config.save()

    @QtCore.Slot()
    def start(self):
        api_key = self.apikey_input.text()
        # csv_file_path = self.selected_csv_label.text()
        # if not csv_file_path:
        #     msg = "请选择一个csv文件"
        #     log.logger.warning(msg)
        #     self.showMessageBox(msg)
        #     return
        try:
            questions = read_csv.read_questions(self.input_filepath)
        except Exception as e:
            msg = f"在读取csv文件时发生一个错误: {e}"
            log.logger.warning(msg)
            self.showMessageBox(msg)
            return
        log.logger.warning(f'从 {self.input_filepath} 读取数据')
        # log.logger.info(f'一共读取到{len(questions)}组问题')

        self.save_config()

        from main import start
        t = Thread(target=start, args=(api_key, self.input_filepath))
        t.start()
        log.logger.info('启动')

        self.button.setEnabled(False)
        self.select_csv_button.setEnabled(False)
        self.interval_input.setEnabled(False)
        self.apikey_input.setEnabled(False)

    def showMessageBox(self, msg):
        log.logger.warning(msg)
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle(APP_NAME)
        msgBox.setText(msg)
        msgBox.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 350)
    widget.show()

    widget.setWindowTitle(APP_NAME)
    # 设置窗口置顶
    # widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    log.logger.info('程序启动')
    sys.exit(app.exec())
