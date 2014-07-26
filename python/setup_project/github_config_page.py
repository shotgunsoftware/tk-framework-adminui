# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import random

from sgtk.platform.qt import QtGui
from sgtk.platform.qt import QtCore

from .base_page import UriSelectionPage
from ..ui import resources_rc


class GithubConfigPage(UriSelectionPage):
    """ Page to base a configuration on a github repo. """
    def setup_ui(self, page_id):
        UriSelectionPage.setup_ui(self, page_id)
        wiz = self.wizard()

        # set the default text
        default_text = "https://www.github.com"
        wiz.ui.github_url.setText(default_text)
        wiz.ui.github_url.setSelection(0, len(default_text))

    def initializePage(self):
        # pick a random octocat
        cats = []
        dir_iter = QtCore.QDirIterator(
            ":tk-framework-adminui/setup_project/octocats", QtCore.QDirIterator.Subdirectories)

        cat = dir_iter.next()
        while cat:
            cats.append(cat)
            cat = dir_iter.next()

        if cats:
            selected = random.choice(cats)
            wiz = self.wizard()
            wiz.ui.octocat.setPixmap(selected)

    def validatePage(self):
        wiz = self.wizard()
        uri = self.field("github_url")
        if not uri.endswith(".git"):
            wiz.ui.github_errors.setText("Error, the url does not end in '.git'")
            return False

        try:
            self._storage_locations_page.set_uri(uri)
            wiz.ui.github_errors.setText("")
        except Exception, e:
            wiz.ui.github_errors.setText(str(e))
            return False

        return True
