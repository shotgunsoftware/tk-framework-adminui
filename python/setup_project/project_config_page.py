# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sys

from sgtk.platform.qt import QtGui
from sgtk.platform.qt import QtCore

from sgtk.util import shotgun
from sgtk.platform import constants

from .project_model import ProjectModel
from .project_delegate import ProjectDelegate

from .base_page import BasePage


class ProjectConfigPage(BasePage):
    """ Page to base a configuration on that of another project's. """
    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self._valid_selection = False

    def setup_ui(self, page_id):
        BasePage.setup_ui(self, page_id)

        # setup the model and delegate for the list view
        wiz = self.wizard()
        self.project_model = ProjectModel(wiz.ui.project_list)
        self.project_delegate = ProjectDelegate(wiz.ui.project_list)
        wiz.ui.project_list.setModel(self.project_model)
        wiz.ui.project_list.setItemDelegate(self.project_delegate)

        # hook up the selection changed
        selection = wiz.ui.project_list.selectionModel()
        selection.selectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self, selected, deselected):
        # turn on wait cursor
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        wiz = self.wizard()
        indexes = selected.indexes()
        if len(indexes) == 0:
            # selection has been cleared, reset the config uri
            self._valid_selection = False
            wiz.core_wizard.set_config_uri(None)
        else:
            # get the primary config path from Shotgun for the selected project
            project_id = indexes[0].data(ProjectModel.PROJECT_ID_ROLE)
            sg = shotgun.create_sg_connection()

            filters = [
                ["code", "is", constants.PRIMARY_PIPELINE_CONFIG_NAME],
                ["project", "is", {"type": "Project", "id": project_id}],
            ]
            fields = ["code", "mac_path", "windows_path", "linux_path"]
            configuration = sg.find_one(
                constants.PIPELINE_CONFIGURATION_ENTITY, filters, fields=fields)

            config_uri = None
            if configuration is not None:
                if sys.platform == "win32":
                    config_uri = configuration.get("windows_path")
                elif sys.platform == "darwin":
                    config_uri = configuration.get("mac_path")
                elif sys.platform.startswith("linux"):
                    config_uri = configuration.get("linux_path")

            if config_uri:
                # got back a value, validate it
                config_uri = os.path.join(config_uri, "config")
                try:
                    # test the config and clear errors on success
                    wiz.core_wizard.set_config_uri(config_uri)
                    self._valid_selection = True
                    wiz.ui.project_errors.setText("")
                except Exception, e:
                    self._valid_selection = False
                    wiz.ui.project_errors.setText(str(e))
            else:
                # did not get a valid configuration
                self._valid_selection = False
                project_name = indexes[0].data(ProjectModel.DISPLAY_NAME_ROLE)
                wiz.ui.project_errors.setText("Could not load configuration for '%s'" % project_name)

        # restore the regular cursor
        QtGui.QApplication.restoreOverrideCursor()

        # signal the wizard that the Next button's state may have changed
        self.completeChanged.emit()

    def isComplete(self):
        return self._valid_selection
