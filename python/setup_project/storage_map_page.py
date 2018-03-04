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
import sys

import sgtk
from sgtk.platform.qt import QtCore
from sgtk.platform.qt import QtGui
from sgtk.util.filesystem import ensure_folder_exists
from sgtk.util.storage_roots import StorageRoots

from .base_page import BasePage
from .storage_map_widget import StorageMapWidget

# use sg utils settings to remember previous storage mappings
settings = sgtk.platform.import_framework(
    "tk-framework-shotgunutils",
    "settings"
)


class StorageMapContainerWidget(QtGui.QWidget):
    """
    This class defines the widget contained within the scroll area where the
    mapping widgets will be added.

    The primary purpose of this class is to add a layout to the widget so
    that the mapping widgets can be added to it.
    """

    def __init__(self, parent=None):
        super(StorageMapContainerWidget, self).__init__(parent)

        layout = QtGui.QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        self.setLayout(layout)


class StorageModel(QtGui.QStandardItemModel):

    CHOOSE_STORAGE_ITEM_TEXT = "Choose..."
    CREATE_STORAGE_ITEM_TEXT = "+ New"

    STORAGE_DATA_ROLE = QtCore.Qt.UserRole + 7

    def __init__(self, parent):

        super(StorageModel, self).__init__(parent)
        self._storages = []

        sg_connection = sgtk.platform.current_engine().shotgun
        storages = sg_connection.find(
            "LocalStorage",
            filters=[],
            fields=["code", "id", "linux_path", "mac_path", "windows_path"],
            order=[{"field_name": "code", "direction":"asc"}]
        )

        choose_item = QtGui.QStandardItem(self.CHOOSE_STORAGE_ITEM_TEXT)
        self.appendRow(choose_item)

        create_item = QtGui.QStandardItem(self.CREATE_STORAGE_ITEM_TEXT)
        self.appendRow(create_item)

        for storage in storages:
            self.add_storage(storage)

    @property
    def storages(self):
        """All storage dictionaries stored by the model"""
        return self._storages

    def add_storage(self, storage):

        self._storages.append(storage)

        storage_name = storage["code"]
        storage_item = QtGui.QStandardItem(storage_name)
        storage_item.setData(storage, self.STORAGE_DATA_ROLE)

        # insert the storage at the end of the list, before the "create" item
        self.insertRow(self.rowCount() - 1, storage_item)

    def update_storage(self, storage_name, storage_data):

        # find the storage with the supplied name and update its data
        for row in range(0, self.rowCount()):
            item = self.item(row, 0)
            if item.text() == storage_name:
                item.setData(storage_data, self.STORAGE_DATA_ROLE)


class StorageMapPage(BasePage):
    """
    Page to map the required roots for the selected config with SG local
    storages.
    """

    _HELP_URL = BasePage._HELP_URL + "#Setting%20up%20a%20storage"

    # the key used in global settings to store historical storage mappings
    HISTORICAL_MAPPING_KEY = "project_setup_storage_mappings"

    def __init__(self, parent=None):
        super(StorageMapPage, self).__init__(parent)

        self._uri = None
        self._map_widgets = []
        self._required_roots = []

        self._settings = settings.UserSettings(sgtk.platform.current_bundle())
        self._historical_mappings = self._settings.retrieve(
            self.HISTORICAL_MAPPING_KEY, {})

    def setup_ui(self, page_id, error_field=None):
        super(StorageMapPage, self).setup_ui(page_id, error_field=error_field)

        # create one storage model to be shard by all widgets. that way, if one
        # creates a new storage, all will share
        self._storages_model = StorageModel(self)

    def initializePage(self):
        wiz = self.wizard()
        ui = wiz.ui
        layout = ui.storage_map_area_widget.layout()

        num_roots = len(self._required_roots)
        count = 1

        for (root_name, root_info) in self._required_roots:

            map_widget = StorageMapWidget(self._storages_model)
            map_widget.root_name = root_name
            map_widget.root_info = root_info
            map_widget.set_count(count, num_roots)

            # set the best guess for this mapping based on saved historical
            # mappings (this could be None)
            map_widget.best_guess = self._historical_mappings.get(root_name)

            # add the map widget to the ui
            layout.addWidget(map_widget)

            # get alerts when a storage is saved
            map_widget.storage_saved.connect(self._on_storage_saved)

            # keep a reference to the map widget
            self._map_widgets.append(map_widget)

            # tell the widget to make an educated guess as to which storage
            # should be used for the supplied root name/info.
            map_widget.guess_storage()

            count += 1

        layout.addStretch()

        # clear out any errors
        ui.storage_errors.setText("")

    def add_mapping(self, root_name, root_info):
        """Add a new storage mapping widget to the list."""
        self._required_roots.append((root_name, root_info))

    def clear_roots(self):
        """Clear any required roots already set for the page."""

        wiz = self.wizard()
        ui = wiz.ui
        layout = ui.storage_map_area_widget.layout()

        self._required_roots = []
        self._map_widgets = []
        for index in range(0, layout.count()):
            layout_item = layout.takeAt(0)
            widget = None
            if layout_item:
                widget = layout_item.widget()
            layout.removeItem(layout_item)
            if widget and isinstance(widget, StorageMapWidget):
                widget.deleteLater()

    def set_config_uri(self, uri):
        """Set the config URI.

        This will be set for the wizard once the storages have all been mapped
        and validated.
        """
        self._uri = uri

    def validatePage(self):

        wiz = self.wizard()
        ui = wiz.ui

        # clear any errors
        ui.storage_errors.setText("")

        # get the path key for the current os
        if sys.platform.startswith("linux"):
            current_os_key = "linux_path"
        elif sys.platform == "darwin":
            current_os_key = "mac_path"
        elif sys.platform == "win32":
            current_os_key = "windows_path"
        else:
            ui.storage_errors.setText("The current OS is unrecognized.")
            return False

        invalid_widgets = []
        not_on_disk_widgets = []

        first_invalid_widget = None

        # see if each of the mappings is valid
        for map_widget in self._map_widgets:

            if not map_widget.mapping_is_valid():
                # something is wrong with this widget's mapping
                invalid_widgets.append(map_widget)
                if first_invalid_widget is None:
                    first_invalid_widget = map_widget

            storage = map_widget.local_storage or {}
            current_os_path = storage.get(current_os_key)

            if current_os_path and not os.path.exists(current_os_path):
                # the current os path for this widget doesn't exist on disk
                not_on_disk_widgets.append(map_widget)

        if invalid_widgets:
            # tell the user which roots don't have valid mappings
            root_names = [w.root_name for w in invalid_widgets]
            ui.storage_errors.setText(
                "The mappings for these roots are invalid: <b>%s</b>" %
                (", ".join(root_names),)
            )
            if first_invalid_widget:
                ui.storage_map_area.ensureWidgetVisible(first_invalid_widget)
            return False

        if not_on_disk_widgets:

            # try to create the folders for current OS if they don't exist
            failed_to_create = []
            for widget in not_on_disk_widgets:

                storage = widget.local_storage

                # try to create any missing paths for the current OS
                try:
                    folder = storage[current_os_key]
                    ensure_folder_exists(folder)
                except Exception:
                    failed_to_create.append(storage["code"])

            if failed_to_create:
                # some folders weren't created. let the user know.
                ui.storage_errors.setText(
                    "Unable to create folders on disk for these storages: %s."
                    "Please check to make sure you have permission to create "
                    "these folders." % (", ".join(failed_to_create),)
                )

        # TODO: go through the old page logic carefully. what is missing?

        # ---- now we've mapped the roots, and they're all valid, we need to
        #      create a StorageRoots instance and set it on the project params.

        roots_metadata = {}
        for map_widget in self._map_widgets:

            root_name = map_widget.root_name
            root_info = map_widget.root_info
            storage_data = map_widget.local_storage

            # populate the data defined prior to mapping
            roots_metadata[root_name] = root_info

            # update the mapped shotgun data
            roots_metadata[root_name]["shotgun_storage_id"] = storage_data["id"]
            roots_metadata[root_name]["linux_path"] = str(
                storage_data["linux_path"])
            roots_metadata[root_name]["mac_path"] = str(
                storage_data["mac_path"])
            roots_metadata[root_name]["windows_path"] = str(
                storage_data["windows_path"])

            # store the fact that we've mapped this root name with this
            # storage name. we can use this information to make better
            # guesses next time this user is mapping storages.
            self._historical_mappings[root_name] = storage_data["code"]
            self._settings.store(
                self.HISTORICAL_MAPPING_KEY,
                self._historical_mappings
            )

        storage_roots = StorageRoots.from_metadata(roots_metadata)
        wiz.core_wizard.set_storage_roots(self._uri, storage_roots)

        # if we made it here, then we should be valid.
        # Try to set the config
        try:
            wiz.core_wizard.set_config_uri(self._uri)
        except Exception, e:
            error = (
                "Unknown error when setting the configuration uri:\n%s" %
                str(e)
            )
            ui.storage_errors.setText(error)
            return False

        return True

    def _on_storage_saved(self):

        for map_widget in self._map_widgets:
            map_widget.refresh_display()
