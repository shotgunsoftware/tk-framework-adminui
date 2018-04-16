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
            lambda p: self._on_path_changed(p, "linux2"))
        self.ui.mac_path_edit.textChanged.connect(
            lambda p: self._on_path_changed(p, "darwin"))
        self.ui.windows_path_edit.textChanged.connect(
            lambda p: self._on_path_changed(p, "win32"))

        # connect the file browse buttons
        self.ui.linux_path_browse.clicked.connect(
            lambda: self._browse_path("linux2"))
        self.ui.mac_path_browse.clicked.connect(
            lambda: self._browse_path("darwin"))
        self.ui.windows_path_browse.clicked.connect(
            lambda: self._browse_path("win32"))

        # connect the save button
        self.ui.save_storage_btn.clicked.connect(self._on_storage_save_clicked)

        # we need to disable the wheel scrolling on the storage combobox.
        # install an event filter on it to intercept and ignore wheel events.
        self.ui.storage_select_combo.installEventFilter(self)

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

        # clear the storage info text to begin
        self.ui.storage_info.setText("")

        # hide this by default
        self.ui.save_storage_btn.hide()

        # root is not mapped to a local storage
        if not local_storage:
            self.ui.storage_info.setText("* No storage selected")
            return False

        storage_name = local_storage["code"]

        # ---- first, validate any edited paths:

        if self.ui.linux_path_edit.isVisible():
            is_current_os = sys.platform.startswith("linux")
            edited_linux_path = self._linux_path_edit.get(storage_name)
            if edited_linux_path:
                (is_valid, reason) = self._path_is_valid(
                    edited_linux_path, is_current_os)
                if is_valid:
                    self.ui.save_storage_btn.show()
                    self.ui.storage_info.setText(
                        "* Please save the linux path before proceeding.")
                    return False
                else:
                    self.ui.storage_info.setText(
                        "* Linux path is invalid: %s" % (reason,))
                    return False

        if self.ui.mac_path_edit.isVisible():
            is_current_os = sys.platform == "darwin"
            edited_mac_path = self._mac_path_edit.get(storage_name)
            if edited_mac_path:
                (is_valid, reason) = self._path_is_valid(
                    edited_mac_path, is_current_os)
                if is_valid:
                    self.ui.save_storage_btn.show()
                    self.ui.storage_info.setText(
                        "* Please save the mac path before proceeding.")
                    return False
                else:
                    self.ui.storage_info.setText(
                        "* Mac path is invalid: %s" % (reason,))
                    return False

        if self.ui.windows_path_edit.isVisible():
            is_current_os = sys.platform == "win32"
            edited_windows_path = self._windows_path_edit.get(storage_name)
            if edited_windows_path:
                (is_valid, reason) = self._path_is_valid(
                    edited_windows_path, is_current_os)
                if is_valid:
                    self.ui.save_storage_btn.show()
                    self.ui.storage_info.setText(
                        "* Please save the windows path before proceeding.")
                    return False
                else:
                    self.ui.storage_info.setText(
                        "* Windows path is invalid: %s" % (reason,))
                    return False

        # get the stored paths once to make the code below a bit more readable
        linux_path = local_storage.get("linux_path")
        mac_path = local_storage.get("mac_path")
        windows_path = local_storage.get("windows_path")

        # get the current os path
        if sys.platform.startswith("linux"):
            current_os_path = linux_path
        elif sys.platform == "darwin":
            current_os_path = mac_path
        elif sys.platform == "win32":
            current_os_path = windows_path
        else:
            raise Exception("Unrecognized platform: %s" % (sys.platform,))

        # no path for the current os
        if not current_os_path:
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

            # set the tooltips as well
            self.ui.linux_path.setToolTip(linux_path)
            self.ui.mac_path.setToolTip(mac_path)
            self.ui.windows_path.setToolTip(windows_path)

            # show lock if the path is defined, else make the path editable
            if linux_path:
                self.ui.linux_lock.show()
            else:
                self._set_path_editable("linux")
                if sys.platform.startswith("linux"):
                    self.ui.linux_path_browse.show()
                    self.ui.linux_path_edit.setFocus()

            if mac_path:
                self.ui.mac_lock.show()
            else:
                self._set_path_editable("mac")
                if sys.platform == "darwin":
                    self.ui.mac_path_browse.show()
                    self.ui.mac_path_edit.setFocus()

            if windows_path:
                self.ui.windows_lock.show()
            else:
                self._set_path_editable("windows")
                if sys.platform == "win32":
                    self.ui.windows_path_browse.show()
                    self.ui.windows_path_edit.setFocus()

        else:
            # this is a new storage that hasn't been created in SG yet.

            # show the path edit widgets
            self.ui.linux_path_edit.show()
            self.ui.mac_path_edit.show()
            self.ui.windows_path_edit.show()

            # show the browse button for the current os
            if sys.platform.startswith("linux") and not linux_path:
                self.ui.linux_path_edit.setFocus()
                self.ui.linux_path_browse.show()
            elif sys.platform == "darwin" and not mac_path:
                self.ui.mac_path_edit.setFocus()
                self.ui.mac_path_browse.show()
            elif sys.platform == "win32" and not windows_path:
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
            # store lower case names so we can do case insensitive comparisons
            storage_name = storage["code"].lower()
            storage_id = storage["id"]
            storage_by_id[storage_id] = storage
            storage_by_name[storage_name] = storage

        # see if a shotgun storage id is defined in the root info.
        root_sg_id = self.root_info.get("shotgun_id")
        if root_sg_id in storage_by_id:
            # shotgun id defined explicitly for this root. set it!
            self.local_storage = storage_by_id[root_sg_id]["code"]

        # does name match an existing storage?
        elif self.root_name.lower() in storage_by_name:
            storage_key = self.root_name.lower()
            self.local_storage = storage_by_name[storage_key]["code"]

        # has this name been mapped before?
        elif self._best_guess and self._best_guess.lower() in storage_by_name:
            storage_key = self._best_guess.lower()
            self.local_storage = storage_by_name[storage_key]["code"]

        # fall back to requiring the user to manually select an item
        else:
            self.local_storage = self._storage_model.CHOOSE_STORAGE_ITEM_TEXT

    def set_count(self, num, total):
        """Simply sets the text of the count label of the widget. ex (1 of 3)"""

        self.ui.count_lbl.setText("%s of %s" % (num, total))

    def _browse_path(self, platform):
        """Browse and set the path for the supplied platform.

        :param platform: A string indicating the platform to associate with the
            browsed path. Should match the strings returned by ``sys.platform``.
        """

        # create the dialog
        folder_path = QtGui.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Choose Storage Root Folder",
            options=QtGui.QFileDialog.DontResolveSymlinks |
                    QtGui.QFileDialog.DontUseNativeDialog |
                    QtGui.QFileDialog.ShowDirsOnly
        )

        if not folder_path:
            return

        # create the SG path object. assigning the path to the corresponding
        # OS property below will sanitize
        sg_path = ShotgunPath()

        if platform.startswith("linux"):
            sg_path.linux = folder_path
            self.ui.linux_path_edit.setText(sg_path.linux)
        elif platform == "darwin":
            sg_path.macosx = folder_path
            self.ui.mac_path_edit.setText(sg_path.macosx)
        elif platform == "win32":
            sg_path.windows = folder_path
            self.ui.windows_path_edit.setText(sg_path.windows)

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

    def _on_path_changed(self, path, platform):
        """
        Keep track of any path edits as they happen. Keep the user informed if
        there are any concerns about the entered text.

        :param path: The path that has changed.
        :param platform: The platform the modified path is associated with.
        """

        # does the path only contain slashes?
        only_slashes = path.replace("/", "").replace("\\", "") == ""

        # does it end in a slash?
        trailing_slash = path.endswith("/") or path.endswith("\\")

        # the name of the storage being edited
        storage_name = str(self.ui.storage_select_combo.currentText())

        # a temp SG path object used for sanitization
        sg_path = ShotgunPath()

        # store the edited path in the appropriate path lookup. sanitize first
        # by running it through the ShotgunPath object. since sanitize removes
        # the trailing slash, add it back in if the user typed it.
        # if the sanitized path differs, update the edit.
        if platform.startswith("linux"):
            if only_slashes:
                # SG path code doesn't like only slashes in a path
                self._linux_path_edit[storage_name] = path
            elif path:
                sg_path.linux = path  # sanitize
                sanitized_path = sg_path.linux
                if trailing_slash:
                    # add the trailing slash back in
                    sanitized_path = "%s/" % (sanitized_path,)
                if sanitized_path != path:
                    # path changed due to sanitation. change it in the UI
                    self.ui.linux_path_edit.setText(sanitized_path)
                # remember the sanitized path
                self._linux_path_edit[storage_name] = sanitized_path
            else:
                # no path. update the edit lookup to reflect
                self._linux_path_edit[storage_name] = ""
        elif platform == "darwin":
            if only_slashes:
                # SG path code doesn't like only slashes in a path
                self._mac_path_edit[storage_name] = path
            elif path:
                sg_path.macosx = path  # sanitize
                sanitized_path = sg_path.macosx
                if trailing_slash:
                    # add the trailing slash back in
                    sanitized_path = "%s/" % (sanitized_path,)
                if sanitized_path != path:
                    # path changed due to sanitation. change it in the UI
                    self.ui.mac_path_edit.setText(sanitized_path)
                # remember the sanitized path
                self._mac_path_edit[storage_name] = sanitized_path
            else:
                # no path. update the edit lookup to reflect
                self._mac_path_edit[storage_name] = ""
        elif platform == "win32":
            if only_slashes:
                # SG path code doesn't like only slashes in a path
                self._windows_path_edit[storage_name] = path
            elif path:
                sg_path.windows = path  # sanitize
                sanitized_path = sg_path.windows
                if trailing_slash and not sanitized_path.endswith("\\"):
                    # add the trailing slash back in
                    sanitized_path = "%s\\" % (sanitized_path,)
                if sanitized_path != path:
                    # path changed due to sanitation. change it in the UI
                    self.ui.windows_path_edit.setText(sanitized_path)
                # remember the sanitized path
                self._windows_path_edit[storage_name] = sanitized_path
            else:
                # no path. update the edit lookup to reflect
                self._windows_path_edit[storage_name] = ""

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
            # the storage exists in SG. we want to update any edited paths

            path_data = {}

            if self.ui.linux_path_edit.isVisible():
                path_data["linux_path"] = \
                    self._linux_path_edit.get(storage_name, "")

            if self.ui.mac_path_edit.isVisible():
                path_data["mac_path"] = \
                    self._mac_path_edit.get(storage_name, "")

            if self.ui.windows_path_edit.isVisible():
                path_data["windows_path"] = \
                    self._windows_path_edit.get(storage_name, "")

            # do the update in SG. this method should be wrapped in a try/except
            # to handle any issues here.
            logger.debug("Updating SG local storage: %s." % (path_data,))
            update_data = sg.update(
                "LocalStorage",
                storage_data["id"],
                path_data
            )

            # update the path in the storage data
            storage_data.update(update_data)
        else:
            # the storage does not exist in SG. we need to create it with the
            # edited OS paths.

            # push any edited text into the storage data
            storage_data["linux_path"] = self._linux_path_edit.get(
                storage_name, "")
            storage_data["mac_path"] = self._mac_path_edit.get(
                storage_name, "")
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

    def _set_path_editable(self, os_name):
        """
        Convenience method to enable editing for an OS path.
        """

        storage_name = self.ui.storage_select_combo.currentText()

        if os_name == "linux":
            edited_linux_path = self._linux_path_edit.get(storage_name, "")
            self.ui.linux_path.hide()
            self.ui.linux_lock.hide()
            self.ui.linux_path_edit.show()
            self.ui.linux_path_edit.setText(edited_linux_path)

        elif os_name == "mac":
            edited_mac_path = self._mac_path_edit.get(storage_name, "")
            self.ui.mac_path.hide()
            self.ui.mac_lock.hide()
            self.ui.mac_path_edit.show()
            self.ui.mac_path_edit.setText(edited_mac_path)

        elif os_name == "windows":
            edited_windows_path = self._windows_path_edit.get(storage_name, "")
            self.ui.windows_path.hide()
            self.ui.windows_lock.hide()
            self.ui.windows_path_edit.show()
            self.ui.windows_path_edit.setText(edited_windows_path)

    def _set_default_edit_state(self):
        """
        Convenience method to get the UI in its default state.
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

        # clear the tooltips
        self.ui.linux_path.setToolTip("")
        self.ui.mac_path.setToolTip("")
        self.ui.windows_path.setToolTip("")

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

    def _path_is_valid(self, path, is_current_os_path):
        """
        Returns a tuple. First value is True if the path is a valid storage
        path. The second value is a string message describing the problem if the
        first value is False (invalid storage path).
        """

        # make sure the path isn't just a separator
        if path == os.path.sep:
            return False, "Please provide a directory name for the storage."

        if is_current_os_path:
            # current os path must be absolute path
            if not os.path.isabs(path):
                return False, "* The current OS storage path must be absolute."

        return True, None

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

    def eventFilter(self, q_object, event):
        """
        Handles intercepting object/widget events such as the wheel event on the
        storage selection combo box.

        :param q_object: The monitored q_object where an event occured.
        :param event:
        :return:
        """

        if (event.type() == QtCore.QEvent.Wheel and
            q_object == self.ui.storage_select_combo):
            # Ignore wheel events on the storage select combo
            return True

        return False