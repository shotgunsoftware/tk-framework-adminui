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

from .base_page import BasePage


class StorageLocationsPage(BasePage):
    """ Page to collect the needed storages for the selected config. """
    def __init__(self, parent=None):
        BasePage.__init__(self, parent)

        self._uri = None
        self._storage_info = None
        self._store_path_widgets = {}

    def _is_store_valid(self, store_info):
        """ returns True if the store should be valid.  False otherwise """
        return store_info["exists_on_disk"] and store_info["defined_in_shotgun"]

    def show_page(self):
        """ Returns true if the config needs primary storages setup. """
        if self._storage_info is None:
            # no storages set, don't show the page
            return False

        # see if any of the storages need to be created or if the paths are invalid
        for info in self._storage_info.values():
            if not self._is_store_valid(info):
                return True

        # everything is valid, no need to show the page
        return False

    def set_uri(self, uri):
        """
        Set the uri for the wizard.

        This will validate the uri and if it is valid and all the storages are
        valid then it will set the uri.

        If the uri is not valid, then the exception that validation raises is passed up.

        If the uri is valid, but the storages are not, then the uri is cached and this
        page signals that it needs to be shown.  The uri will be set upon successful
        configuration of all of the needed storages.
        """
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            self._uri = uri

            # pass exceptions from this up so each page can deal with them in a page specific way
            wiz = self.wizard()
            self._storage_info = wiz.core_wizard.validate_config_uri(uri)

            if self.show_page():
                # going to show the page, set up the gui
                self._setup_widgets()
            else:
                # everything is all setup, actually set the uri
                wiz.core_wizard.set_config_uri(self._uri)
        finally:
            QtGui.QApplication.restoreOverrideCursor()

    def _setup_widgets(self):
        """ clear and setup the widgets on the page to reflect the current storage info """
        # widgets that are static, created from designer
        wiz = self.wizard()
        designer_widgets = [wiz.ui.storage_errors, wiz.ui.storage_note]

        # clear the layout
        layout = self.layout()
        layout.setColumnStretch(1, 1)
        for i in range(layout.count()):
            w = layout.takeAt(0)
            if w not in designer_widgets:
                del w
        self._store_path_widgets = {}

        # Setup a group of line edits per storage
        os_specifics = [
            ("Mac", "darwin", sys.platform == "darwin"),
            ("Windows", "win32", sys.platform == "win32"),
            ("Linux", "linux2", sys.platform.startswith("linux")),
        ]

        row = 0
        for (store_name, store_info) in self._storage_info.iteritems():
            # see if we don't need to do anything for this storage
            if self._is_store_valid(store_info):
                continue

            # setup title and subtitle
            store_title = QtGui.QLabel("<big>%s</big>" % store_name.title(), self)
            layout.addWidget(store_title, row, 0, 1, 3)
            store_subtitle = QtGui.QLabel(store_info["description"], self)
            layout.addWidget(store_subtitle, row+1, 0, 1, 3)
            row += 2

            # setup the operating systems
            self._store_path_widgets[store_name] = {}
            for (os_display, os_key, os_current) in os_specifics:
                # setup the os widgets
                os_label = QtGui.QLabel("%s:" % os_display, self)
                os_path = QtGui.QLineEdit(self)

                # populate with existing paths
                if store_info[os_key]:
                    os_path.setText(store_info[os_key])

                # don't allow editing data from Shotgun, too dangerous
                if store_info["defined_in_shotgun"] and store_info[os_key]:
                    os_path.setReadOnly(True)
                    os_path.setEnabled(False)

                # keep around the line edits for validation
                self._store_path_widgets[store_name][os_key] = os_path

                # only create the browse button for the current os if
                #  the storage is not in Shotgun or
                #  the storage is blank in Shotgun
                create_browse = os_current and (
                    not store_info["defined_in_shotgun"] or
                    (store_info["defined_in_shotgun"] and not store_info[os_key])
                )
                if create_browse:
                    os_button = QtGui.QPushButton("Browse...", self)

                    # connect the button to populate the os specific path
                    def generate_on_browse_clicked(path_widget):
                        # generate the slot as a closure to capture the current widget
                        def ret():
                            storage_dir = QtGui.QFileDialog.getExistingDirectory(
                                self, "Choose storage root", None,
                                QtGui.QFileDialog.ShowDirsOnly |
                                QtGui.QFileDialog.DontConfirmOverwrite)
                            path_widget.setText(storage_dir)
                        return ret
                    os_button.pressed.connect(generate_on_browse_clicked(os_path))

                # add the widgets to the layout
                layout.addWidget(os_label, row, 0, 1, 1)
                if create_browse:
                    layout.addWidget(os_path, row, 1, 1, 1)
                    layout.addWidget(os_button, row, 2, 1, 1)
                else:
                    layout.addWidget(os_path, row, 1, 1, 2)
                row += 1

        # add a spacer since PySide uic compilation doesn't track spacers in a code accessible way
        spacer = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacer, row, 0, 1, 3)
        row += 1

        # reset the designer widgets so they are placed correctly
        for w in designer_widgets:
            layout.addWidget(w, row, 0, 1, 3)
            row += 1

    def validatePage(self):
        # clear any errors
        wiz = self.wizard()
        wiz.ui.storage_errors.setText("")

        # get the os key for the current platform
        current_os = sys.platform
        if current_os.startswith("linux"):
            current_os = "linux2"

        # gather the different kinds of operations we might have to do
        invalid = []
        not_on_disk = []
        update_in_shotgun = []
        create_in_shotgun = []
        invalid_in_shotgun = []
        for (store_name, store_info) in self._storage_info.iteritems():
            # only do work for invalid stores
            if self._is_store_valid(store_info):
                continue

            # grab the path for the operating systems
            current_os_path = str(self._store_path_widgets[store_name][current_os].text())
            mac_path = str(self._store_path_widgets[store_name]["darwin"].text())
            windows_path = str(self._store_path_widgets[store_name]["win32"].text())
            linux_path = str(self._store_path_widgets[store_name]["linux2"].text())

            if store_info["defined_in_shotgun"]:
                # see if any shotgun values have changed
                # only values that started blank were set to read/write
                update_data = {}
                for (os_path, os_key, sg_key) in [
                        (mac_path, "darwin", "mac_path"),
                        (windows_path, "win32", "windows_path"),
                        (linux_path, "linux2", "linux_path")]:
                    if os_path and os_path != store_info[os_key]:
                        if os.path.isabs(os_path):
                            # path was defined, changed, and valid.  Add it to the update data
                            update_data[sg_key] = os_path
                        else:
                            # path is not valid, add it to the list of invalids
                            invalid.append(store_name)

                # if there were changes, add them to the update list
                if update_data:
                    update_data["code"] = store_name
                    update_in_shotgun.append(update_data)

                # special checks for current operating system
                if current_os_path and os.path.isabs(current_os_path):
                    if not os.path.exists(current_os_path):
                        not_on_disk.append(current_os_path)
                elif store_info[current_os] and current_os_path == store_info[current_os]:
                    # path is invalid in Shotgun
                    # (if it were changed and invalid it would be picked up above)
                    invalid_in_shotgun.append((store_name, current_os_path))
            else:
                # not in shotgun need to make sure the path is filled out and valid
                if not current_os_path or not os.path.isabs(current_os_path):
                    invalid.append(store_name)
                else:
                    # valid path, add to the create list
                    create_in_shotgun.append({
                        "code": store_name,
                        "mac_path": mac_path,
                        "windows_path": windows_path,
                        "linux_path": linux_path,
                    })

                    # and see if we are going to have to create the path
                    if not os.path.exists(current_os_path):
                        not_on_disk.append(current_os_path)

        # if anything is invalid in Shotgun, then we aren't going to be able to continue
        if invalid_in_shotgun:
            # display a message about the invalid paths
            message = "There are invalid paths in Shotgun.  Please correct the following in the " \
                "File Management section of your Shotgun preferences and then try setting up the " \
                "project again:\n\n"
            for (store_name, path) in invalid_in_shotgun:
                message += "   %s - '%s'\n" % (store_name, path)
            wiz.ui.storage_errors.setText(message)
            return False

        # if local paths don't exist see if we can create them
        if not_on_disk:
            # prompt for permission
            message = "There are paths that do not exist.  Try to create them?\n\n"
            for path in not_on_disk:
                message += "  %s\n" % path
            response = QtGui.QMessageBox.warning(
                self, "Create paths", message,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
            if response == QtGui.QMessageBox.No:
                return False

            # got the go ahead, try to create the directories
            error_paths = []
            for path in not_on_disk:
                try:
                    os.makedirs(path)
                except Exception, e:
                    error_paths.append((path, e))
            if error_paths:
                # could not create all the directories, report and bail
                message = "Got the following errors creating the directories:\n"
                for (path, error) in error_paths:
                    message += "  %s - %s\n" % (path, str(error))
                QtGui.QMessageBox.critical(self, "Error creating directories.", message)
                return False

        # report if invalid paths were entered
        if invalid:
            error = "All paths must be filled out with absolute paths."
            wiz.ui.storage_errors.setText(error)
            return False

        # do creates and updates in shotgun
        batch = []
        sg = shotgun.create_sg_connection()
        batch.extend([{
            "request_type": "create",
            "entity_type": "LocalStorage",
            "data": data,
        } for data in create_in_shotgun])

        # grab the ids for the local storages from Shotgun
        # NOTE: this is temporary until the store_info dictionary includes the id
        if update_in_shotgun:
            local_stores = sg.find("LocalStorage", [], fields=["code", "id"])
            local_store_map = dict([(s["code"], s["id"]) for s in local_stores])

        batch.extend([{
            "request_type": "update",
            "entity_type": "LocalStorage",
            "entity_id": local_store_map[data["code"]],
            "data": data,
        } for data in update_in_shotgun])

        if batch:
            try:
                sg.batch(batch)
            except Exception, e:
                if create_in_shotgun and update_in_shotgun:
                    error = "Error creating and updating LocalStorage entities in Shotgun:\n%s" % str(e)
                elif update_in_shotgun:
                    error = "Error updating LocalStorage entities in Shotgun:\n%s" % str(e)
                else:
                    error = "Error creating LocalStorage entities in Shotgun:\n%s" % str(e)
                wiz.ui.storage_errors.setText(error)
                return False

        # if we made it here, then we should be all valid.  Try to set the config
        try:
            wiz.core_wizard.set_config_uri(self._uri)
        except Exception, e:
            error = "Unknown error when setting the configuration uri:\n%s" % str(e)
            wiz.ui.storage_errors.setText(error)
            return False

        # uri all set and all storages now valid
        return True
