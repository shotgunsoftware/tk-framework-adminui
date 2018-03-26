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
    """
    A simple dialog to prompt the user for a storage name. Includes validation.
    """

    # a regex that defines valid storage name
    STORAGE_NAME_REGEX = re.compile("^[\w\d]+$")

    def __init__(self, existing_storage_names, parent=None):
        """Initialize the create dialog.

        :param existing_storage_names: A list of storage names that already
            exist either in SG or pre-created by the map widget.
        :param parent: The dialog parent
        """

        super(CreateStorageDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Popup)

        self._existing_storage_names = existing_storage_names
        self._new_storage_name = None

        # set up the UI
        self.ui = create_storage_dialog.Ui_CreateStorageDialog()
        self.ui.setupUi(self)

        # keep a handle on the button. we can disable it until a valid name is
        # input.
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

    def _validation_check(self):
        """Returns ``True`` if the input is valid, ``False`` otherwise."""

        # get the value once for efficiency
        storage_name = str(self.ui.storage_name.text())

        if not storage_name:
            # no storage name defined
            return self._set_valid(
                False, "* Storage name is required.")

        # case insensitive check against existing storage names. we do this
        # separately from the case sensitive check in order to provide the user
        # with more info and prevent confusion when they go looking in SG for a
        # Foobar storage when it's foobar that's the one that exists. FYI, SG
        # itself does not allow both Foobar and foobar storages.
        lc_existing_storage_names = [
            s.lower() for s in self._existing_storage_names]
        if storage_name.lower() in lc_existing_storage_names:
            index = lc_existing_storage_names.index(storage_name.lower())
            return self._set_valid(
                False,
                "* Storage name already exists: '%s'" %
                (self._existing_storage_names[index],)
            )

        if not self.STORAGE_NAME_REGEX.match(storage_name):
            # storage name is invalid
            return self._set_valid(
                False, "* Storage name has invalid character.")

        # all good!
        return self._set_valid(True)

    def _set_valid(self, is_valid, message=None):
        """
        Sets the info label at the bottom to assist the user.

        Returns the supplied is_valid boolean for convenience.
        """

        # update the info message
        if message:
            self.ui.info.setText(message)
            self.ui.info.show()
        else:
            self.ui.info.setText("")
            self.ui.info.hide()

        # enable/disable the accept button
        if is_valid:
            self._accept_button.setEnabled(True)
        else:
            self._accept_button.setEnabled(False)

        return is_valid

    def accept(self):
        """Store the new storage name for access by the calling code."""
        self._new_storage_name = str(self.ui.storage_name.text())
        super(CreateStorageDialog, self).accept()
