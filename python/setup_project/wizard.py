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

from sgtk.platform.qt import QtGui

from ..ui import setup_project
from .emitting_handler import EmittingHandler

import sgtk


class SetupProjectWizard(QtGui.QWizard):
    """
    A GUI wizard to setup a project for toolkit.

    This wraps the setup_project core command.
    """
    def __init__(self, project, parent=None):
        QtGui.QWizard.__init__(self, parent)

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

        # Setup fields
        self.ui.github_config_page.registerField("github_url*", self.ui.github_url)
        self.ui.disk_config_page.registerField("disk_path*", self.ui.path)
        self.ui.project_name_page.registerField("project_name*", self.ui.project_name)
        self.ui.config_location_page.registerField("config_path_mac", self.ui.mac_path)
        self.ui.config_location_page.registerField("config_path_win", self.ui.windows_path)
        self.ui.config_location_page.registerField("config_path_linux", self.ui.linux_path)

        # Let each page set itself up
        for page_id in self.pageIds():
            self.page(page_id).setup_ui(page_id)

        # Setup Page Order
        self.ui.setup_type_page.set_default_configs_page(self.ui.default_configs_page)
        self.ui.setup_type_page.set_project_page(self.ui.project_config_page)
        self.ui.setup_type_page.set_github_page(self.ui.github_config_page)
        self.ui.setup_type_page.set_disk_page(self.ui.disk_config_page)

        self.ui.default_configs_page.set_storage_locations_page(self.ui.storage_locations_page)
        self.ui.project_config_page.set_storage_locations_page(self.ui.storage_locations_page)
        self.ui.github_config_page.set_storage_locations_page(self.ui.storage_locations_page)
        self.ui.disk_config_page.set_storage_locations_page(self.ui.storage_locations_page)

        self.ui.storage_locations_page.set_next_page(self.ui.project_name_page)
        self.ui.project_name_page.set_next_page(self.ui.config_location_page)
        self.ui.config_location_page.set_next_page(self.ui.progress_page)

        self.ui.config_location_page.setCommitPage(True)

        # Override button formatting
        self.setButtonText(self.NextButton, "Continue")
        self.setButtonText(self.BackButton, "Back")
        self.setButtonText(self.FinishButton, "Done")
        self.button(self.NextButton).setStyleSheet("background-color: rgb(16, 148,223);")
        self.button(self.FinishButton).setStyleSheet("background-color: rgb(16, 148,223);")
