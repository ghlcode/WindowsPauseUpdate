import os
from main_windows import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox
import winreg
import datetime


class MainWindowView(QtWidgets.QMainWindow, Ui_MainWindow):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())

        font = QFont('Arial', 14)
        self.lineEdit.setFont(font)

        self.pushButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        key_path = r"SOFTWARE\Microsoft\WindowsUpdate\UX\Settings"
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)  # 设置对话框图标

        try:
            # 以管理员权限打开注册表项
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                pause_days = int(self.lineEdit.text())

                # 设置允许最大暂停天数
                winreg.SetValueEx(key, "FlightSettingsMaxPauseDays", 0, winreg.REG_DWORD, pause_days)

                # 计算暂停更新的时间
                current_time = datetime.datetime.utcnow()
                end_time = (current_time + datetime.timedelta(days=pause_days)).strftime("%Y-%m-%dT%H:%M:%SZ")

                start_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                winreg.SetValueEx(key, 'PauseFeatureUpdatesStartTime', 0, winreg.REG_SZ, start_time)
                winreg.SetValueEx(key, 'PauseQualityUpdatesStartTime', 0, winreg.REG_SZ, end_time)
                winreg.SetValueEx(key, 'PauseUpdatesStartTime', 0, winreg.REG_SZ, start_time)

                # 设置 Windows Update 暂停时间
                winreg.SetValueEx(key, "PauseFeatureUpdatesEndTime", 0, winreg.REG_SZ, end_time)
                winreg.SetValueEx(key, "PauseQualityUpdatesEndTime", 0, winreg.REG_SZ, end_time)
                winreg.SetValueEx(key, "PauseUpdatesExpiryTime", 0, winreg.REG_SZ, end_time)

                msg.setText(f"Windows 更新已暂停 {pause_days} 天！")  # 设置对话框文本
                msg.setWindowTitle("暂停成功")  # 设置对话框标题

        except PermissionError:
            msg.setText("修改失败，请以 **管理员** 身份运行脚本！")  # 设置对话框文本
            msg.setWindowTitle("权限错误")  # 设置对话框标题

        except Exception as e:
            msg.setText(f"修改失败，错误信息：\n{e}")  # 设置对话框文本
            msg.setWindowTitle("暂停失败")  # 设置对话框标题
        msg.setStandardButtons(QMessageBox.Ok)
        # 显示对话框并处理用户点击的按钮
        result = msg.exec_()
        if result == QMessageBox.Ok:
            pass



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window  = MainWindowView()
    window .show()
    app.exec_()