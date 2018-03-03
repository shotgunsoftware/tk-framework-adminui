# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_storage_dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_CreateStorageDialog(object):
    def setupUi(self, CreateStorageDialog):
        CreateStorageDialog.setObjectName("CreateStorageDialog")
        CreateStorageDialog.resize(311, 126)
        CreateStorageDialog.setAutoFillBackground(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CreateStorageDialog)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setContentsMargins(12, 12, 12, 12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_widget = QtGui.QWidget(CreateStorageDialog)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.main_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.create_storage_title_lbl = QtGui.QLabel(self.main_widget)
        self.create_storage_title_lbl.setObjectName("create_storage_title_lbl")
        self.verticalLayout.addWidget(self.create_storage_title_lbl)
        spacerItem = QtGui.QSpacerItem(20, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.storage_name_layout = QtGui.QHBoxLayout()
        self.storage_name_layout.setSpacing(4)
        self.storage_name_layout.setObjectName("storage_name_layout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.storage_name_layout.addItem(spacerItem1)
        self.storage_name_lbl = QtGui.QLabel(self.main_widget)
        self.storage_name_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.storage_name_lbl.setObjectName("storage_name_lbl")
        self.storage_name_layout.addWidget(self.storage_name_lbl)
        self.storage_name = QtGui.QLineEdit(self.main_widget)
        self.storage_name.setObjectName("storage_name")
        self.storage_name_layout.addWidget(self.storage_name)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.storage_name_layout.addItem(spacerItem2)
        self.storage_name_layout.setStretch(0, 5)
        self.storage_name_layout.setStretch(2, 15)
        self.verticalLayout.addLayout(self.storage_name_layout)
        spacerItem3 = QtGui.QSpacerItem(20, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.info = QtGui.QLabel(self.main_widget)
        self.info.setText("")
        self.info.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.info.setWordWrap(True)
        self.info.setObjectName("info")
        self.verticalLayout.addWidget(self.info)
        self.verticalLayout_2.addWidget(self.main_widget)
        self.button_box = QtGui.QDialogButtonBox(CreateStorageDialog)
        self.button_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout_2.addWidget(self.button_box)

        self.retranslateUi(CreateStorageDialog)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("accepted()"), CreateStorageDialog.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("rejected()"), CreateStorageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateStorageDialog)
        CreateStorageDialog.setTabOrder(self.storage_name, self.button_box)

    def retranslateUi(self, CreateStorageDialog):
        CreateStorageDialog.setWindowTitle(QtGui.QApplication.translate("CreateStorageDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.create_storage_title_lbl.setText(QtGui.QApplication.translate("CreateStorageDialog", "<html><head/><body><p><span style=\" font-size:16pt;\">Create Local Storage</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.storage_name_lbl.setText(QtGui.QApplication.translate("CreateStorageDialog", "Storage Name:", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
