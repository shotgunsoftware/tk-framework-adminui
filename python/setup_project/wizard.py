# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import logging
import os

import sgtk
from sgtk.platform.qt import QtGui
from sgtk.platform.qt import QtCore

from ..ui import setup_project
from .emitting_handler import EmittingHandler


class SetupProjectWizard(QtGui.QWizard):
    """
    A GUI wizard to setup a project for toolkit.

    This wraps the setup_project core command.
    """
    def __init__(self, project, parent=None):
        QtGui.QWizard.__init__(self, parent)

        # Disable Close button. Note that on mac, need to disable minimize
        # button also to do this (but maximize can stay). 
        self.setWindowFlags(QtCore.Qt.Tool | 
                            QtCore.Qt.CustomizeWindowHint | 
                            QtCore.Qt.WindowTitleHint | 
                            QtCore.Qt.WindowMaximizeButtonHint)

        # Set stylesheet modification for this wizard
        self.setStyleSheet("QLineEdit:Disabled {background-color: rgb(60, 60, 60); color: rgb(128, 128, 128);}")

        # setup the command wizard from core
        wizard_factory = sgtk.get_command("setup_project_factory")

        # setup logging
        self._logger = logging.getLogger("tk-framework-adminui.setup_project")
        self._handler = EmittingHandler()
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(self._handler)
        wizard_factory.set_logger(self._logger)

        # run the factory to grab the wizard
        self.core_wizard = wizard_factory.execute({})
        self.core_wizard.set_project(project["id"])

        # setup the GUI
        self.ui = setup_project.Ui_Wizard()
        self.ui.setupUi(self)

        # hook up logging
        self._handler.connect(self.ui.progress_page.append_log_message)

        # hook up help handling
        self.helpRequested.connect(self._on_help_requested)

        # Setup fields
        self.ui.github_config_page.registerField("github_url*", self.ui.github_url)
        self.ui.disk_config_page.registerField("disk_path*", self.ui.path)
        self.ui.project_name_page.registerField("project_name*", self.ui.project_name)
        self.ui.config_location_page.registerField("config_path_mac", self.ui.mac_path)
        self.ui.config_location_page.registerField("config_path_win", self.ui.windows_path)
        self.ui.config_location_page.registerField("config_path_linux", self.ui.linux_path)

        # Let each page set itself up
        for page_id in self.pageIds():
            page = self.page(page_id)
            if hasattr(page, "setup_ui"):
                self.page(page_id).setup_ui(page_id)

        # Setup Page Order
        self.ui.setup_type_page.set_default_configs_page(self.ui.default_configs_page)
        self.ui.setup_type_page.set_project_page(self.ui.project_config_page)
        self.ui.setup_type_page.set_github_page(self.ui.github_config_page)
        self.ui.setup_type_page.set_disk_page(self.ui.disk_config_page)

        self.ui.project_name_page.set_next_page(self.ui.config_location_page)
        self.ui.config_location_page.set_next_page(self.ui.progress_page)

        self.ui.config_location_page.setCommitPage(True)
        self.ui.summary_page.setFinalPage(True)

        # Override button formatting
        self.setButtonText(self.NextButton, "Continue")
        self.setButtonText(self.BackButton, "Back")
        self.setButtonText(self.FinishButton, "Done")
        self.setButtonText(self.CommitButton, "Run Setup")
        self.button(self.NextButton).setStyleSheet("background-color: rgb(16, 148,223);")
        self.button(self.FinishButton).setStyleSheet("background-color: rgb(16, 148,223);")
        self.button(self.CommitButton).setStyleSheet("background-color: rgb(16, 148,223);")

        # load the stylesheet
        self._load_stylesheet()

    def closeEvent(self, event):
        """
        Disables Alt-F4 on windows and prevents user from cancelling mid-operation and
        leaving the configuration in an un-recoverable state.
        """
        event.ignore()

    def _on_help_requested(self):
        # forward help request to current page
        page = self.currentPage()
        page.help_requested()

    def validate_config_uri(self, uri):
        """Download and validate the supplied config URI.

        This will also update the wizard to display the required storages for
        mapping by the user.
        """

        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            # download and validate the uri and update the required storages.
            # let any exceptions propagate up to the calling page to be handled
            storage_info = self.core_wizard.validate_config_uri(uri)

            # set the uri for the storage mapping page
            self.ui.storage_map_page.set_config_uri(uri)

            # add mappings for each required storage root. clear any existing
            # roots first (possible if back button is used)
            self.ui.storage_map_page.clear_roots()
            for (root_name, root_info) in storage_info.iteritems():
                self.ui.storage_map_page.add_mapping(root_name, root_info)

            # a config has been chosen. we don't need to visit the other config
            # selection pages. make the next page the storage mapping page.
            current_page = self.currentPage()
            current_page.set_next_page(self.ui.storage_map_page)

        finally:
            QtGui.QApplication.restoreOverrideCursor()

    def _load_stylesheet(self):
        """
        Loads in a stylesheet from disk
        """
        qss_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "style.qss"
        )
        f = None
        try:
            f = open(qss_file, "rt")
            qss_data = f.read()
            # apply to widget (and all its children)
            self.setStyleSheet(qss_data)
        finally:
            if f:
                f.close()
