# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setup_project.ui'
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


from ..setup_project.setup_type_page import SetupTypePage
from ..setup_project.project_config_page import ProjectConfigPage
from ..setup_project.github_config_page import GithubConfigPage
from ..setup_project.disk_config_page import DiskConfigPage
from ..setup_project.project_name_page import ProjectNamePage
from ..setup_project.config_location_page import ConfigLocationPage
from ..setup_project.progress_page import ProgressPage
from ..setup_project.storage_map_page import StorageMapPage
from ..setup_project.storage_map_page import StorageMapContainerWidget

from  . import resources_rc
from  . import resources_rc

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.resize(839, 540)
        icon1 = QIcon()
        icon1.addFile(u":/res/shotgun_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        Wizard.setWindowIcon(icon1)
        Wizard.setModal(True)
        Wizard.setWizardStyle(QWizard.ModernStyle)
        Wizard.setOptions(QWizard.CancelButtonOnLeft|QWizard.HaveHelpButton|QWizard.NoBackButtonOnLastPage)
        Wizard.setTitleFormat(Qt.RichText)
        Wizard.setSubTitleFormat(Qt.RichText)
        self.setup_type_page = SetupTypePage()
        self.setup_type_page.setObjectName(u"setup_type_page")
        self.verticalLayout = QVBoxLayout(self.setup_type_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(25, 20, 25, 20)
        self.setup_type_subheader = QLabel(self.setup_type_page)
        self.setup_type_subheader.setObjectName(u"setup_type_subheader")
        self.setup_type_subheader.setStyleSheet(u"font-size: 14px;")
        self.setup_type_subheader.setWordWrap(True)

        self.verticalLayout.addWidget(self.setup_type_subheader)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.select_standard = QRadioButton(self.setup_type_page)
        self.select_standard.setObjectName(u"select_standard")
        self.select_standard.setFocusPolicy(Qt.NoFocus)
        self.select_standard.setStyleSheet(u"QRadioButton {\n"
"    font-size: 16px;\n"
"}\n"
"")
        self.select_standard.setChecked(True)

        self.verticalLayout.addWidget(self.select_standard)

        self.label_standard = QLabel(self.setup_type_page)
        self.label_standard.setObjectName(u"label_standard")
        self.label_standard.setStyleSheet(u"font-size: 12px;\n"
"color: rgb(160, 160, 160);")
        self.label_standard.setIndent(20)

        self.verticalLayout.addWidget(self.label_standard)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.select_project = QRadioButton(self.setup_type_page)
        self.select_project.setObjectName(u"select_project")
        self.select_project.setFocusPolicy(Qt.NoFocus)
        self.select_project.setStyleSheet(u"QRadioButton {\n"
"    font-size: 16px;\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.select_project)

        self.label_project = QLabel(self.setup_type_page)
        self.label_project.setObjectName(u"label_project")
        self.label_project.setStyleSheet(u"font-size: 12px;\n"
"color: rgb(160, 160, 160);")
        self.label_project.setIndent(20)

        self.verticalLayout.addWidget(self.label_project)

        self.verticalSpacer_6 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.select_github = QRadioButton(self.setup_type_page)
        self.select_github.setObjectName(u"select_github")
        self.select_github.setFocusPolicy(Qt.NoFocus)
        self.select_github.setStyleSheet(u"QRadioButton {\n"
"    font-size: 16px;\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.select_github)

        self.label_github = QLabel(self.setup_type_page)
        self.label_github.setObjectName(u"label_github")
        self.label_github.setStyleSheet(u"font-size: 12px;\n"
"color: rgb(160, 160, 160);")
        self.label_github.setIndent(20)

        self.verticalLayout.addWidget(self.label_github)

        self.verticalSpacer_7 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_7)

        self.select_disk = QRadioButton(self.setup_type_page)
        self.select_disk.setObjectName(u"select_disk")
        self.select_disk.setFocusPolicy(Qt.NoFocus)
        self.select_disk.setStyleSheet(u"QRadioButton {\n"
"    font-size: 16px;\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.select_disk)

        self.label_disk = QLabel(self.setup_type_page)
        self.label_disk.setObjectName(u"label_disk")
        self.label_disk.setStyleSheet(u"font-size: 12px;\n"
"color: rgb(160, 160, 160);")
        self.label_disk.setIndent(20)

        self.verticalLayout.addWidget(self.label_disk)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.verticalLayout.setStretch(13, 1)
        Wizard.addPage(self.setup_type_page)
        self.project_config_page = ProjectConfigPage()
        self.project_config_page.setObjectName(u"project_config_page")
        self.verticalLayout_2 = QVBoxLayout(self.project_config_page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(25, 20, 25, 20)
        self.project_config_subheader = QLabel(self.project_config_page)
        self.project_config_subheader.setObjectName(u"project_config_subheader")
        self.project_config_subheader.setStyleSheet(u"font-size: 14px;")
        self.project_config_subheader.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.project_config_subheader)

        self.verticalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_8)

        self.project_list = QListView(self.project_config_page)
        self.project_list.setObjectName(u"project_list")
        self.project_list.setFrameShape(QFrame.NoFrame)
        self.project_list.setFrameShadow(QFrame.Plain)
        self.project_list.setAutoScroll(False)
        self.project_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.project_list.setProperty("showDropIndicator", False)
        self.project_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.project_list.setTextElideMode(Qt.ElideNone)
        self.project_list.setMovement(QListView.Static)
        self.project_list.setFlow(QListView.LeftToRight)
        self.project_list.setProperty("isWrapping", True)
        self.project_list.setResizeMode(QListView.Adjust)
        self.project_list.setLayoutMode(QListView.Batched)
        self.project_list.setSpacing(10)
        self.project_list.setViewMode(QListView.IconMode)
        self.project_list.setUniformItemSizes(True)
        self.project_list.setWordWrap(True)
        self.project_list.setSelectionRectVisible(False)

        self.verticalLayout_2.addWidget(self.project_list)

        self.project_errors = QLabel(self.project_config_page)
        self.project_errors.setObjectName(u"project_errors")
        self.project_errors.setStyleSheet(u"color: rgb(252, 98, 70);")
        self.project_errors.setAlignment(Qt.AlignCenter)
        self.project_errors.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.project_errors)

        Wizard.addPage(self.project_config_page)
        self.github_config_page = GithubConfigPage()
        self.github_config_page.setObjectName(u"github_config_page")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.github_config_page.sizePolicy().hasHeightForWidth())
        self.github_config_page.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.github_config_page)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(25, 20, 25, 20)
        self.github_config_subheader = QLabel(self.github_config_page)
        self.github_config_subheader.setObjectName(u"github_config_subheader")
        self.github_config_subheader.setStyleSheet(u"font-size: 14px;")
        self.github_config_subheader.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.github_config_subheader)

        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_14)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_20)

        self.github_url = QLineEdit(self.github_config_page)
        self.github_url.setObjectName(u"github_url")

        self.verticalLayout_4.addWidget(self.github_url)

        self.label = QLabel(self.github_config_page)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_9)

        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.github_errors = QLabel(self.github_config_page)
        self.github_errors.setObjectName(u"github_errors")
        self.github_errors.setStyleSheet(u"color: rgb(252, 98, 70);")
        self.github_errors.setAlignment(Qt.AlignCenter)
        self.github_errors.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.github_errors)

        Wizard.addPage(self.github_config_page)
        self.disk_config_page = DiskConfigPage()
        self.disk_config_page.setObjectName(u"disk_config_page")
        self.verticalLayout_8 = QVBoxLayout(self.disk_config_page)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(25, 20, 25, 20)
        self.disk_config_subheader = QLabel(self.disk_config_page)
        self.disk_config_subheader.setObjectName(u"disk_config_subheader")
        self.disk_config_subheader.setStyleSheet(u"font-size: 14px;")
        self.disk_config_subheader.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.disk_config_subheader)

        self.verticalSpacer_17 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_17)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.folder_icon = QLabel(self.disk_config_page)
        self.folder_icon.setObjectName(u"folder_icon")
        self.folder_icon.setMaximumSize(QSize(200, 200))
        self.folder_icon.setPixmap(QPixmap(u":/tk-framework-adminui/setup_project/shotgun_folder.png"))
        self.folder_icon.setScaledContents(True)
        self.folder_icon.setOpenExternalLinks(True)

        self.horizontalLayout_2.addWidget(self.folder_icon)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(10)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_21)

        self.path = QLineEdit(self.disk_config_page)
        self.path.setObjectName(u"path")

        self.verticalLayout_7.addWidget(self.path)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.disk_browse_button_zip = QPushButton(self.disk_config_page)
        self.disk_browse_button_zip.setObjectName(u"disk_browse_button_zip")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.disk_browse_button_zip.sizePolicy().hasHeightForWidth())
        self.disk_browse_button_zip.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.disk_browse_button_zip)

        self.disk_browse_button_dir = QPushButton(self.disk_config_page)
        self.disk_browse_button_dir.setObjectName(u"disk_browse_button_dir")
        sizePolicy1.setHeightForWidth(self.disk_browse_button_dir.sizePolicy().hasHeightForWidth())
        self.disk_browse_button_dir.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.disk_browse_button_dir)

        self.verticalLayout_7.addLayout(self.horizontalLayout_4)

        self.label_2 = QLabel(self.disk_config_page)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_7.addWidget(self.label_2)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_10)

        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.disk_errors = QLabel(self.disk_config_page)
        self.disk_errors.setObjectName(u"disk_errors")
        self.disk_errors.setStyleSheet(u"color: rgb(252, 98, 70);")
        self.disk_errors.setAlignment(Qt.AlignCenter)
        self.disk_errors.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.disk_errors)

        Wizard.addPage(self.disk_config_page)
        self.storage_map_page = StorageMapPage()
        self.storage_map_page.setObjectName(u"storage_map_page")
        self.verticalLayout_10 = QVBoxLayout(self.storage_map_page)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(25, 20, 25, 20)
        self.storage_def_lbl = QLabel(self.storage_map_page)
        self.storage_def_lbl.setObjectName(u"storage_def_lbl")
        self.storage_def_lbl.setWordWrap(True)
        self.storage_def_lbl.setOpenExternalLinks(True)

        self.verticalLayout_10.addWidget(self.storage_def_lbl)

        self.verticalSpacer_13 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_13)

        self.storage_map_area = QScrollArea(self.storage_map_page)
        self.storage_map_area.setObjectName(u"storage_map_area")
        self.storage_map_area.setFocusPolicy(Qt.NoFocus)
        self.storage_map_area.setAutoFillBackground(True)
        self.storage_map_area.setWidgetResizable(True)
        self.storage_map_area_widget = StorageMapContainerWidget()
        self.storage_map_area_widget.setObjectName(u"storage_map_area_widget")
        self.storage_map_area_widget.setGeometry(QRect(0, 0, 763, 232))
        self.storage_map_area.setWidget(self.storage_map_area_widget)

        self.verticalLayout_10.addWidget(self.storage_map_area)

        self.verticalSpacer_16 = QSpacerItem(20, 6, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_16)

        self.local_file_link_lbl = QLabel(self.storage_map_page)
        self.local_file_link_lbl.setObjectName(u"local_file_link_lbl")
        self.local_file_link_lbl.setStyleSheet(u"font-size: 10px;\n"
"color: rgb(160, 160, 160);")
        self.local_file_link_lbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.local_file_link_lbl.setWordWrap(True)
        self.local_file_link_lbl.setOpenExternalLinks(True)

        self.verticalLayout_10.addWidget(self.local_file_link_lbl)

        self.verticalSpacer_15 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_15)

        self.storage_errors = QLabel(self.storage_map_page)
        self.storage_errors.setObjectName(u"storage_errors")
        self.storage_errors.setStyleSheet(u"color: rgb(252, 98, 70);")
        self.storage_errors.setWordWrap(True)

        self.verticalLayout_10.addWidget(self.storage_errors)

        Wizard.addPage(self.storage_map_page)
        self.project_name_page = ProjectNamePage()
        self.project_name_page.setObjectName(u"project_name_page")
        self.verticalLayout_9 = QVBoxLayout(self.project_name_page)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.project_name_scroll_area = QScrollArea(self.project_name_page)
        self.project_name_scroll_area.setObjectName(u"project_name_scroll_area")
        self.project_name_scroll_area.setFocusPolicy(Qt.NoFocus)
        self.project_name_scroll_area.setFrameShape(QFrame.NoFrame)
        self.project_name_scroll_area.setFrameShadow(QFrame.Plain)
        self.project_name_scroll_area.setWidgetResizable(True)
        self.project_name_scroll_area_contents = QWidget()
        self.project_name_scroll_area_contents.setObjectName(u"project_name_scroll_area_contents")
        self.project_name_scroll_area_contents.setGeometry(QRect(0, 0, 302, 189))
        self.project_contents_layout = QVBoxLayout(self.project_name_scroll_area_contents)
        self.project_contents_layout.setObjectName(u"project_contents_layout")
        self.project_contents_layout.setContentsMargins(25, 20, 25, 20)
        self.project_name_subheader = QLabel(self.project_name_scroll_area_contents)
        self.project_name_subheader.setObjectName(u"project_name_subheader")
        self.project_name_subheader.setStyleSheet(u"font-size: 14px;")
        self.project_name_subheader.setWordWrap(True)

        self.project_contents_layout.addWidget(self.project_name_subheader)

        self.verticalSpacer_18 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.project_contents_layout.addItem(self.verticalSpacer_18)

        self.project_name = QLineEdit(self.project_name_scroll_area_contents)
        self.project_name.setObjectName(u"project_name")

        self.project_contents_layout.addWidget(self.project_name)

        self.verticalSpacer_23 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.project_contents_layout.addItem(self.verticalSpacer_23)

        self.project_directories = QLabel(self.project_name_scroll_area_contents)
        self.project_directories.setObjectName(u"project_directories")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.project_directories.sizePolicy().hasHeightForWidth())
        self.project_directories.setSizePolicy(sizePolicy2)
        self.project_directories.setFrameShape(QFrame.NoFrame)
        self.project_directories.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.project_contents_layout.addWidget(self.project_directories)

        self.project_name_scroll_area.setWidget(self.project_name_scroll_area_contents)

        self.verticalLayout_9.addWidget(self.project_name_scroll_area)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_11)

        self.project_name_errors = QLabel(self.project_name_page)
        self.project_name_errors.setObjectName(u"project_name_errors")
        self.project_name_errors.setStyleSheet(u"color: rgb(252, 98, 70);")
        self.project_name_errors.setAlignment(Qt.AlignCenter)
        self.project_name_errors.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.project_name_errors)

        Wizard.addPage(self.project_name_page)
        self.config_location_page = ConfigLocationPage()
        self.config_location_page.setObjectName(u"config_location_page")
        self.verticalLayout_12 = QVBoxLayout(self.config_location_page)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(25, 20, 25, 20)
        self.select_distributed_config = QRadioButton(self.config_location_page)
        self.select_distributed_config.setObjectName(u"select_distributed_config")
        self.select_distributed_config.setFocusPolicy(Qt.NoFocus)
        self.select_distributed_config.setStyleSheet(u"QRadioButton {\n"
"    font-size: 16px;\n"
"}\n"
"")

        self.verticalLayout_12.addWidget(self.select_distributed_config)

        self.distributed_config_subheader = QLabel(self.config_location_page)
        self.distributed_config_subheader.setObjectName(u"distributed_config_subheader")
        self.distributed_config_subheader.setStyleSheet(u"font-size: 12px;\n"
"color: rgb(160, 160, 160);")
        self.distributed_config_subheader.setWordWrap(True)
        self.distributed_config_subheader.setIndent(20)

        self.verticalLayout_12.addWidget(self.distributed_config_subheader)

        self.select_centralized_config = QRadioButton(self.config_location_page)
        self.select_centralized_config.setObjectName(u"select_centralized_config")
        self.select_centralized_config.setFocusPolicy(Qt.NoFocus)
        self.select_centralized_config.setStyleSheet(u"QRadioButton {\n"
"    font-size: 16px;\n"
"}\n"
"")
        self.select_centralized_config.setChecked(True)

        self.verticalLayout_12.addWidget(self.select_centralized_config)

        self.centralized_config_subheader = QLabel(self.config_location_page)
        self.centralized_config_subheader.setObjectName(u"centralized_config_subheader")
        self.centralized_config_subheader.setStyleSheet(u"font-size: 12px;\n"
"color: rgb(160, 160, 160);")
        self.centralized_config_subheader.setWordWrap(True)
        self.centralized_config_subheader.setIndent(20)

        self.verticalLayout_12.addWidget(self.centralized_config_subheader)

        self.config_location_frame = QFrame(self.config_location_page)
        self.config_location_frame.setObjectName(u"config_location_frame")
        self.config_location_frame.setFrameShape(QFrame.StyledPanel)
        self.config_location_frame.setFrameShadow(QFrame.Raised)
        self.storage_grid_layout = QGridLayout(self.config_location_frame)
        self.storage_grid_layout.setObjectName(u"storage_grid_layout")
        self.mac_path = QLineEdit(self.config_location_frame)
        self.mac_path.setObjectName(u"mac_path")

        self.storage_grid_layout.addWidget(self.mac_path, 2, 1, 1, 1)

        self.windows_browse = QPushButton(self.config_location_frame)
        self.windows_browse.setObjectName(u"windows_browse")
        self.windows_browse.setEnabled(True)

        self.storage_grid_layout.addWidget(self.windows_browse, 0, 2, 1, 1)

        self.linux_path = QLineEdit(self.config_location_frame)
        self.linux_path.setObjectName(u"linux_path")

        self.storage_grid_layout.addWidget(self.linux_path, 1, 1, 1, 1)

        self.mac_browse = QPushButton(self.config_location_frame)
        self.mac_browse.setObjectName(u"mac_browse")
        self.mac_browse.setEnabled(True)

        self.storage_grid_layout.addWidget(self.mac_browse, 2, 2, 1, 1)

        self.linux_browse = QPushButton(self.config_location_frame)
        self.linux_browse.setObjectName(u"linux_browse")
        self.linux_browse.setEnabled(True)

        self.storage_grid_layout.addWidget(self.linux_browse, 1, 2, 1, 1)

        self.linux_label = QLabel(self.config_location_frame)
        self.linux_label.setObjectName(u"linux_label")
        self.linux_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.storage_grid_layout.addWidget(self.linux_label, 1, 0, 1, 1)

        self.windows_path = QLineEdit(self.config_location_frame)
        self.windows_path.setObjectName(u"windows_path")

        self.storage_grid_layout.addWidget(self.windows_path, 0, 1, 1, 1)

        self.windows_label = QLabel(self.config_location_frame)
        self.windows_label.setObjectName(u"windows_label")
        self.windows_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.storage_grid_layout.addWidget(self.windows_label, 0, 0, 1, 1)

        self.mac_label = QLabel(self.config_location_frame)
        self.mac_label.setObjectName(u"mac_label")
        self.mac_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.storage_grid_layout.addWidget(self.mac_label, 2, 0, 1, 1)

        self.verticalLayout_12.addWidget(self.config_location_frame)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_12)

        self.config_location_errors = QLabel(self.config_location_page)
        self.config_location_errors.setObjectName(u"config_location_errors")
        self.config_location_errors.setStyleSheet(u"color: rgb(252, 98, 70);")
        self.config_location_errors.setAlignment(Qt.AlignCenter)
        self.config_location_errors.setWordWrap(True)

        self.verticalLayout_12.addWidget(self.config_location_errors)

        Wizard.addPage(self.config_location_page)
        self.progress_page = ProgressPage()
        self.progress_page.setObjectName(u"progress_page")
        self.verticalLayout_5 = QVBoxLayout(self.progress_page)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(25, -1, 25, -1)
        self.verticalSpacer_22 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_22)

        self.message = QLabel(self.progress_page)
        self.message.setObjectName(u"message")

        self.verticalLayout_5.addWidget(self.message)

        self.progress = QProgressBar(self.progress_page)
        self.progress.setObjectName(u"progress")

        self.verticalLayout_5.addWidget(self.progress)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.additional_details_button = QPushButton(self.progress_page)
        self.additional_details_button.setObjectName(u"additional_details_button")
        self.additional_details_button.setBaseSize(QSize(20, 32))
        self.additional_details_button.setFocusPolicy(Qt.NoFocus)
        self.additional_details_button.setAutoDefault(False)
        self.additional_details_button.setFlat(False)

        self.horizontalLayout_3.addWidget(self.additional_details_button)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.progress_output = QPlainTextEdit(self.progress_page)
        self.progress_output.setObjectName(u"progress_output")
        self.progress_output.setFocusPolicy(Qt.NoFocus)
        self.progress_output.setUndoRedoEnabled(False)
        self.progress_output.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.progress_output.setReadOnly(True)
        self.progress_output.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_5.addWidget(self.progress_output)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.complete_errors = QLabel(self.progress_page)
        self.complete_errors.setObjectName(u"complete_errors")
        self.complete_errors.setStyleSheet(u"color: rgb(252, 98, 70);")
        self.complete_errors.setAlignment(Qt.AlignCenter)
        self.complete_errors.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.complete_errors)

        Wizard.addPage(self.progress_page)
        self.summary_page = QWizardPage()
        self.summary_page.setObjectName(u"summary_page")
        self.gridLayout = QGridLayout(self.summary_page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setContentsMargins(25, 60, 25, 20)
        self.verticalSpacer_24 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_24, 5, 2, 1, 1)

        self.final_message = QLabel(self.summary_page)
        self.final_message.setObjectName(u"final_message")
        self.final_message.setStyleSheet(u"font-size: 16px;\n"
"color: rgb(141, 143, 143);")
        self.final_message.setTextFormat(Qt.RichText)
        self.final_message.setWordWrap(True)
        self.final_message.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.final_message, 6, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.setup_complete = QLabel(self.summary_page)
        self.setup_complete.setObjectName(u"setup_complete")
        self.setup_complete.setStyleSheet(u"font-size: 20px;")
        self.setup_complete.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.setup_complete, 4, 2, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.icon = QLabel(self.summary_page)
        self.icon.setObjectName(u"icon")
        self.icon.setMaximumSize(QSize(100, 100))
        self.icon.setPixmap(QPixmap(u":/tk-framework-adminui/setup_project/circle_logo.png"))
        self.icon.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.icon)

        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 2, 1, 1)

        self.verticalSpacer_25 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_25, 7, 2, 1, 1)

        Wizard.addPage(self.summary_page)
#if QT_CONFIG(shortcut)
        self.label_standard.setBuddy(self.select_standard)
        self.label_project.setBuddy(self.select_project)
        self.label_github.setBuddy(self.select_github)
        self.label_disk.setBuddy(self.select_disk)
        self.project_directories.setBuddy(self.project_name)
        self.distributed_config_subheader.setBuddy(self.select_standard)
        self.centralized_config_subheader.setBuddy(self.select_standard)
        self.linux_label.setBuddy(self.linux_path)
        self.windows_label.setBuddy(self.windows_path)
        self.mac_label.setBuddy(self.mac_path)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.project_list, self.github_url)
        QWidget.setTabOrder(self.github_url, self.disk_browse_button_dir)
        QWidget.setTabOrder(self.disk_browse_button_dir, self.project_name)
        QWidget.setTabOrder(self.project_name, self.windows_path)
        QWidget.setTabOrder(self.windows_path, self.windows_browse)
        QWidget.setTabOrder(self.windows_browse, self.linux_path)
        QWidget.setTabOrder(self.linux_path, self.linux_browse)
        QWidget.setTabOrder(self.linux_browse, self.mac_path)
        QWidget.setTabOrder(self.mac_path, self.mac_browse)
        QWidget.setTabOrder(self.mac_browse, self.project_name_scroll_area)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"Flow Production Tracking Set Up Project Wizard", None))
        self.setup_type_page.setTitle(QCoreApplication.translate("Wizard", u"<p></p><font size=18>&nbsp;Select a Configuration</font><p></p>", None))
        self.setup_type_page.setSubTitle(QCoreApplication.translate("Wizard", u"&nbsp;", None))
        self.setup_type_subheader.setText(QCoreApplication.translate("Wizard", u"<p style=\"line-height: 130%\">Base your Project's setup on one of the four options below.</p>", None))
        self.select_standard.setText(QCoreApplication.translate("Wizard", u"Flow Production Tracking Default", None))
        self.label_standard.setText(QCoreApplication.translate("Wizard", u"Use a standard configuration as a starting point for your Project.", None))
        self.select_project.setText(QCoreApplication.translate("Wizard", u"Another Project", None))
        self.label_project.setText(QCoreApplication.translate("Wizard", u"Use the configuration from another Project with this Project.", None))
        self.select_github.setText(QCoreApplication.translate("Wizard", u"Git", None))
        self.label_github.setText(QCoreApplication.translate("Wizard", u"Clone a configuration from a repository and use it for this Project.", None))
        self.select_disk.setText(QCoreApplication.translate("Wizard", u"Browse", None))
        self.label_disk.setText(QCoreApplication.translate("Wizard", u"Choose a configuration from a location on disk and use it for this Project.", None))
#if QT_CONFIG(tooltip)
        self.project_config_page.setToolTip(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Select a Project to copy the config from.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.project_config_page.setTitle(QCoreApplication.translate("Wizard", u"<p></p><font size=18>&nbsp;Select Another Project's Configuration</font><p></p>", None))
        self.project_config_page.setSubTitle(QCoreApplication.translate("Wizard", u"&nbsp;", None))
        self.project_config_subheader.setText(QCoreApplication.translate("Wizard", u"<p style=\"line-height: 130%\">Click on a Project to use it for this configuration.</p>", None))
        self.project_errors.setText("")
        self.github_config_page.setTitle(QCoreApplication.translate("Wizard", u"<p></p><font size=18>&nbsp;Select a Git Configuration</font><p></p>", None))
        self.github_config_page.setSubTitle(QCoreApplication.translate("Wizard", u"&nbsp;", None))
        self.github_config_subheader.setText(QCoreApplication.translate("Wizard", u"<p style=\"line-height: 130%\">Enter the Git URL to the repository that you want to use for this configuration.</p>", None))
#if QT_CONFIG(tooltip)
        self.github_url.setToolTip(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Enter the url to a github repo containing a configuration to clone.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.github_url.setText("")
        self.github_url.setPlaceholderText(QCoreApplication.translate("Wizard", u"Git URL", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Your url needs to end with .git, for example:<br/><br/><span style=\" font-family:'Courier New,courier'; font-size:12pt;\">https://github.com/shotgunsoftware/tk-config-default2.git<br/>git@github.com:shotgunsoftware/tk-config-default2.git</span></p></body></html>", None))
        self.github_errors.setText("")
        self.disk_config_page.setTitle(QCoreApplication.translate("Wizard", u"<p></p><font size=18>&nbsp;Browse for a Configuration</font><p></p>", None))
        self.disk_config_page.setSubTitle(QCoreApplication.translate("Wizard", u"&nbsp;", None))
        self.disk_config_subheader.setText(QCoreApplication.translate("Wizard", u"<p style=\"line-height: 130%\">Specify a path to the location on disk that you want to use for this configuration.</p>", None))
        self.folder_icon.setText("")
#if QT_CONFIG(tooltip)
        self.path.setToolTip(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Enter the path to a configuration on disk.  Either a valid configuration directory or a zip of one.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.path.setPlaceholderText(QCoreApplication.translate("Wizard", u"/Path/To/Configuration", None))
        self.disk_browse_button_zip.setText(QCoreApplication.translate("Wizard", u"&Choose zip...", None))
        self.disk_browse_button_dir.setText(QCoreApplication.translate("Wizard", u"&Choose directory...", None))
        self.label_2.setText(QCoreApplication.translate("Wizard", u"Please select either a folder or a zip file.", None))
        self.disk_errors.setText("")
        self.storage_map_page.setTitle(QCoreApplication.translate("Wizard", u"<p></p><font size=18>&nbsp;Define Storages</font><p></p>", None))
        self.storage_map_page.setSubTitle(QCoreApplication.translate("Wizard", u"&nbsp;", None))
        self.storage_def_lbl.setText(QCoreApplication.translate("Wizard", u"This configuration requires one or more filesystem roots where files will be stored. For each filesystem root required by this configuration on the left, specify an associated Flow Production Tracking Local Storage on the right that defines the paths for the operating systems you use. <a href=\"https://help.autodesk.com/view/SGSUB/ENU/?guid=SG_Administrator_ar_data_management_ar_linking_local_files_html\">More info\u2026</a>", None))
        self.local_file_link_lbl.setText(QCoreApplication.translate("Wizard", u"Linking to local files must be enabled in your <a href=\"https://help.autodesk.com/view/SGSUB/ENU/?guid=SG_Administrator_ar_data_management_ar_linking_local_files_html\">Flow Production Tracking Preferences</a>", None))
        self.storage_errors.setText("")
        self.project_name_page.setTitle(QCoreApplication.translate("Wizard", u"<p></p><font size=18>&nbsp;Project Folder Name</font><p></p>", None))
        self.project_name_page.setSubTitle(QCoreApplication.translate("Wizard", u"&nbsp;", None))
        self.project_name_subheader.setText(QCoreApplication.translate("Wizard", u"<p style=\"line-height: 130%\">Enter the name you want to use for the Project folder on disk.</p>", None))
#if QT_CONFIG(tooltip)
        self.project_name.setToolTip(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Enter a valid project name.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.project_name.setPlaceholderText(QCoreApplication.translate("Wizard", u"Name", None))
        self.project_directories.setText(QCoreApplication.translate("Wizard", u"The following project folders will be created:", None))
        self.project_name_errors.setText("")
        self.config_location_page.setTitle(QCoreApplication.translate("Wizard", u"<p></p><font size=18>&nbsp;Select Deployment</font><p></p>", None))
        self.config_location_page.setSubTitle(QCoreApplication.translate("Wizard", u"&nbsp;", None))
        self.select_distributed_config.setText(QCoreApplication.translate("Wizard", u"Distributed Setup", None))
        self.distributed_config_subheader.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p>The configuration will be uploaded to Flow Production Tracking. As a user starts up their content creation software, Toolkit will automatically download the configuration and all its dependencies.</p></body></html>", None))
        self.select_centralized_config.setText(QCoreApplication.translate("Wizard", u"Centralized Setup", None))
        self.centralized_config_subheader.setText(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Your Project's pipeline configuration will to be installed in a shared location. All users need to access the configuration from this location. If you use multiple operating systems, enter the equivalent path for each.</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.mac_path.setToolTip(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Enter the path on disk where the configuration will be stored.</p><p>The current operating system's directory will be used to install the configuration.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.mac_path.setPlaceholderText(QCoreApplication.translate("Wizard", u"/Path/On/Mac", None))
        self.windows_browse.setText(QCoreApplication.translate("Wizard", u"Browse...", None))
#if QT_CONFIG(tooltip)
        self.linux_path.setToolTip(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Enter the path on disk where the configuration will be stored.</p><p>The current operating system's directory will be used to install the configuration.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.linux_path.setPlaceholderText(QCoreApplication.translate("Wizard", u"/path/on/linux", None))
        self.mac_browse.setText(QCoreApplication.translate("Wizard", u"Browse...", None))
        self.linux_browse.setText(QCoreApplication.translate("Wizard", u"Browse...", None))
        self.linux_label.setText(QCoreApplication.translate("Wizard", u"Linux", None))
#if QT_CONFIG(tooltip)
        self.windows_path.setToolTip(QCoreApplication.translate("Wizard", u"<html><head/><body><p>Enter the path on disk where the configuration will be stored.</p><p>The current operating system's directory will be used to install the configuration.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.windows_path.setPlaceholderText(QCoreApplication.translate("Wizard", u"\\\\Path\\On\\Windows", None))
        self.windows_label.setText(QCoreApplication.translate("Wizard", u"Windows", None))
        self.mac_label.setText(QCoreApplication.translate("Wizard", u"Mac", None))
        self.config_location_errors.setText("")
        self.progress_page.setTitle(QCoreApplication.translate("Wizard", u"<p></p><font size=18>&nbsp;Hang on, setting up your project</font><p></p>", None))
        self.progress_page.setSubTitle(QCoreApplication.translate("Wizard", u"&nbsp;", None))
        self.message.setText("")
        self.additional_details_button.setText(QCoreApplication.translate("Wizard", u"Show Details", None))
        self.complete_errors.setText("")
        self.final_message.setText(QCoreApplication.translate("Wizard", u"Toolkit is now ready to use in your Project!<br/>\n"
"<br/>\n"
"For more information on how to configure your Project and tailor it to your system, <a href=\"https://developer.shotgridsoftware.com/5d83a936/?title=Configuration+Setup\" style=\"color: rgb(203, 205, 205);\">click here to check out our documentation</a>.", None))
        self.setup_complete.setText(QCoreApplication.translate("Wizard", u"<big>Project Setup Complete</big>", None))
        self.icon.setText("")
    # retranslateUi
