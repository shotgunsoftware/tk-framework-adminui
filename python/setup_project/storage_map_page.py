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
import traceback

import sgtk
from sgtk.platform.qt import QtCore
from sgtk.platform.qt import QtGui
from sgtk.util.filesystem import ensure_folder_exists
from sgtk.util import ShotgunPath

from .base_page import BasePage
from .storage_map_widget import StorageMapWidget

logger = sgtk.platform.get_logger(__name__)

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
        layout.setSpacing(6)
        layout.setContentsMargins(6, 6, 6, 6)

        self.setLayout(layout)


class StorageModel(QtGui.QStandardItemModel):
    """
    A simple modle to store all available storages.

    Some storages may exists in SG, others may be created/edited/saved via the
    storage map widgets. The model is shared by all map widgets to keep them
    in sync as storages are created/updated.
    """

    # non-storage item text
    CHOOSE_STORAGE_ITEM_TEXT = "Choose..."
    CREATE_STORAGE_ITEM_TEXT = "+ New"

    # data role for the storages in the model's items
    STORAGE_DATA_ROLE = QtCore.Qt.UserRole + 7

    def __init__(self, parent):
        """Initialize the model."""

        super(StorageModel, self).__init__(parent)

        # query all existing SG storages to include in the model
        logger.debug("Querying all SG LocalStorage entries...")
        sg_connection = sgtk.platform.current_engine().shotgun
        storages = sg_connection.find(
            "LocalStorage",
            filters=[],
            fields=["code", "id", "linux_path", "mac_path", "windows_path"],
            order=[{"field_name": "code", "direction":"asc"}]
        )
        logger.debug(
            "Found %s LocalStorages: %s" %
            (len(storages), storages)
        )

        # add the "choose" item
        choose_item = QtGui.QStandardItem(self.CHOOSE_STORAGE_ITEM_TEXT)
        self.appendRow(choose_item)

        # add the "create" item
        create_item = QtGui.QStandardItem(self.CREATE_STORAGE_ITEM_TEXT)
        self.appendRow(create_item)

        # add existing storages. they will be inserted before the "create" item
        for storage in storages:
            self.add_storage(storage)

    @property
    def storages(self):
        """All storage dictionaries stored by the model"""
        storages = []

        # iterate through the model and build a list of all storages
        for row in range(0, self.rowCount()):
            item = self.item(row, 0)
            storage_data = item.data(self.STORAGE_DATA_ROLE)

            # not all items represent storages
            if storage_data:
                storages.append(storage_data)

        return storages

    def add_storage(self, storage):
        """Add a new item to the model for the supplied storage dictionary.

        :param dict storage: A standard SG LocalStorage entity dict.
        """

        logger.debug("Adding storage to the model: %s" % (storage,))

        # create the item
        storage_name = storage["code"]
        storage_item = QtGui.QStandardItem(storage_name)
        storage_item.setData(storage, self.STORAGE_DATA_ROLE)

        # insert the storage at the end of the list, before the "create" item
        self.insertRow(self.rowCount() - 1, storage_item)

    def update_storage(self, storage_name, storage_data):
        """Update the supplied storage name with the supplied data."""

        logger.debug("Updating storage %s: %s" % (storage_name, storage_data))

        # find the storage with the supplied name and update its data
        for row in range(0, self.rowCount()):
            item = self.item(row, 0)
            if item.text() == storage_name:
                item.setData(storage_data, self.STORAGE_DATA_ROLE)


class StorageMapPage(BasePage):
    """
    Map the required roots for the selected config with SG local storages

    A list of mapping widgets is displayed, one for each root required by the
    configuration. The user must create a valid mapping for each required root
    before the page will validate.
    """

    _HELP_URL = BasePage._HELP_URL + "#Setting%20up%20a%20storage"

    # the key used in global settings to store historical storage mappings
    HISTORICAL_MAPPING_KEY = "project_setup_storage_mappings"

    def __init__(self, parent=None):
        """Initialize the storage map page."""

        super(StorageMapPage, self).__init__(parent)

        # internal data stored for the page
        self._uri = None
        self._map_widgets = []
        self._required_roots = []

        # retrieve a historical mapping of root names to SG storages. these will
        # be used to make a best guess if it's not obvious what the mappings
        # should be.
        logger.debug("Querying historical storage mappings...")
        self._settings = settings.UserSettings(sgtk.platform.current_bundle())
        self._historical_mappings = self._settings.retrieve(
            self.HISTORICAL_MAPPING_KEY, {})
        logger.debug("Historical mappings: %s" % (self._historical_mappings,))

    def setup_ui(self, page_id, error_field=None):
        """Set up the UI for this page."""

        super(StorageMapPage, self).setup_ui(page_id, error_field=error_field)

        # create one storage model to be shard by all widgets.
        self._storages_model = StorageModel(self)

    def initializePage(self):
        """Initialize the wizard page to display its contents properly."""

        logger.debug("Initialize storage map page...")

        # the wizard instance and its UI
        wiz = self.wizard()
        ui = wiz.ui

        # we'll add the storage mapping widgets to the area widget's layout
        layout = ui.storage_map_area_widget.layout()

        # keep a count so the user can see which one, and how many they need to
        # edit.
        num_roots = len(self._required_roots)
        count = 1

        # iterate over each required root and create a mapping widget
        for (root_name, root_info) in self._required_roots:

            # create the widget and set all the values
            map_widget = StorageMapWidget(self._storages_model, parent=self)
            map_widget.root_name = root_name
            map_widget.root_info = root_info
            map_widget.set_count(count, num_roots)

            # set the best guess for this mapping based on saved historical
            # mappings (this could be None)
            map_widget.best_guess = self._historical_mappings.get(root_name)

            # add the map widget to the ui
            layout.addWidget(map_widget)

            # get alerts when a storage is saved for this mapping
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
        """Add a new storage mapping widget to the list.

        This should be called before the page is initialized.
        """
        logger.debug(
            "Adding root '%s' to be mapped: %s" %
            (root_name, root_info)
        )
        self._required_roots.append((root_name, root_info))

    def clear_roots(self):
        """Clear any required roots already set for the page.

        This is typically called when the wizard's "back" button is used. The
        roots are cleared so they can be rebuilt with potentially a different
        configuration.
        """

        logger.debug("Clearing all storage roots from storage mapping page!")

        # the wizard instance and its UI
        wiz = self.wizard()
        ui = wiz.ui

        # the scroll area widget where the mapping widgets live
        layout = ui.storage_map_area_widget.layout()

        # reset the internal data
        self._required_roots = []
        self._map_widgets = []

        # iterate over all layout items and remove them. if the item is a
        # storage map widget, delete it.
        for index in range(0, layout.count()):
            layout_item = layout.takeAt(0)
            widget = None
            if layout_item:
                widget = layout_item.widget()
            layout.removeItem(layout_item)
            if widget and isinstance(widget, StorageMapWidget):
                # this is required to fully remove the widget from the parent's
                # display. without this, the widget will still show up and be
                # interactive in the scroll area for some reason.
                widget.deleteLater()

    def set_config_uri(self, uri):
        """Set the config URI."""
        logger.debug("Setting config uri: %s" % (uri,))
        self._uri = uri

    def validatePage(self):
        """The 'next' button was pushed. See if the mappings are valid."""

        logger.debug("Validating the storage mappings page...")

        # the wizard instance and its UI
        wiz = self.wizard()
        ui = wiz.ui

        # clear any errors
        ui.storage_errors.setText("")

        # get the path key for the current os
        current_os_key = ShotgunPath.get_shotgun_storage_key()

        logger.debug("Current OS storage path key: %s" % (current_os_key,))

        # temp lists of widgets that need attention
        invalid_widgets = []
        not_on_disk_widgets = []

        # keep track of the first invalid widget so we can ensure it is visible
        # to the user in the list.
        first_invalid_widget = None

        logger.debug("Checking all map widgets...")

        # see if each of the mappings is valid
        for map_widget in self._map_widgets:

            logger.debug(
                "Checking mapping for root: %s" %
                (map_widget.root_name,)
            )

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
            logger.debug("Invalid mappings for roots: %s" % (root_names))
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
                folder = storage[current_os_key]

                logger.debug(
                    "Ensuring folder on disk for storage '%s': %s" %
                    (storage["code"], folder)
                )

                # try to create the missing path for the current OS. this will
                # help ensure the storage specified in SG is valid and the
                # project data can be written to this root.
                try:
                    ensure_folder_exists(folder)
                except Exception:
                    logger.error("Failed to create folder: %s" % (folder,))
                    logger.error(traceback.format_exc())
                    failed_to_create.append(storage["code"])

            if failed_to_create:
                # some folders weren't created. let the user know.
                ui.storage_errors.setText(
                    "Unable to create folders on disk for these storages: %s."
                    "Please check to make sure you have permission to create "
                    "these folders. See the tk-desktop log for more info." %
                    (", ".join(failed_to_create),)
                )

        # ---- now we've mapped the roots, and they're all valid, we need to
        #      update the root information on the core wizard

        for map_widget in self._map_widgets:

            root_name = map_widget.root_name
            root_info = map_widget.root_info
            storage_data = map_widget.local_storage

            # populate the data defined prior to mapping
            updated_storage_data = root_info

            # update the mapped shotgun data
            updated_storage_data["shotgun_storage_id"] = storage_data["id"]
            updated_storage_data["linux_path"] = str(storage_data["linux_path"])
            updated_storage_data["mac_path"] = str(storage_data["mac_path"])
            updated_storage_data["windows_path"] = str(
                storage_data["windows_path"])

            # now update the core wizard's root info
            wiz.core_wizard.update_storage_root(
                self._uri,
                root_name,
                updated_storage_data
            )

            # store the fact that we've mapped this root name with this
            # storage name. we can use this information to make better
            # guesses next time this user is mapping storages.
            self._historical_mappings[root_name] = storage_data["code"]
            self._settings.store(
                self.HISTORICAL_MAPPING_KEY,
                self._historical_mappings
            )

        logger.debug("Storage mappings are valid.")

        # if we made it here, then we should be valid.
        try:
            wiz.core_wizard.set_config_uri(self._uri)
        except Exception as e:
            error = (
                "Unknown error when setting the configuration uri:\n%s" %
                str(e)
            )
            logger.error(error)
            logger.error(traceback.print_exc())
            ui.storage_errors.setText(error)
            return False

        return True

    def _on_storage_saved(self):
        """A slot used to ensure all widget displays are updated."""

        logger.debug("Storage saved, ensuring other widget displays updated...")
        for map_widget in self._map_widgets:
            map_widget.refresh_display()
