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
import traceback

import sgtk
from sgtk.platform.qt import QtCore
from sgtk.platform.qt import QtGui
from sgtk.util import ShotgunPath

from .create_storage_dialog import CreateStorageDialog
from ..ui import storage_map_widget

logger = sgtk.platform.get_logger(__name__)


class StorageMapWidget(QtGui.QWidget):
    """Allows mapping config storage roots to a SG local storage"""

    # emitted when a storage was saved or updated (indicating it was changed in
    # some way). useful for to alert other map widgets that may be displaying
    # the same storage
    storage_saved = QtCore.Signal()

    def __init__(self, storage_model, parent=None):
        """
        Initialize the widget.

        :param storage_model: The SG model for available local storages.
        :param parent: The parent object for this widget
        """

        super(StorageMapWidget, self).__init__(parent)

        # internal state values
        self._storage_model = storage_model
        self._root_name = None
        self._root_info = None
        self._best_guess = None

        # hold on to any edited text for the selected storage
        self._linux_path_edit = {}
        self._mac_path_edit = {}
        self._windows_path_edit = {}

        # set up the UI
        self.ui = storage_map_widget.Ui_StorageMapWidget()
        self.ui.setupUi(self)

        # set the combo box to use the supplied storage model
        self.ui.storage_select_combo.setModel(self._storage_model)

        # update the display when a storage is selected in the combo box
        self.ui.storage_select_combo.activated.connect(
            lambda a: self.refresh_display())

        # keep a handle on any edited text
        self.ui.linux_path_edit.textChanged.connect(
            lambda p: self._on_path_changed(p, self._linux_path_edit))
        self.ui.mac_path_edit.textChanged.connect(
            lambda p: self._on_path_changed(p, self._mac_path_edit))
        self.ui.windows_path_edit.textChanged.connect(
            lambda p: self._on_path_changed(p, self._windows_path_edit))

        # connect the file browse buttons
        self.ui.linux_path_browse.clicked.connect(
            lambda: self._browse_path(self.ui.linux_path_edit))
        self.ui.mac_path_browse.clicked.connect(
            lambda: self._browse_path(self.ui.mac_path_edit))
        self.ui.windows_path_browse.clicked.connect(
            lambda: self._browse_path(self.ui.windows_path_edit))

        # connect the save button
        self.ui.save_storage_btn.clicked.connect(self._on_storage_save_clicked)

    @property
    def best_guess(self):
        """The name of the best guess SG storage to associate with this root."""
        return self._best_guess

    @best_guess.setter
    def best_guess(self, storage_name):
        """Set the 'best guess' SG storage name to associate with this root."""
        self._best_guess = storage_name

    @property
    def root_name(self):
        """The root name being mapped to a SG local storage"""
        return self._root_name

    @root_name.setter
    def root_name(self, name):
        """Set the root name to be mapped"""
        self._root_name = name
        self.ui.root_name.setText("<b>%s</b>" % (name,))

    @property
    def root_info(self):
        """The info for the root being mapped."""
        return self._root_info

    @root_info.setter
    def root_info(self, info):
        """
        Set the root info.

        The ``info`` dict is a standard dict as defined in a config's roots.yml.
        """
        self._root_info = info
        self.ui.root_description.setText(info.get("description"))

    @property
    def local_storage(self):
        """
        Returns the local storage chosen by the user or None if no storage
        has been selected. This will be a standard SG LocalStorage dict.

        Will return ``None`` if no local storage selected.
        """
        current_index = self.ui.storage_select_combo.currentIndex()

        # this will return None if not a storage item
        return self.ui.storage_select_combo.itemData(
            current_index, self._storage_model.STORAGE_DATA_ROLE)

    @local_storage.setter
    def local_storage(self, storage_name):
        """
        Set the mapped local storage with the supplied name.

        :param storage_name: The name of the storage to map to the root.
        """
        # find the storage name in the combo box and set that item
        match_index = self.ui.storage_select_combo.findText(storage_name)
        if match_index > -1:
            self.ui.storage_select_combo.setCurrentIndex(match_index)
            self.refresh_display()

    def mapping_is_valid(self):
        """Checks that the mapped storage is valid and saved in SG."""

        # ensure a local storage is set
        local_storage = self.local_storage

        # hide this by default
        self.ui.save_storage_btn.hide()

        # root is not mapped to a local storage
        if not local_storage:
            self.ui.storage_info.setText("* No storage selected")
            return False

        # get these once to make the code below a bit more readable
        linux_path = local_storage.get("linux_path")
        mac_path = local_storage.get("mac_path")
        windows_path = local_storage.get("windows_path")

        # get the current os path and any edited path for the current OS.
        if sys.platform.startswith("linux") and not linux_path:
            current_os_path = linux_path
            edited_current_os_path_lookup = self._linux_path_edit
        elif sys.platform == "darwin":
            current_os_path = mac_path
            edited_current_os_path_lookup = self._mac_path_edit
        elif sys.platform == "win32":
            current_os_path = windows_path
            edited_current_os_path_lookup = self._windows_path_edit
        else:
            raise Exception("Unrecognized platform: %s" % (sys.platform,))

        # no path for the current os
        if not current_os_path:

            # the name of the selected local storage
            storage_name = local_storage["code"]

            # if haven't edited anything, need to edit + save
            edited_current_os_path = edited_current_os_path_lookup.get(
                storage_name)

            if edited_current_os_path:
                # user has manually edited the path for the current OS

                # current os path must be absolute path
                if not os.path.isabs(edited_current_os_path):
                    self.ui.storage_info.setText(
                        "* The current OS storage path must be absolute.")
                    return False

                # they've edited but haven't saved (otherwise the
                # current_os_path would not be None. show the save button to
                # indicate they should save.
                self.ui.save_storage_btn.show()
                self.ui.storage_info.setText(
                    "* Please save the current OS path before proceeding.")
                return False

            else:
                self.ui.storage_info.setText(
                    "* A storage path is required for the current OS.")
                return False

        if not local_storage.get("id"):
            # if there's no id, the storage hasn't been saved. show the save
            # button to indicate they should save
            self.ui.save_storage_btn.show()
            self.ui.storage_info.setText(
                "* Please save this storage to continue.")
            return False

        # if we're here, everything is valid!
        return True

    def refresh_display(self):
        """Update the path display for the current selected storage."""

        # selected storage info
        storage_name = self.ui.storage_select_combo.currentText()
        storage_data = self.local_storage

        # clear everything out to its default state
        self._set_default_edit_state()

        if not storage_data:
            # no storage data to process.

            if storage_name == self._storage_model.CREATE_STORAGE_ITEM_TEXT:
                # user wants to create a new storage
                self._create_new_storage()

            # nothing left to do. if they create a new storage above, this
            # method will be called again.
            return

        # --- if here, then a storage name was selected

        # show the path section
        self.ui.path_frame.show()

        # get the paths once to make the code below a bit more readable
        linux_path = storage_data.get("linux_path")
        mac_path = storage_data.get("mac_path")
        windows_path = storage_data.get("windows_path")

        # get any edited text for each OS
        edited_linux_path = self._linux_path_edit.get(storage_name, "")
        edited_mac_path = self._mac_path_edit.get(storage_name, "")
        edited_windows_path = self._windows_path_edit.get(storage_name, "")

        # we have storage data. show the labels
        self.ui.linux_path_lbl.show()
        self.ui.mac_path_lbl.show()
        self.ui.windows_path_lbl.show()

        if storage_data.get("id"):
            # this storage exists in SG

            # show the path display widgets
            self.ui.linux_path.show()
            self.ui.mac_path.show()
            self.ui.windows_path.show()

            # set the paths
            self.ui.linux_path.setText(linux_path)
            self.ui.mac_path.setText(mac_path)
            self.ui.windows_path.setText(windows_path)

            if sys.platform.startswith("linux") and not linux_path:
                # storage exists in SG, but no path defined for current OS.
                # make it possible to edit the current OS path.
                self.ui.linux_path.hide()
                self.ui.linux_lock.hide()
                self.ui.linux_path_edit.show()
                self.ui.linux_path_browse.show()
                self.ui.linux_path_edit.setText(edited_linux_path)
                self.ui.linux_path_edit.setFocus()
                self.ui.mac_lock.show()
                self.ui.windows_lock.show()
            elif sys.platform == "darwin" and not mac_path:
                # storage exists in SG, but no path defined for current OS
                # make it possible to edit the current OS path.
                self.ui.mac_path.hide()
                self.ui.mac_lock.hide()
                self.ui.mac_path_edit.show()
                self.ui.mac_path_browse.show()
                self.ui.mac_path_edit.setText(edited_mac_path)
                self.ui.mac_path_edit.setFocus()
                self.ui.linux_lock.show()
                self.ui.windows_lock.show()
            elif sys.platform == "win32" and not mac_path:
                # storage exists in SG, but no path defined for current OS
                # make it possible to edit the current OS path.
                self.ui.windows_path.hide()
                self.ui.windows_lock.hide()
                self.ui.windows_path_edit.show()
                self.ui.windows_path_browse.show()
                self.ui.windows_path_edit.setText(edited_windows_path)
                self.ui.windows_path_edit.setFocus()
                self.ui.linux_lock.show()
                self.ui.mac_lock.show()

        else:
            # this is a new storage that hasn't been created in SG yet.

            # show the path edit widgets
            self.ui.linux_path_edit.show()
            self.ui.mac_path_edit.show()
            self.ui.windows_path_edit.show()

            # show the browse button for the current os
            if sys.platform.startswith("linux"):
                self.ui.linux_path_edit.setFocus()
                self.ui.linux_path_browse.show()
            elif sys.platform == "darwin" and not mac_path:
                self.ui.mac_path_edit.setFocus()
                self.ui.mac_path_browse.show()
            elif sys.platform == "win32" and not mac_path:
                self.ui.windows_path_edit.setFocus()
                self.ui.windows_path_browse.show()

            # set the path values if they've been edited before
            self.ui.linux_path_edit.setText(edited_linux_path)
            self.ui.mac_path_edit.setText(edited_mac_path)
            self.ui.windows_path_edit.setText(edited_windows_path)

        # run this to populate the info label if there are any concerns with
        # the current input value(s)
        self.mapping_is_valid()

    def guess_storage(self):
        """
        Attempt to guess the most appropriate storage to use for the root.
        """

        # build lookups by name and id
        storage_by_id = {}
        storage_by_name = {}

        # the storages may change as new storages are added manually so we do
        # this each time this is called
        storages = self._storage_model.storages
        for storage in storages:
            storage_name = storage["code"]
            storage_id = storage["id"]
            storage_by_id[storage_id] = storage
            storage_by_name[storage_name] = storage

        # see if a shotgun storage id is defined in the root info.
        root_sg_id = self.root_info.get("shotgun_id")
        if root_sg_id in storage_by_id:
            # shotgun id defined explicitly for this root. set it!
            self.local_storage = storage_by_id[root_sg_id]["code"]

        # does name match an existing storage?
        elif self.root_name in storage_by_name:
            self.local_storage = self.root_name

        # has this name been mapped before?
        elif self._best_guess and self._best_guess in storage_by_name:
            self.local_storage = self._best_guess

        # fall back to requiring the user to manually select an item
        else:
            self.local_storage = self._storage_model.CHOOSE_STORAGE_ITEM_TEXT

    def set_count(self, num, total):
        """Simply sets the text of the count label of the widget. ex (1 of 3)"""

        self.ui.count_lbl.setText("%s of %s" % (num, total))

    def _browse_path(self, line_edit):
        """Browse and set the path for the supplied edit widget."""

        # create the dialog
        folder_path = QtGui.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Choose Storage Root Folder",
            options=QtGui.QFileDialog.DontResolveSymlinks |
                    QtGui.QFileDialog.DontUseNativeDialog |
                    QtGui.QFileDialog.ShowDirsOnly
        )

        if folder_path:
            # folder was browsed, set the path in the widget.
            line_edit.setText(folder_path)

    def _create_new_storage(self):
        """Prompt the user for a new storage name."""

        # get all existing storages to provide to the dialog
        all_storages = self._storage_model.storages
        existing_storage_names = [storage["code"] for storage in all_storages]

        # propt the user for a new storage name
        create_dialog = CreateStorageDialog(
            existing_storage_names,
            parent=self
        )

        if create_dialog.exec_() == QtGui.QDialog.Accepted:
            # user entered a valid storage name. create the skeleton data and
            # add it to the storage model. the user will still have to "Save"
            # the info to SG when they're finished editing the path(s).
            new_storage_name = create_dialog.new_storage_name
            new_storage = {
                "id": None,
                "code": new_storage_name,
                "linux_path": None,
                "mac_path": None,
                "windows_path": None,
            }
            self._storage_model.add_storage(new_storage)
            self.local_storage = new_storage["code"]
        else:
            # didn't create a new storage. try to guess the best storage. this
            # will switch away from "create" back to "choose" or a storage.
            self.guess_storage()

    def _on_path_changed(self, path, edit_lookup):
        """
        Keep track of any path edits as they happen. Kepe the user informed if
        there are any concerns about the entered text.
        """

        # store the edited path in the appropriate path lookup
        storage_name = str(self.ui.storage_select_combo.currentText())
        edit_lookup[storage_name] = path

        # run the validation tell the user if there are issues
        self.mapping_is_valid()

    def _on_storage_save_clicked(self):
        """
        The user has clicked the save button.

        They want to create a new storage in SG (if no id is defined for the
        storage) or they want to update an existing storage with a path for
        the current os.
        """

        try:
            self._do_storage_update_or_save()
        except Exception:
            logger.error(traceback.format_exc())
            self.ui.storage_info.setText(
                "Error occurred trying to save storage data! "
                "See the tk-desktop log for more info."
            )

        self.storage_saved.emit()

    def _do_storage_update_or_save(self):
        """
        Handles saving or updating the edited storage being displayed by the
        widget.
        """

        # the storage info
        storage_data = self.local_storage
        storage_name = storage_data["code"]

        # a SG connect we can use to save/update
        sg = sgtk.platform.current_engine().shotgun

        if storage_data.get("id"):
            # the storage exists in SG. we just want to update the current OS
            # path as the other OS paths can't be modified.

            current_os_key = ShotgunPath.get_shotgun_storage_key()

            # get the current os key (field name in SG) and the path to update.
            # this will be the edited path we've been keeping track of
            if sys.platform.startswith("linux"):
                current_os_path = self._linux_path_edit[storage_name]
            elif sys.platform == "darwin":
                current_os_path = self._mac_path_edit[storage_name]
            elif sys.platform == "win32":
                current_os_path = self._mac_path_edit[storage_name]
            else:
                raise Exception("Unrecognized platform: %s" % (sys.platform,))

            # do the update in SG. this method should be wrapped in a try/except
            # to handle any issues here.
            logger.debug(
                "Updating SG local storage %s with %s: %s." %
                (storage_name, current_os_key, current_os_path)
            )
            update_data = sg.update(
                "LocalStorage",
                storage_data["id"],
                {current_os_key: current_os_path}
            )

            # update the path in the storage data
            storage_data[current_os_key] = update_data[current_os_key]
        else:
            # the storage does not exist in SG. we need to create it with the
            # edited OS paths.

            # push any edited text into the storage data
            storage_data["linux_path"] = self._linux_path_edit.get(
                storage_name, "")
            storage_data["mac_path"] = self._mac_path_edit.get(storage_name, "")
            storage_data["windows_path"] = self._windows_path_edit.get(
                storage_name, "")

            # delete the id field as it will be populated for us by SG. if we
            # don't delete it, we get errors.
            del storage_data["id"]

            # no storage exists in SG. create a new one
            logger.debug("Creating SG local storage: %s" % (storage_data,))
            storage_data = sg.create(
                "LocalStorage",
                storage_data,
                return_fields=storage_data.keys()
            )

        # update the storage in the model with the new data
        self._storage_model.update_storage(storage_name, storage_data)

        # it should be sufficient to set the newly created/updated storage
        # this will update the storage display in the UI
        self.local_storage = storage_data["code"]

    def _set_default_edit_state(self):
        """
        Convenience method to get the UI in its default state.
        :return:
        """

        # hide the entire path section
        self.ui.path_frame.hide()

        # ensure the edits are hidden
        self.ui.linux_path_edit.hide()
        self.ui.mac_path_edit.hide()
        self.ui.windows_path_edit.hide()

        # ensure the browse buttons are hidden
        self.ui.linux_path_browse.hide()
        self.ui.mac_path_browse.hide()
        self.ui.windows_path_browse.hide()

        # ensure the lock icon labels are hidden
        self.ui.linux_lock.hide()
        self.ui.mac_lock.hide()
        self.ui.windows_lock.hide()

        # ensure the save button is hidden
        self.ui.save_storage_btn.hide()

        # clear the paths
        self.ui.linux_path.setText("")
        self.ui.mac_path.setText("")
        self.ui.windows_path.setText("")

        # clear the edits
        self.ui.linux_path_edit.setText("")
        self.ui.mac_path_edit.setText("")
        self.ui.windows_path_edit.setText("")

        # hide the path displays
        self.ui.linux_path.hide()
        self.ui.mac_path.hide()
        self.ui.windows_path.hide()

        # hide the labels
        self.ui.linux_path_lbl.hide()
        self.ui.mac_path_lbl.hide()
        self.ui.windows_path_lbl.hide()

        # clear the info text
        self.ui.storage_info.setText("")

    def paintEvent(self, event):
        """
        As per the docs, implementing this in order to use stylesheets on a
        custom widget, allowing setting of bg color.

        See: https://wiki.qt.io/How_to_Change_the_Background_Color_of_QWidget
        """

        opt = QtGui.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtGui.QStyle.PE_Widget, opt, painter, self)

        super(StorageMapWidget, self).paintEvent(event)
