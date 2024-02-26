import os
import subprocess
import sys

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


class ApplicationButtonWdg(QtWidgets.QWidget):

    BUTTON_SIZE = QtCore.QSize(48, 48)

    clicked = QtCore.Signal(str)

    def __init__(self, name, application_path, parent=None):
        super(ApplicationButtonWdg, self).__init__(parent)

        self.application_path = application_path

        self.button = self.create_button()

        self.label = QtWidgets.QLabel("<b>{0}</b>".format(name))

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.addWidget(self.button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.label)
        main_layout.addStretch()

    def create_button(self):
        button = QtWidgets.QToolButton()
        button.setFixedSize(ApplicationButtonWdg.BUTTON_SIZE)

        file_info = QtCore.QFileInfo(self.application_path)

        file_icon_provider = QtWidgets.QFileIconProvider()
        icon = file_icon_provider.icon(file_info)

        icon = self.get_scaled_icon(icon)
        button.setIcon(icon)
        button.setIconSize(ApplicationButtonWdg.BUTTON_SIZE)

        button.clicked.connect(self.on_click)

        return button

    def get_scaled_icon(self, icon):
        pixmap = icon.pixmap(ApplicationButtonWdg.BUTTON_SIZE)
        return QtGui.QIcon(pixmap)

    def on_click(self):
        self.clicked.emit(self.application_path)


class MayaLauncher(QtWidgets.QWidget):

    MAYA_2024_PATH = "/mnt/e/maya/Maya2024/bin/maya.exe"
    MAYA_2023_PATH = "/mnt/e/maya_2023/Maya2023/bin/maya.exe"

    EMPTY_SCENE = "<Empty Scene>"

    def __init__(self):
        super(MayaLauncher, self).__init__(parent=None)

        self.setWindowTitle("Maya Launcher")
        self.setMinimumWidth(360)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.env_select_cmb = QtWidgets.QComboBox()
        self.env_select_cmb.addItems(["Stable", "Dev"])

        self.maya_2023_btn = ApplicationButtonWdg("Maya 2023", MayaLauncher.MAYA_2023_PATH)
        self.maya_2024_btn = ApplicationButtonWdg("Maya 2024", MayaLauncher.MAYA_2024_PATH)

        self.scene_select_cmb = QtWidgets.QComboBox()
        self.scene_select_cmb.addItems([MayaLauncher.EMPTY_SCENE, "E:/maya_output/shapes.ma"])
        
    def create_layout(self):
        env_select_layout = QtWidgets.QHBoxLayout()
        env_select_layout.addStretch()
        env_select_layout.addWidget(QtWidgets.QLabel("Environment:"))
        env_select_layout.addWidget(self.env_select_cmb)

        maya_btn_layout = QtWidgets.QHBoxLayout()
        maya_btn_layout.addWidget(self.maya_2023_btn)
        maya_btn_layout.addWidget(self.maya_2024_btn)
        maya_btn_layout.addStretch()

        scene_select_layout = QtWidgets.QVBoxLayout()
        scene_select_layout.addWidget(QtWidgets.QLabel("Scene Selection:"))
        scene_select_layout.addWidget(self.scene_select_cmb)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(env_select_layout)
        main_layout.addLayout(maya_btn_layout)
        main_layout.addLayout(scene_select_layout)
        main_layout.addStretch()

    def create_connections(self):
        self.maya_2023_btn.clicked.connect(self.open_application)
        self.maya_2024_btn.clicked.connect(self.open_application)

    def open_application(self, application_path):
        print("Opening Application: {0}".format(application_path))
        
        selected_env = ""
        maya_args = []
        
        selected_env = self.env_select_cmb.currentText()
        if selected_env == "Dev":
            selected_env_path = "E:/Pythondev"
        elif selected_env == "Stable":
            selected_env_path = "E:/PythonStable"
            
        scene_path = self.scene_select_cmb.currentText()
        if scene_path != MayaLauncher.EMPTY_SCENE:
            maya_args = ["-file", scene_path]
        
        self.open_application_qt(application_path, selected_env_path, maya_args)
    
    def open_application_python(self, application_path, selected_env_path, maya_args):
        maya_env = os.environ.copy()
        maya_env["PYTHONPATH"] = selected_env_path

        maya_args.insert(0, application_path)
        
        subprocess.Popen(maya_args,env=maya_env)  
        
        
    def open_application_qt(self, application_path, selected_env_path, maya_args):
        processing_enviroment = QtCore.QProcessEnvironment.systemEnvironment()
        processing_enviroment.insert("PYTHONPATH",selected_env_path)
        print(processing_enviroment.toStringList())
        
        process = QtCore.QProcess(self)
        process.setProcessEnvironment(processing_enviroment)
        process.setProgram(application_path)
        process.setArguments(maya_args)
        
        process.startDetached()
        


if __name__ == "__main__":
    # Create the main Qt application
    app = QtWidgets.QApplication(sys.argv)

    window = MayaLauncher()
    window.show()

    # Enter Qt main loop (start event handling)
    app.exec_()

