# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from sgtk.platform.qt import QtGui
from sgtk.platform.qt import QtCore

from .base_page import UriSelectionPage


class DiskConfigPage(UriSelectionPage):
    """ Page to base a configuration on a disk location. """
    def setup_ui(self, page_id):
        UriSelectionPage.setup_ui(self, page_id)

        wiz = self.wizard()
        wiz.ui.disk_browse_button.pressed.connect(self._on_browse_pressed)

    def _on_browse_pressed(self):
        config_dir = QtGui.QFileDialog.getExistingDirectory(
            self, "Choose configuration", None,
            QtGui.QFileDialog.ShowDirsOnly |
            QtGui.QFileDialog.DontConfirmOverwrite |
            QtGui.QFileDialog.ReadOnly)
        self.setField("disk_path", config_dir)

    def validatePage(self):
        uri = self.field("disk_path")
        wiz = self.wizard()
        try:
            self._storage_locations_page.set_uri(uri)
            wiz.ui.disk_errors.setText("")
        except Exception, e:
            wiz.ui.disk_errors.setText(str(e))
            return False

        return True
