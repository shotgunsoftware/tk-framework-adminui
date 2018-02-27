# Copyright (c) 2018 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
from sgtk.platform.qt import QtGui

log = sgtk.platform.get_logger(__name__)

from ..ui import storage_map_widget


class StorageMapWidget(QtGui.QWidget):
    """Allows mapping config storage roots to a SG local storage"""

    def __init__(self, parent=None):
        """
        Initialize the widget.

        :param parent: The parent object for this widget
        """

        super(StorageMapWidget, self).__init__(parent)

        # set up the UI
        self.ui = storage_map_widget.Ui_StorageMapWidget()
        self.ui.setupUi(self)

        # TODO: populate storages with all existing storages
        # TODO: use SG model with delegate to get updates as new storages are created

    @property
    def root_name(self):
        """The root name being mapped to a local storage"""
        return self.root_name.text()

    @root_name.setter
    def root_name(self, name):
        """Set the root name to be mapped"""
        self.ui.root_name.setText(name)

        # TODO: check settings to see if this root has been mapped before
        # TODO: look for one matching this name

    @property
    def root_description(self):
        """The description or the root being mapped."""
        return self.root_description.text()

    @root_description.setter
    def root_description(self, description):
        """Set the root description."""
        self.ui.root_description.setText(description)

    @property
    def local_storage(self):
        """
        Returns the local storage chosen by the user or None if no storage
        has been selected.
        """
        return None
        # TODO: extract the storage dict from the current item in the model

    @local_storage.setter
    def local_storage(self, storage_name):
        """
        Set the mapped local storage with the supplied name.

        :param storage_name: The name of the storage to map to the root.
        """
        pass
        #TODO: find the corresponding storage in the model, make it current

