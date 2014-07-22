# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sys
from sgtk.platform.qt import QtGui
from sgtk.platform.qt import QtCore

from .base_page import BasePage


class ConfigLocationPage(BasePage):
    """ Page to specify the location for the configuration. """
    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self._path_label = None
        self._path_field = None

    def setup_ui(self, page_id):
        BasePage.setup_ui(self, page_id)

        # enable browse button for this os
        wiz = self.wizard()
        if sys.platform == "darwin":
            browse = self.wizard().ui.mac_browse
            self._path_label = wiz.ui.mac_path
            self._path_field = "config_path_mac"
        elif sys.platform == "win32":
            browse = self.wizard().ui.windows_browse
            self._path_label = wiz.ui.windows_path
            self._path_field = "config_path_win"
        elif sys.platform.startswith("linux"):
            browse = self.wizard().ui.linux_browse
            self._path_label = wiz.ui.linux_path
            self._path_field = "config_path_linux"

        browse.setEnabled(True)
        browse.pressed.connect(self._on_browse_pressed)

    def _on_browse_pressed(self):
        config_dir = QtGui.QFileDialog.getExistingDirectory(
            self, "Choose configuration", None,
            QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontConfirmOverwrite)
        self.setField(self._path_field, config_dir)

    def initializePage(self):
        # setup the default locations
        # this must be done in initializePage since the answers depend on previous field values
        wiz = self.wizard()
        default_locations = wiz.core_wizard.get_default_configuration_location()
        self.wizard().ui.linux_path.setText(default_locations["linux2"])
        self.wizard().ui.windows_path.setText(default_locations["win32"])
        self.wizard().ui.mac_path.setText(default_locations["darwin"])

    def validatePage(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        macosx_path = self.field("config_path_mac")
        linux_path = self.field("config_path_linux")
        windows_path = self.field("config_path_win")

        # pass the paths to the wizard and make sure they are ok
        wiz = self.wizard()
        try:
            wiz.core_wizard.set_configuration_location(linux_path, windows_path, macosx_path)
            wiz.core_wizard._params.validate_config_io()
            wiz.ui.config_location_errors.setText("")
            QtGui.QApplication.restoreOverrideCursor()
        except Exception, e:
            wiz.ui.config_location_errors.setText(str(e))
            QtGui.QApplication.restoreOverrideCursor()
            return False

        return True
