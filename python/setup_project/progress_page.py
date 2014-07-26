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
from sgtk.platform.qt import QtCore

from .base_page import BasePage


class RunSetupThread(QtCore.QThread):
    """ Simple thread to run the wizard in the background """
    success = QtCore.Signal()
    failure = QtCore.Signal(str)

    def __init__(self, wizard, parent=None):
        QtCore.QThread.__init__(self, parent)
        self._wizard = wizard

    def run(self):
        try:
            self._wizard.execute()
            self.success.emit()
        except Exception, e:
            self.failure.emit(str(e))


class ProgressPage(BasePage):
    """ Page to show the progress bar during configuration setup. """
    def setup_ui(self, page_id):
        BasePage.setup_ui(self, page_id)

        wiz = self.wizard()
        wiz.ui.complete_icon.setVisible(False)

    def append_log_message(self, text):
        # append the log message to the end of the logging area
        wiz = self.wizard()
        wiz.ui.progress_output.appendHtml(text)
        cursor = wiz.ui.progress_output.textCursor()
        cursor.movePosition(cursor.End)
        cursor.movePosition(cursor.StartOfLine)
        wiz.ui.progress_output.setTextCursor(cursor)
        wiz.ui.progress_output.ensureCursorVisible()

    def initializePage(self):
        # disable the cancel and back buttons
        wiz = self.wizard()
        wiz.button(wiz.CancelButton).setVisible(False)
        wiz.button(wiz.BackButton).setVisible(False)
        wiz.button(wiz.FinishButton).setEnabled(False)

        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        # run the thread
        self.execute_thread = RunSetupThread(wiz.core_wizard)
        self.execute_thread.success.connect(self._on_run_succeeded)
        self.execute_thread.failure.connect(self._on_run_failed)
        self.execute_thread.start()

    def _on_run_finished(self):
        # thread has finished
        # clean up the page state
        wiz = self.wizard()
        wiz.ui.complete_icon.setVisible(True)
        QtGui.QApplication.restoreOverrideCursor()
        button = wiz.button(wiz.FinishButton)
        button.setEnabled(True)

    def _on_run_succeeded(self):
        # thread finished successfully
        self._on_run_finished()
        wiz = self.wizard()

        # show the success icon and message
        wiz.ui.complete_icon.setPixmap(":/tk-framework-adminui/setup_project/checkmark.png")
        wiz.ui.complete_errors.setText("")
        wiz.ui.complete_label.setText("""
            <html><head/><body>
                <p><span style=" font-size:26pt;">Project Setup Complete</span></p>
            </body></html>
        """)

    def _on_run_failed(self, message):
        # thread failed
        self._on_run_finished()
        wiz = self.wizard()

        # show the failure icon and message
        wiz.ui.complete_icon.setPixmap(":/tk-framework-adminui/setup_project/error.png")
        wiz.ui.complete_errors.setText(message)
        wiz.ui.complete_label.setText("""
            <html><head/><body>
                <p><span style=" font-size:26pt;">Error During Setup</span></p>
            </body></html>
        """)

        def isFinalPage(self):
            return True
