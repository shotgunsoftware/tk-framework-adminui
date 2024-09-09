# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'storage_map_widget.ui'
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

class Ui_StorageMapWidget(object):
    def setupUi(self, StorageMapWidget):
        if not StorageMapWidget.objectName():
            StorageMapWidget.setObjectName(u"StorageMapWidget")
        StorageMapWidget.resize(456, 182)
        StorageMapWidget.setAutoFillBackground(True)
        self.gridLayout_2 = QGridLayout(StorageMapWidget)
        self.gridLayout_2.setContentsMargins(8, 8, 8, 8)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(12)
        self.gridLayout_2.setVerticalSpacing(6)
        self.root_desc_layout = QHBoxLayout()
        self.root_desc_layout.setSpacing(0)
        self.root_desc_layout.setObjectName(u"root_desc_layout")
        self.horizontalSpacer = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.root_desc_layout.addItem(self.horizontalSpacer)

        self.stroage_root_desc_area = QScrollArea(StorageMapWidget)
        self.stroage_root_desc_area.setObjectName(u"stroage_root_desc_area")
        self.stroage_root_desc_area.setFocusPolicy(Qt.NoFocus)
        self.stroage_root_desc_area.setFrameShape(QFrame.NoFrame)
        self.stroage_root_desc_area.setFrameShadow(QFrame.Plain)
        self.stroage_root_desc_area.setWidgetResizable(True)
        self.storage_root_desc = QWidget()
        self.storage_root_desc.setObjectName(u"storage_root_desc")
        self.storage_root_desc.setGeometry(QRect(0, 0, 157, 104))
        self.verticalLayout = QVBoxLayout(self.storage_root_desc)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.root_description = QLabel(self.storage_root_desc)
        self.root_description.setObjectName(u"root_description")
        self.root_description.setStyleSheet(u"font-size: 10px;\n"
"color: rgb(160, 160, 160);")
        self.root_description.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.root_description.setWordWrap(True)

        self.verticalLayout.addWidget(self.root_description)

        self.stroage_root_desc_area.setWidget(self.storage_root_desc)

        self.root_desc_layout.addWidget(self.stroage_root_desc_area)

        self.root_desc_layout.setStretch(0, 1)

        self.gridLayout_2.addLayout(self.root_desc_layout, 1, 0, 1, 1)

        self.storage_layout = QHBoxLayout()
        self.storage_layout.setSpacing(6)
        self.storage_layout.setObjectName(u"storage_layout")
        self.storage_lbl = QLabel(StorageMapWidget)
        self.storage_lbl.setObjectName(u"storage_lbl")

        self.storage_layout.addWidget(self.storage_lbl)

        self.storage_select_combo = QComboBox(StorageMapWidget)
        self.storage_select_combo.setObjectName(u"storage_select_combo")
        self.storage_select_combo.setFocusPolicy(Qt.NoFocus)
        self.storage_select_combo.setAutoFillBackground(True)
        self.storage_select_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.storage_layout.addWidget(self.storage_select_combo)

        self.save_storage_btn = QToolButton(StorageMapWidget)
        self.save_storage_btn.setObjectName(u"save_storage_btn")
        font = QFont()
        font.setPointSize(10)
        self.save_storage_btn.setFont(font)
        self.save_storage_btn.setFocusPolicy(Qt.NoFocus)
        self.save_storage_btn.setToolButtonStyle(Qt.ToolButtonTextOnly)

        self.storage_layout.addWidget(self.save_storage_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.storage_layout.addItem(self.horizontalSpacer_2)

        self.storage_layout.setStretch(0, 1)
        self.storage_layout.setStretch(1, 1)
        self.storage_layout.setStretch(2, 1)
        self.storage_layout.setStretch(3, 100)

        self.gridLayout_2.addLayout(self.storage_layout, 0, 1, 1, 1)

        self.paths_layout = QHBoxLayout()
        self.paths_layout.setSpacing(0)
        self.paths_layout.setObjectName(u"paths_layout")
        self.path_frame = QFrame(StorageMapWidget)
        self.path_frame.setObjectName(u"path_frame")
        self.gridLayout_3 = QGridLayout(self.path_frame)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.windows_path_lbl = QLabel(self.path_frame)
        self.windows_path_lbl.setObjectName(u"windows_path_lbl")
        self.windows_path_lbl.setStyleSheet(u"font-size: 10px;\n"
"color: rgb(120, 120, 120);")
        self.windows_path_lbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.windows_path_lbl, 2, 0, 1, 1)

        self.windows_path_layout = QHBoxLayout()
        self.windows_path_layout.setSpacing(4)
        self.windows_path_layout.setObjectName(u"windows_path_layout")
        self.windows_path = QLineEdit(self.path_frame)
        self.windows_path.setObjectName(u"windows_path")
        self.windows_path.setEnabled(False)
        self.windows_path.setFocusPolicy(Qt.NoFocus)

        self.windows_path_layout.addWidget(self.windows_path)

        self.windows_path_edit = QLineEdit(self.path_frame)
        self.windows_path_edit.setObjectName(u"windows_path_edit")
        self.windows_path_edit.setFocusPolicy(Qt.ClickFocus)

        self.windows_path_layout.addWidget(self.windows_path_edit)

        self.windows_path_layout.setStretch(0, 1)
        self.windows_path_layout.setStretch(1, 1)

        self.gridLayout_3.addLayout(self.windows_path_layout, 2, 1, 1, 1)

        self.linux_path_layout = QHBoxLayout()
        self.linux_path_layout.setSpacing(4)
        self.linux_path_layout.setObjectName(u"linux_path_layout")
        self.linux_path = QLineEdit(self.path_frame)
        self.linux_path.setObjectName(u"linux_path")
        self.linux_path.setEnabled(False)
        self.linux_path.setFocusPolicy(Qt.NoFocus)

        self.linux_path_layout.addWidget(self.linux_path)

        self.linux_path_edit = QLineEdit(self.path_frame)
        self.linux_path_edit.setObjectName(u"linux_path_edit")
        self.linux_path_edit.setFocusPolicy(Qt.ClickFocus)

        self.linux_path_layout.addWidget(self.linux_path_edit)

        self.linux_path_layout.setStretch(0, 1)
        self.linux_path_layout.setStretch(1, 1)

        self.gridLayout_3.addLayout(self.linux_path_layout, 0, 1, 1, 1)

        self.linux_path_lbl = QLabel(self.path_frame)
        self.linux_path_lbl.setObjectName(u"linux_path_lbl")
        self.linux_path_lbl.setStyleSheet(u"font-size: 10px;\n"
"color: rgb(120, 120, 120);")
        self.linux_path_lbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.linux_path_lbl, 0, 0, 1, 1)

        self.mac_path_lbl = QLabel(self.path_frame)
        self.mac_path_lbl.setObjectName(u"mac_path_lbl")
        self.mac_path_lbl.setStyleSheet(u"font-size: 10px;\n"
"color: rgb(120, 120, 120);")
        self.mac_path_lbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.mac_path_lbl, 1, 0, 1, 1)

        self.mac_path_layout = QHBoxLayout()
        self.mac_path_layout.setSpacing(4)
        self.mac_path_layout.setObjectName(u"mac_path_layout")
        self.mac_path = QLineEdit(self.path_frame)
        self.mac_path.setObjectName(u"mac_path")
        self.mac_path.setEnabled(False)
        self.mac_path.setFocusPolicy(Qt.NoFocus)

        self.mac_path_layout.addWidget(self.mac_path)

        self.mac_path_edit = QLineEdit(self.path_frame)
        self.mac_path_edit.setObjectName(u"mac_path_edit")
        self.mac_path_edit.setFocusPolicy(Qt.ClickFocus)

        self.mac_path_layout.addWidget(self.mac_path_edit)

        self.mac_path_layout.setStretch(0, 1)
        self.mac_path_layout.setStretch(1, 1)

        self.gridLayout_3.addLayout(self.mac_path_layout, 1, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.linux_path_browse = QToolButton(self.path_frame)
        self.linux_path_browse.setObjectName(u"linux_path_browse")
        self.linux_path_browse.setFocusPolicy(Qt.NoFocus)
        icon = QIcon()
        icon.addFile(u":/tk-framework-adminui/setup_project/file_browse.png", QSize(), QIcon.Normal, QIcon.Off)
        self.linux_path_browse.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.linux_path_browse)

        self.linux_lock = QLabel(self.path_frame)
        self.linux_lock.setObjectName(u"linux_lock")
        self.linux_lock.setMinimumSize(QSize(8, 11))
        self.linux_lock.setMaximumSize(QSize(8, 11))
        self.linux_lock.setPixmap(QPixmap(u":/tk-framework-adminui/setup_project/icon_lock.png"))
        self.linux_lock.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.linux_lock)

        self.horizontalSpacer_8 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)

        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 2, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_6 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.mac_path_browse = QToolButton(self.path_frame)
        self.mac_path_browse.setObjectName(u"mac_path_browse")
        self.mac_path_browse.setFocusPolicy(Qt.NoFocus)
        self.mac_path_browse.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.mac_path_browse)

        self.mac_lock = QLabel(self.path_frame)
        self.mac_lock.setObjectName(u"mac_lock")
        self.mac_lock.setMinimumSize(QSize(8, 11))
        self.mac_lock.setMaximumSize(QSize(8, 11))
        self.mac_lock.setPixmap(QPixmap(u":/tk-framework-adminui/setup_project/icon_lock.png"))
        self.mac_lock.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.mac_lock)

        self.horizontalSpacer_9 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.gridLayout_3.addLayout(self.horizontalLayout_4, 1, 2, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_7 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.windows_path_browse = QToolButton(self.path_frame)
        self.windows_path_browse.setObjectName(u"windows_path_browse")
        self.windows_path_browse.setFocusPolicy(Qt.NoFocus)
        self.windows_path_browse.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.windows_path_browse)

        self.windows_lock = QLabel(self.path_frame)
        self.windows_lock.setObjectName(u"windows_lock")
        self.windows_lock.setMinimumSize(QSize(8, 11))
        self.windows_lock.setMaximumSize(QSize(8, 11))
        self.windows_lock.setPixmap(QPixmap(u":/tk-framework-adminui/setup_project/icon_lock.png"))
        self.windows_lock.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.windows_lock)

        self.horizontalSpacer_10 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)

        self.gridLayout_3.addLayout(self.horizontalLayout_5, 2, 2, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 100)
        self.gridLayout_3.setColumnStretch(2, 1)

        self.paths_layout.addWidget(self.path_frame)

        self.gridLayout_2.addLayout(self.paths_layout, 1, 1, 1, 1)

        self.root_name_layout = QHBoxLayout()
        self.root_name_layout.setSpacing(4)
        self.root_name_layout.setObjectName(u"root_name_layout")
        self.root_name = QLabel(StorageMapWidget)
        self.root_name.setObjectName(u"root_name")

        self.root_name_layout.addWidget(self.root_name)

        self.horizontalSpacer_4 = QSpacerItem(40, 4, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.root_name_layout.addItem(self.horizontalSpacer_4)

        self.root_name_layout.setStretch(0, 1)
        self.root_name_layout.setStretch(1, 10)

        self.gridLayout_2.addLayout(self.root_name_layout, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.count_lbl = QLabel(StorageMapWidget)
        self.count_lbl.setObjectName(u"count_lbl")
        self.count_lbl.setStyleSheet(u"font-size: 10px;\n"
"color: rgb(120, 120, 120);")

        self.horizontalLayout_2.addWidget(self.count_lbl)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.storage_info = QLabel(StorageMapWidget)
        self.storage_info.setObjectName(u"storage_info")
        self.storage_info.setStyleSheet(u"font-size: 10px;\n"
"color: rgb(252, 98, 70);")
        self.storage_info.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.storage_info.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.storage_info)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 10)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)

        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setColumnStretch(0, 2)
        self.gridLayout_2.setColumnStretch(1, 3)

        self.retranslateUi(StorageMapWidget)

        QMetaObject.connectSlotsByName(StorageMapWidget)
    # setupUi

    def retranslateUi(self, StorageMapWidget):
        StorageMapWidget.setWindowTitle(QCoreApplication.translate("StorageMapWidget", u"Form", None))
        self.root_description.setText(QCoreApplication.translate("StorageMapWidget", u"This is a description of the root as defined in the roots.yml file. This can be short or long.", None))
#if QT_CONFIG(tooltip)
        self.storage_lbl.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>These are the storage paths defined by your Flow Production Tracking site.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.storage_lbl.setText(QCoreApplication.translate("StorageMapWidget", u"Storage:", None))
#if QT_CONFIG(tooltip)
        self.storage_select_combo.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>These are the storage paths defined by your Flow Production Tracking site.</p>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.save_storage_btn.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>Click this to save your changes to the selected Storage paths.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.save_storage_btn.setText(QCoreApplication.translate("StorageMapWidget", u"Save", None))
        self.windows_path_lbl.setText(QCoreApplication.translate("StorageMapWidget", u"Windows:", None))
#if QT_CONFIG(tooltip)
        self.windows_path_edit.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>Edit the storage path for this operating system.</p>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.linux_path_edit.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>Edit the storage path for this operating system.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.linux_path_lbl.setText(QCoreApplication.translate("StorageMapWidget", u"Linux:", None))
        self.mac_path_lbl.setText(QCoreApplication.translate("StorageMapWidget", u"Mac:", None))
#if QT_CONFIG(tooltip)
        self.mac_path_edit.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>Edit the storage path for this operating system.</p>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.linux_path_browse.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>Browse a path on the current operating system.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.linux_path_browse.setText(QCoreApplication.translate("StorageMapWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.linux_lock.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>This path is locked since it has been saved to Flow Production Tracking. Visit Site Preferences > File Management to modify this path. WARNING: changing this path could break existing projects.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.linux_lock.setText("")
#if QT_CONFIG(tooltip)
        self.mac_path_browse.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>Browse a path on the current operating system.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.mac_path_browse.setText(QCoreApplication.translate("StorageMapWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.mac_lock.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>This path is locked since it has been saved to Flow Production Tracking. Visit Site Preferences > File Management to modify this path. WARNING: changing this path could break existing projects.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.mac_lock.setText("")
#if QT_CONFIG(tooltip)
        self.windows_path_browse.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>Browse a path on the current operating system.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.windows_path_browse.setText(QCoreApplication.translate("StorageMapWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.windows_lock.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>This path is locked since it has been saved to Flow Production Tracking. Visit Site Preferences > File Management to modify this path. WARNING: changing this path could break existing projects.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.windows_lock.setText("")
#if QT_CONFIG(tooltip)
        self.root_name.setToolTip(QCoreApplication.translate("StorageMapWidget", u"<p>This is the storage root name as required by the selected configuration.</p>", None))
#endif // QT_CONFIG(tooltip)
        self.root_name.setText(QCoreApplication.translate("StorageMapWidget", u"root_name", None))
        self.count_lbl.setText("")
        self.storage_info.setText("")
    # retranslateUi
