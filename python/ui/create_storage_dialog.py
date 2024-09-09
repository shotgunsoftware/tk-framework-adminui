# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_storage_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from tank.platform.qt import QtCore
for name, cls in QtCore.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls

from tank.platform.qt import QtGui
for name, cls in QtGui.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls


from  . import resources_rc

class Ui_CreateStorageDialog(object):
    def setupUi(self, CreateStorageDialog):
        if not CreateStorageDialog.objectName():
            CreateStorageDialog.setObjectName(u"CreateStorageDialog")
        CreateStorageDialog.resize(285, 94)
        CreateStorageDialog.setAutoFillBackground(True)
        self.verticalLayout_2 = QVBoxLayout(CreateStorageDialog)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setContentsMargins(12, 12, 12, 12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_widget = QWidget(CreateStorageDialog)
        self.main_widget.setObjectName(u"main_widget")
        self.verticalLayout = QVBoxLayout(self.main_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.storage_name_layout = QHBoxLayout()
        self.storage_name_layout.setSpacing(4)
        self.storage_name_layout.setObjectName(u"storage_name_layout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.storage_name_layout.addItem(self.horizontalSpacer)

        self.storage_name_lbl = QLabel(self.main_widget)
        self.storage_name_lbl.setObjectName(u"storage_name_lbl")
        self.storage_name_lbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.storage_name_layout.addWidget(self.storage_name_lbl)

        self.storage_name = QLineEdit(self.main_widget)
        self.storage_name.setObjectName(u"storage_name")

        self.storage_name_layout.addWidget(self.storage_name)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.storage_name_layout.addItem(self.horizontalSpacer_2)

        self.storage_name_layout.setStretch(0, 5)
        self.storage_name_layout.setStretch(2, 15)

        self.verticalLayout.addLayout(self.storage_name_layout)

        self.info = QLabel(self.main_widget)
        self.info.setObjectName(u"info")
        font = QFont()
        font.setPointSize(10)
        self.info.setFont(font)
        self.info.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.info.setWordWrap(True)

        self.verticalLayout.addWidget(self.info)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)

        self.verticalLayout_2.addWidget(self.main_widget)

        self.button_box = QDialogButtonBox(CreateStorageDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setLayoutDirection(Qt.LeftToRight)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.button_box)

        QWidget.setTabOrder(self.storage_name, self.button_box)

        self.retranslateUi(CreateStorageDialog)
        self.button_box.accepted.connect(CreateStorageDialog.accept)
        self.button_box.rejected.connect(CreateStorageDialog.reject)

        QMetaObject.connectSlotsByName(CreateStorageDialog)
    # setupUi

    def retranslateUi(self, CreateStorageDialog):
        CreateStorageDialog.setWindowTitle(QCoreApplication.translate("CreateStorageDialog", u"New Storage", None))
        self.storage_name_lbl.setText(QCoreApplication.translate("CreateStorageDialog", u"Storage Name:", None))
        self.info.setText("")
    # retranslateUi
