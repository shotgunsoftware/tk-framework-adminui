# Copyright (c) 2018 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from sgtk.platform.qt import QtGui

from .base_page import BasePage


class StorageMapPage(BasePage):
    """
    Page to map the required roots for the selected config with SG local
    storages.
    """

    _HELP_URL = BasePage._HELP_URL + "#Setting%20up%20a%20storage"

    def __init__(self, parent=None):
        super(StorageMapPage, self).__init__(parent)

        self._map_widgets = []

    def setup_ui(self, page_id):
        BasePage.setup_ui(self, page_id)

        # TODO: clean up if back button was used?

    def add_mapping(self, root_name, root_info):
        """Add a new storage mapping widget to the list."""

        

    def validatePage(self):

        # TODO: valid if all roots are mapped to created SG storages
