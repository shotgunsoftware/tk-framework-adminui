# Copyright (c) 2018 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import re

from sgtk.platform.qt import QtGui
from sgtk.platform.qt import QtCore

from ..ui import create_storage_dialog


class CreateStorageDialog(QtGui.QDialog):
    """A dialog that allows a user to create a new local storage in SG."""

    # a regex that defines valid storage name
    STORAGE_NAME_REGEX = re.compile("^[\w\d]+$")

    def __init__(self, existing_storage_names, parent=None):
        """Initialize the create dialog."""

        super(CreateStorageDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Popup)

        self._existing_storage_names = existing_storage_names
        self._new_storage_name = None

        # set up the UI
        self.ui = create_storage_dialog.Ui_CreateStorageDialog()
        self.ui.setupUi(self)

        # keep a handle on the buttons
        self._accept_button = self.ui.button_box.button(
            QtGui.QDialogButtonBox.Ok)

        # connect the validation check method to the storage name input box
        self.ui.storage_name.textChanged.connect(self._validation_check)

        # do an initial check for valid values
        self._validation_check()

        self.ui.storage_name.setFocus()

    @property
    def new_storage_name(self):
        """The new storage name if the dialog was successful."""
        return self._new_storage_name

    @property
    def storage_name(self):
        """The name of the storage to create."""
        return str(self.ui.storage_name.text())

    def _validation_check(self):
        """Returns ``True`` if the input is valid, ``False`` otherwise."""

        # get the values once for efficiency
        storage_name = self.storage_name

        if not storage_name:
            # no storage name defined
            return self._set_valid(
                False, "* Storage name is required.")

        if storage_name in self._existing_storage_names:
            # storage name already exists in SG
            return self._set_valid(
                False, "* Storage name already exists.")

        if not self.STORAGE_NAME_REGEX.match(storage_name):
            # storage name is invalid
            return self._set_valid(
                False, "* Storage name is invalid (alphanumeric and '_' only).")

        # all good!
        return self._set_valid(True)

    def _set_valid(self, is_valid, message=None):
        """
        Sets the info label at the bottom to assist the user.

        :param message: The message to display.
        """
        if message:
            self.ui.info.setText(message)
        else:
            self.ui.info.setText("")

        if is_valid:
            self._accept_button.setEnabled(True)
        else:
            self._accept_button.setEnabled(False)

        return is_valid

    def accept(self):
        """
        Create the storage in SG.
        """

        self._new_storage_name = self.storage_name
        super(CreateStorageDialog, self).accept()
