# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from .base_page import BasePage


class ProjectNamePage(BasePage):
    """ Page to name a project. """
    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self.name_valid = False

    def setup_ui(self, page_id):
        BasePage.setup_ui(self, page_id)
        self.wizard().ui.project_name.textChanged.connect(self.on_name_changed)

    def initializePage(self):
        wiz = self.wizard()
        name = wiz.core_wizard.get_default_project_disk_name()
        self.setField("project_name", name)

    def on_name_changed(self, name):
        name = self.field("project_name")
        wiz = self.wizard()
        try:
            # update where the project folders will be for the given name
            wiz.core_wizard.set_project_disk_name(name)
            project_paths_dict = wiz.core_wizard.preview_project_paths(name)
            paths = []
            for platform in ["darwin", "linux2", "win32"]:
                for root in project_paths_dict:
                    paths.append(project_paths_dict[root][platform])
            formatted_paths = """
                <html><head/><body>
                <p><span style="font-size:large;">Project Directories will be:</span></p>
                <p>
                %s
                </p></body></html>
            """ % "<br/>\n".join(paths)
            wiz.ui.project_directories.setText(formatted_paths)
            wiz.ui.project_name_errors.setText("")
            self.name_valid = True
        except Exception, e:
            wiz.ui.project_directories.setText("")
            wiz.ui.project_name_errors.setText(str(e))
            self.name_valid = False

        # signal that the next button may have changed state
        self.completeChanged.emit()

    def isComplete(self):
        return self.name_valid
