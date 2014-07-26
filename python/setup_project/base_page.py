# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from sgtk.platform.qt import QtGui


class BasePage(QtGui.QWizardPage):
    """ Base page for all Shotgun pages to inherit from. """
    def __init__(self, parent=None):
        """ Constructor """
        QtGui.QWizardPage.__init__(self, parent)
        self._page_id = None
        self._next_page_id = None

    def setup_ui(self, page_id):
        """ Setup page UI after the Wizard's UI has been setup from the uic. """
        self._page_id = page_id

    def page_id(self):
        """ Return the cached id of this page """
        return self._page_id

    def set_next_page(self, page):
        """ Override which page comes next """
        self._next_page_id = page.page_id()

    def nextId(self):
        """ Enhanced logic for non-linear wizards """
        if self._next_page_id is None:
            return QtGui.QWizardPage.nextId(self)

        return self._next_page_id


class UriSelectionPage(BasePage):
    """ Base page for Shotgun pages that specify and validate the config uri """
    def __init__(self, parent=None):
        BasePage.__init__(self, parent)
        self._storage_locations_page = None

    def set_storage_locations_page(self, page):
        self._storage_locations_page = page

    def nextId(self):
        if self._storage_locations_page is not None and self._storage_locations_page.show_page():
            # need to display the storage locations page
            return self._storage_locations_page.page_id()

        # all storages are accounted for, skip the storage locations page
        return self._storage_locations_page.nextId()
