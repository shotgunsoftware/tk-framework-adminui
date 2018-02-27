# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'storage_map_widget.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_StorageMapWidget(object):
    def setupUi(self, StorageMapWidget):
        StorageMapWidget.setObjectName("StorageMapWidget")
        StorageMapWidget.resize(595, 117)
        self.gridLayout = QtGui.QGridLayout(StorageMapWidget)
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.root_name = QtGui.QLabel(StorageMapWidget)
        self.root_name.setObjectName("root_name")
        self.gridLayout.addWidget(self.root_name, 0, 0, 1, 1)
        self.storage_layout = QtGui.QHBoxLayout()
        self.storage_layout.setSpacing(6)
        self.storage_layout.setObjectName("storage_layout")
        self.storage_lbl = QtGui.QLabel(StorageMapWidget)
        self.storage_lbl.setObjectName("storage_lbl")
        self.storage_layout.addWidget(self.storage_lbl)
        self.storage_select_combo = QtGui.QComboBox(StorageMapWidget)
        self.storage_select_combo.setObjectName("storage_select_combo")
        self.storage_layout.addWidget(self.storage_select_combo)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.storage_layout.addItem(spacerItem)
        self.storage_layout.setStretch(0, 1)
        self.storage_layout.setStretch(1, 10)
        self.storage_layout.setStretch(2, 100)
        self.gridLayout.addLayout(self.storage_layout, 0, 1, 1, 1)
        self.root_description_layout = QtGui.QHBoxLayout()
        self.root_description_layout.setSpacing(0)
        self.root_description_layout.setObjectName("root_description_layout")
        spacerItem1 = QtGui.QSpacerItem(12, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.root_description_layout.addItem(spacerItem1)
        self.root_description = QtGui.QLabel(StorageMapWidget)
        self.root_description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.root_description.setWordWrap(True)
        self.root_description.setObjectName("root_description")
        self.root_description_layout.addWidget(self.root_description)
        self.root_description_layout.setStretch(0, 1)
        self.root_description_layout.setStretch(1, 10)
        self.gridLayout.addLayout(self.root_description_layout, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(48, 68, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 10)

        self.retranslateUi(StorageMapWidget)
        QtCore.QMetaObject.connectSlotsByName(StorageMapWidget)

    def retranslateUi(self, StorageMapWidget):
        StorageMapWidget.setWindowTitle(QtGui.QApplication.translate("StorageMapWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.root_name.setText(QtGui.QApplication.translate("StorageMapWidget", "<b>root_name</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.storage_lbl.setText(QtGui.QApplication.translate("StorageMapWidget", "<b>Local Storage:</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.root_description.setText(QtGui.QApplication.translate("StorageMapWidget", "This is a description of the root as defined in the roots.yml file. This can be short or long.", None, QtGui.QApplication.UnicodeUTF8))

