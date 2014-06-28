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

from PySide import QtGui

from .ui import setup_project


class SetupProject(QtGui.QWizard):
    def __init__(self, parent=None):
        QtGui.QWizard.__init__(self, parent)

        self.ui = setup_project.Ui_Wizard()
        self.ui.setupUi(self)

        # override button formatting
        self.setButtonText(self.NextButton, "Continue")
        self.setButtonText(self.BackButton, "Back")
        self.button(self.NextButton).setStyleSheet("background-color: rgb(16, 148,223);")

        # enable browse button for this os
        if sys.platform == "darwin":
            self.ui.mac_browse.setEnabled(True)
        elif sys.platform == "win32":
            self.ui.windows_browse.setEnabled(True)
        elif sys.platform.startswith("linux"):
            self.ui.linux_browse.setEnabled(True)
