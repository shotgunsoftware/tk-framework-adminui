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

from .base_page import BasePage


class GithubConfigPage(BasePage):
    """ Page to base a configuration on a github repo. """
    def setup_ui(self, page_id):
        BasePage.setup_ui(self, page_id)
        wiz = self.wizard()

        # set the default text
        default_text = "https://www.github.com"
        wiz.ui.github_url.setText(default_text)
        wiz.ui.github_url.setSelection(0, len(default_text))

    def validatePage(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        wiz = self.wizard()
        uri = self.field("github_url")
        if not uri.endswith(".git"):
            wiz.ui.github_errors.setText("Error, the url does not end in '.git'")
            QtGui.QApplication.restoreOverrideCursor()
            return False

        try:
            wiz.core_wizard.set_config_uri(uri)
            wiz.ui.github_errors.setText("")
            QtGui.QApplication.restoreOverrideCursor()
        except Exception, e:
            wiz.ui.github_errors.setText(str(e))
            QtGui.QApplication.restoreOverrideCursor()
            return False

        return True
