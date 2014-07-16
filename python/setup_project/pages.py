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

from . import project_model
from . import project_delegate


class ShotgunPage(QtGui.QWizardPage):
    """ Base page for all Shotgun pages to inherit from. """
    def __init__(self, parent=None):
        """ Constructor """
        QtGui.QWizardPage.__init__(self, parent)
        self._page_id = None
        self._next_page_id = None

    def setup_ui(self, page_id):
        """ Setup page UI after the Wizard's UI has been setup from the uic. """
        self._page_id = page_id

    def page_id(self):
        return self._page_id

    def set_next_page(self, page):
        self._next_page_id = page.page_id()

    def nextId(self):
        if self._next_page_id is None:
            return QtGui.QWizardPage.nextId(self)

        return self._next_page_id


class SetupTypePage(ShotgunPage):
    """ Page to choose what configuration type to use. """
    def __init__(self, parent=None):
        ShotgunPage.__init__(self, parent)
        self._project_page_id = None
        self._github_page_id = None
        self._disk_page_id = None

    def setup_ui(self, page_id):
        ShotgunPage.setup_ui(self, page_id)

        # Setup buttongroup by hand since in PySide it breaks the ui compilation
        wiz = self.wizard()
        self._config_type_button_group = QtGui.QButtonGroup(self)
        self._config_type_button_group.addButton(wiz.ui.select_standard, 0)
        self._config_type_button_group.addButton(wiz.ui.select_project, 1)
        self._config_type_button_group.addButton(wiz.ui.select_github, 2)
        self._config_type_button_group.addButton(wiz.ui.select_disk, 3)

    def set_project_page(self, page):
        """ Set the page to switch to if project is selected. """
        self._project_page_id = page.page_id()

    def set_github_page(self, page):
        """ Set the page to switch to if github url is selected. """
        self._github_page_id = page.page_id()

    def set_disk_page(self, page):
        """ Set the page to switch to if disk location is selected. """
        self._disk_page_id = page.page_id()

    def nextId(self):
        selection = self._config_type_button_group.checkedId()
        if (selection == 1) and self._project_page_id is not None:
            return self._project_page_id
        elif (selection == 2) and self._github_page_id is not None:
            return self._github_page_id
        elif (selection == 3) and self._disk_page_id is not None:
            return self._disk_page_id

        return ShotgunPage.nextId(self)


class ProjectConfigPage(ShotgunPage):
    """ Page to base a configuration on that of another project's. """
    def setup_ui(self, page_id):
        ShotgunPage.setup_ui(self, page_id)

        # Setup the model and delegate for the list view
        wiz = self.wizard()
        self.project_model = project_model.ProjectModel(wiz.ui.project_list)
        self.project_delegate = project_delegate.ProjectDelegate(wiz.ui.project_list)
        wiz.ui.project_list.setModel(self.project_model)
        wiz.ui.project_list.setItemDelegate(self.project_delegate)

        selection = wiz.ui.project_list.selectionModel()
        selection.selectionChanged.connect(self._handle_selection_changed)

    def _handle_selection_changed(self, selected, deselected):
        self.project_id()
        self.completeChanged.emit()

    def isComplete(self):
        wiz = self.wizard()
        selection = wiz.ui.project_list.selectionModel()
        return selection.hasSelection()

    def project_id(self):
        wiz = self.wizard()
        selection = wiz.ui.project_list.selectionModel()
        return selection.currentIndex().data(project_model.ProjectModel.PROJECT_ID_ROLE)


class GithubConfigPage(ShotgunPage):
    """ Page to base a configuration on a github repo. """
    pass


class DiskConfigPage(ShotgunPage):
    """ Page to base a configuration on a disk location. """
    pass


class ProjectNamePage(ShotgunPage):
    """ Page to name a project. """
    pass


class ConfigLocationPage(ShotgunPage):
    """ Page to specify the location for the configuration. """
    def setup_ui(self, page_id):
        ShotgunPage.setup_ui(self, page_id)

        # enable browse button for this os
        if sys.platform == "darwin":
            browse = self.wizard().ui.mac_browse
            path = self.wizard().ui.linux_path
        elif sys.platform == "win32":
            browse = self.wizard().ui.windows_browse
            path = self.wizard().ui.windows_path
        elif sys.platform.startswith("linux"):
            browse = self.wizard().ui.linux_browse
            path = self.wizard().ui.linux_path

        browse.setEnabled(True)


class ProgressPage(ShotgunPage):
    """ Page to show the progress bar during configuration setup. """
    def initializePage(self):
        # Disable the cancel button
        wiz = self.wizard()
        button = wiz.button(wiz.CancelButton)
        button.setEnabled(False)

        fields = [
            "github_url",
            "disk_path",
            "project_name",
            "config_path_mac",
            "config_path_win",
            "config_path_linux",
        ]

        for field in fields:
            print "%s: %s" % (field, wiz.field(field))


class CompletePage(ShotgunPage):
    """ Page to show that the configuration has completed. """
    pass