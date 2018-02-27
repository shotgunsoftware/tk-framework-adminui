# Copyright (c) 2018 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import re
import sys
import traceback

import sgtk
from sgtk.platform.qt import QtGui
from sgtk.platform.qt import QtCore

log = sgtk.platform.get_logger(__name__)

from ..ui import create_storage_dialog

overlay = sgtk.platform.import_framework(
    "tk-framework-qtwidgets",
    "overlay_widget"
)


class CreateStorageDialog(QtGui.QDialog):
    """A dialog that allows a user to create a new local storage in SG."""

    # a regex that defines valid storage name
    STORAGE_NAME_REGEX = re.compile("^[\w\d]+$")

    def __init__(self, sg_connection, parent=None):
        """Initialize the create dialog."""

        super(CreateStorageDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Popup)

        # hold the sg connection while this exists (shouldn't be for long)
        self._sg_connection = sg_connection

        # query existing storages in SG for validation
        existing_storages = sg_connection.find(
            "LocalStorages",
            [],
            ["code", "id", "windows_path", "linux_path", "mac_path"]
        )

        # create a lookup by name
        self._existing_storage_lookup = {}
        for storage in existing_storages:
            storage_name = existing_storages["code"]
            self._existing_storage[storage_name] = storage

        # set up the UI
        self.ui = create_storage_dialog.Ui_CreateStorageDialog()
        self.ui.setupUi(self)

        # set up the overlay
        self._overlay = overlay.ShotgunOverlayWidget(self.ui.main_widget)

        # hide the info label by default
        self.ui.info.hide()

        # hide non-current os browse buttons
        if sys.platform.startswith("linux"):
            self.ui.mac_browse.hide()
            self.ui.windows_browse.hide()
        elif sys.platform == "darwin":
            self.ui.linux_browse.hide()
            self.ui.windows_browse.hide()
        elif sys.platform == "win32":
            self.ui.linux_browse.hide()
            self.ui.mac_browse.hide()
        else:
            # hide all browse buttons
            log.debug("Unrecognized platform: %s" % (sys.platform,))
            self.ui.linux_browse.hide()
            self.ui.mac_browse.hide()
            self.ui.windows_browse.hide()

        # keep a handle on the buttons
        self._accept_button = self.ui.button_box.button(
            QtGui.QDialogButtonBox.Save)
        self._close_button = self.ui.button_box.button(
            QtGui.QDialogButtonBox.Cancel)

        # connect the validation check method to text changes in the input boxes
        self.ui.linux_path.textChanged.connect(self._validation_check)
        self.ui.mac_path.textChanged.connect(self._validation_check)
        self.ui.windows_path.textChanged.connect(self._validation_check)
        self.ui.storage_name.textChanged.connect(self._validation_check)

        # connect the browse buttons
        self.ui.linux_browse.clicked.connect(
            lambda: self._browse_path(self.ui.linux_path))
        self.ui.mac_browse.clicked.connect(
            lambda: self._browse_path(self.ui.mac_path))
        self.ui.windows_browse.clicked.connect(
            lambda: self._browse_path(self.ui.windows_path))

        # connect the accept button the create action
        self._accept_button.clicked.connect(self._create_storage)

        # do an initial check for valid values
        self._validation_check()

    @property
    def linux_path(self):
        """The linux path to associate with the new storage"""
        return self.ui.linux_path.text()

    @linux_path.setter
    def linux_path(self, path):
        """Set the linux path to associate with the new storage"""
        self.ui.linux_path.setText(path)

    @property
    def mac_path(self):
        """The mac path to associate with the new storage"""
        return self.ui.mac_path.text()

    @mac_path.setter
    def mac_path(self, path):
        """Set the mac path to associate with the new storage"""
        self.ui.mac_path.setText(path)

    @property
    def storage_name(self):
        """The name of the storage to create."""
        return self.ui.storage_name.text()

    @property
    def windows_path(self):
        """The windows path to associate with the new storage"""
        return self.ui.windows_path.text()

    @windows_path.setter
    def windows_path(self, path):
        """Set the windows path to associate with the new storage"""
        self.ui.windows_path.setText(path)

    def is_valid(self):
        """Returns ``True`` if the input is valid, ``False`` otherwise."""

        # get the values once for efficiency
        storage_name = self.storage_name

        if not storage_name:
            # no storage name defined
            self._set_info("* Storage name is required.")
            return False

        if storage_name in self._existing_storage_lookup:
            # storage name already exists in SG
            self._set_info("* Storage name already exists in SG")
            return False

        if not self.STORAGE_NAME_REGEX.match(storage_name):
            # storage name is invalid
            self._set_info("* Storage name is invalid. ")

        # get the values once for efficiency
        linux_path = self.linux_path
        mac_path = self.mac_path
        windows_path = self.windows_path

        if not linux_path and not mac_path and not windows_path:
            # no paths defined
            self._set_info("* Must define at least one storage path.")
            return False

        # ---- ensure any defined paths are absolute paths
        for path in [linux_path, mac_path, windows_path]:
            if not os.path.isabs(path):
                self._set_info("* Storage paths must be absolute paths.")
                return False

        # ---- ensure a path is defined for the current os

        # current os is LINUX
        if sys.platform.startswith("linux"):
            if not linux_path:
                # current platform is linux and no linux path supplied
                self._set_info("* Storage path for the current OS is required.")
                return False

        # current os is MAC
        elif sys.platform == "darwin":
            if not mac_path:
                # current platform is mac and no mac path supplied
                self._set_info("* Storage path for the current OS is required.")
                return False

        # current os is WINDOWS
        elif sys.platform == "win32":
            if not windows_path:
                # current platform is windows and no windows path supplied
                self._set_info("* Storage path for the current OS is required.")
                return False

        # all good!
        self._set_info(None)
        return True

    def _browse_path(self, line_edit):
        """
        Browse a path and populate the supplied line edit.

        :param line_edit: The line edit to populate with the browsed path.
        """

        # create the dialog
        file_dialog = QtGui.QFileDialog(
            parent=self,
            caption="Choose Storage Root Folder"
        )
        file_dialog.setLabelText(QtGui.QFileDialog.Accept, "Select")
        file_dialog.setLabelText(QtGui.QFileDialog.Reject, "Cancel")
        file_dialog.setFileMode(QtGui.QFileDialog.Directory)

        # dialog options
        options = [
            QtGui.QFileDialog.DontResolveSymlinks,
            QtGui.QFileDialog.DontUseNativeDialog,
            QtGui.QFileDialog.ShowDirsOnly
        ]
        for option in options:
            file_dialog.setOption(option)

        if not file_dialog.exec_():
            return

        path = file_dialog.selectedFiles()[0]
        line_edit.set_text(path)

        # run the validation
        self._validation_check()

    def _set_info(self, message):
        """
        Sets the info label at the bottom to assist the user.

        :param message: The message to display.
        """
        if message:
            self.ui.info.show()
            self.ui.info.setText(message)
        else:
            self.ui.info.hide()

    def _validation_check(self):
        """
        Enables/disables the accept button if the dialog's contents are valid.
        """

        if not self.is_valid():
            self._accept_button.setEnabled(True)
        else:
            self._accept_button.setEnabled(False)

    def _create_storage(self):
        """
        Create the storage in SG.
        """

        # we assume that everything is valid at this point

        self._overlay.start_spin()
        self.ui.button_box.hide()

        data = {
            "code": self.storage_name,
            "mac_path": self.mac_path,
            "windows_path": self.windows_path,
            "linux_path": self.linux_path,
        }

        try:
            self._created_storage = self._sg_connection.create(
                "LocalStorage", data)
        except Exception:
            log.error("There was a problem creating storage: %s" % (data,))
            log.error("Traceback: %s" % (traceback.format_exc()))
            self._set_info("* Unable to create storage! See log for details.")
            self.ui.button_box.show()
            self._overlay.hide()
        else:
            self.close()
