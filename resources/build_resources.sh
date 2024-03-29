#!/usr/bin/env bash
#
# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

# The path to where the PySide binaries are installed
PYTHON_BASE="/Applications/Shotgun.app/Contents/Resources/Python"


# Helper functions to build UI files
function build_qt {
    echo " > Building " $2

    # compile ui to python
    $1 $2 > $UI_PYTHON_PATH/$3.py

    # replace PySide imports with sgtk.platform.qt and remove line containing Created by date
    sed -i "" -e "s/from PySide import/from sgtk.platform.qt import/g" -e "/# Created:/d" $UI_PYTHON_PATH/$3.py
}

function build_ui {
    build_qt "${PYTHON_BASE}/bin/python ${PYTHON_BASE}/bin/pyside-uic --from-imports" "$1.ui" "$1"
}

function build_res {
    build_qt "${PYTHON_BASE}/bin/pyside-rcc -py3" "$1.qrc" "$1_rc"
}

# build main UIs:
echo "building user interfaces..."
UI_PYTHON_PATH=../python/ui
build_ui wait_screen
build_ui setup_project
build_ui create_storage_dialog
build_ui storage_map_widget

# build resources
echo "building resources..."
build_res resources
