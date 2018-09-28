# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sys

import sgtk.platform
from sgtk.platform.qt import QtCore

from .base_page import BasePage

LOG_TIMER_INTERVAL = 150 # milliseconds

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
    def __init__(self, parent=None):
        BasePage.__init__(self, parent)

        self._thread_success = False
        self._original_next_css = None
        self._original_next_text = None
        self._new_logs = []
        self._chapter = None
        self._progress = None

        self._log_timer = QtCore.QTimer(parent=self)
        self._log_timer.timeout.connect(self._process_new_logged_info)
        self._log_timer.start(LOG_TIMER_INTERVAL)

        self.execute_thread = None

    def setup_ui(self, page_id):
        BasePage.setup_ui(self, page_id)

        wiz = self.wizard()
        wiz.ui.progress_output.hide()
        wiz.ui.additional_details_button.pressed.connect(self.additional_details_pressed)

    def initializePage(self):
        # disable the cancel and back buttons
        wiz = self.wizard()
        wiz.button(wiz.NextButton).setEnabled(False)

        self._original_next_text = wiz.buttonText(wiz.NextButton)
        self._original_next_css = wiz.button(wiz.NextButton).styleSheet()

        wiz.setButtonText(wiz.NextButton, "Running...")

        if QtCore.__version__.startswith("5."):
            wiz.button(wiz.NextButton).setStyleSheet("background-color: rgb(75, 75, 75);")
        else:
            wiz.button(wiz.NextButton).setStyleSheet("background-color: rgb(128, 128, 128);")

        # setup for progress reporting
        wiz.ui.progress.setValue(0)
        wiz.core_wizard.set_progress_callback(self.progress_callback)

        # run the thread
        self.execute_thread = RunSetupThread(wiz.core_wizard)
        self.execute_thread.success.connect(self._on_run_succeeded)
        self.execute_thread.failure.connect(self._on_run_failed)
        self.execute_thread.finished.connect(self._on_thread_finished)
        self.execute_thread.start()

        # can no longer cancel or hit back
        wiz.setButtonLayout([wiz.HelpButton, wiz.Stretch, wiz.NextButton, wiz.FinishButton])

    def additional_details_pressed(self):
        # handle the additional details toggle being pressed
        wiz = self.wizard()

        # show the additional details and hide the additional details button
        wiz.ui.progress_output.show()
        wiz.ui.additional_details_button.hide()

    def append_log_message(self, text):
        """
        Appends the given log message to the list of logs to be added to the
        details widget.

        :param str text: The log message to show the user.
        """
        self._new_logs.append(text)

    def _process_new_logged_info(self):
        """
        Triggers appending of new logs since the last call to the progress output
        widget in the wizard. This must be called on the main thread.
        """
        wiz = self.wizard()

        while self._new_logs:
            # We're going to check the progress and chapter on each iteration
            # so we catch anything that was sent out way without it having to
            # wait for us to get through adding all of the log messages.
            if self._progress or self._chapter:
                self.__progress_on_main_thread(self._chapter, self._progress)
                self._chapter = None
                self._progress = None

            wiz.ui.progress_output.appendHtml(self._new_logs.pop(0))
            cursor = wiz.ui.progress_output.textCursor()
            cursor.movePosition(cursor.End)
            cursor.movePosition(cursor.StartOfLine)
            wiz.ui.progress_output.setTextCursor(cursor)
            wiz.ui.progress_output.ensureCursorVisible()

        # One last check of the progress and chapter. We've been checking it above
        # in the loop that's adding logs, but we might not have had any of those to
        # process this time.
        if self._progress or self._chapter:
            self.__progress_on_main_thread(self._chapter, self._progress)
            self._chapter = None
            self._progress = None

    def progress_callback(self, chapter, progress):
        # Since a thread could be calling this make sure we are doing GUI work on the main thread.
        # On Windows and CentOS, we have stability issues related to the async main thread executor,
        # so we're not going to rely on it here. Instead, we track the chapter and progress values
        # and we let the QTimer we have running find them and set them from the main thread without
        # the need for any direct cross-thread communication.
        #
        # NOTE: OSX is the exception. We don't have stability issues there related to the main thread
        # execution, and we get MUCH better progress-bar performance/UX when we skip using the
        # QTimer approach to keeping it updated.
        if sys.platform == "darwin":
            engine = sgtk.platform.current_engine()
            engine.async_execute_in_main_thread(self.__progress_on_main_thread, chapter, progress)
        else:
            self._chapter = chapter
            self._progress = progress

    def __progress_on_main_thread(self, chapter, progress):
        # update the progress display
        if progress is not None:
            wiz = self.wizard()
            wiz.ui.message.setText(chapter)
            wiz.ui.progress.setValue(progress)
        # Ensure that the progress bar repaints with the new value. This is also going
        # to help make sure that the progress bar and any log messages added to the
        # progress output widget stay in sync.
        QtCore.QCoreApplication.processEvents()

    def _on_run_finished(self):
        # since a thread could be calling this make sure we are doing GUI work on the main thread
        engine = sgtk.platform.current_engine()
        engine.async_execute_in_main_thread(self._on_run_finished_main_thread)

    def _on_run_finished_main_thread(self):
        # thread has finished
        # clean up the page state
        wiz = self.wizard()
        wiz.button(wiz.NextButton).setEnabled(True)

    def _on_run_succeeded(self):
        # since a thread could be calling this make sure we are doing GUI work on the main thread
        engine = sgtk.platform.current_engine()
        engine.async_execute_in_main_thread(self._on_run_succeeded_main_thread)

    def _on_run_succeeded_main_thread(self):
        # thread finished successfully
        self._on_run_finished()

        self._thread_success = True

        wiz = self.wizard()
        wiz.ui.progress.setValue(100)
        wiz.ui.message.setText("Set up finished")
        wiz.setButtonText(wiz.NextButton, self._original_next_text)
        wiz.button(wiz.NextButton).setStyleSheet(self._original_next_css)

        if wiz.ui.progress_output.isHidden():
            # auto advance if details are not shown
            wiz.next()

    def _on_run_failed(self, message):
        # since a thread could be calling this make sure we are doing GUI work on the main thread
        engine = sgtk.platform.current_engine()
        engine.async_execute_in_main_thread(self._on_run_failed_main_thread, message)

    def _on_run_failed_main_thread(self, message):
        # thread failed
        self._on_run_finished()

        # show the failure icon and message
        wiz = self.wizard()
        wiz.button(wiz.CancelButton).setVisible(True)
        wiz.setButtonText(wiz.NextButton, "Quit")
        wiz.ui.complete_errors.setText(message)

    def _on_thread_finished(self):
        # since a thread could be calling this make sure we are doing GUI work on the main thread
        engine = sgtk.platform.current_engine()
        engine.async_execute_in_main_thread(self._on_thread_finished_main_thread)

    def _on_thread_finished_main_thread(self):
        # let the wizard know that our complete state has changed
        self.completeChanged.emit()

        # Force one more timeout to clear any logs, then stop the timer.
        self._log_timer.timeout.emit()
        self._log_timer.stop()

    def isComplete(self):
        return self._thread_success
