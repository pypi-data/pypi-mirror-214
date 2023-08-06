#!/usr/bin/env python3

"""QrM - Connect to reMarkable and modify contents
"""

# pylint: disable=invalid-name

import logging
import signal
import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic


def log() -> logging.Logger:
    """Returns the local logger"""
    return logging.getLogger("medit.ui")


class MEditWindow(QtWidgets.QMainWindow):
    """The one and only application window"""

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(Path(__file__).parent / "medit.ui", self)
        #self.documents.horizontalHeader().setStretchLastSection(True)
        self.setAcceptDrops(True)

        #self.config = qrm_common.load_json(qrm_common.CFG_FILE)

        #self.txt_host.setText(auth.setdefault("host", "reMarkable"))
        #self.txt_username.setText(auth.setdefault("username", "root"))
        #self.txt_password.setText(auth.setdefault("password", "---"))
        #self.txt_host.textChanged.connect(self.on_txt_host_textChanged)
        #self.txt_username.textChanged.connect(self.on_txt_username_textChanged)
        #self.txt_password.textChanged.connect(self.on_txt_password_textChanged)
        #self.pb_connect.clicked.connect(self.connect)
        #self.pb_reboot.clicked.connect(self.on_pb_reboot_clicked)
        #self.pb_reboot.setEnabled(False)

        #self.setGeometry(*self.config.get("window_geometry", (50, 50, 1000, 500)))
        self.show()

    #def on_txt_host_textChanged(self, text: str) -> None:
        #"""React on hostname modification"""
        #self.config["auth"]["host"] = text

    def event(self, event: QtCore.QEvent) -> bool:
        #if event.type() == QtCore.QEvent.DragEnter:
            #if any(
                #Path(u.url()).suffix.lower() in {".pdf", ".epub"} for u in event.mimeData().urls()
            #):
                #event.accept()
        #elif event.type() == QtCore.QEvent.Drop:
            #urls = [
                #path
                #for u in event.mimeData().urls()
                #if (path := Path(u.url())).suffix.lower() in {".pdf", ".epub"}
            #]
            #print(urls)

        #elif not event.type() in {
            #QtCore.QEvent.UpdateRequest,
            #QtCore.QEvent.Paint,
            #QtCore.QEvent.Enter,
            #QtCore.QEvent.HoverEnter,
            #QtCore.QEvent.HoverMove,
            #QtCore.QEvent.HoverLeave,
            #QtCore.QEvent.KeyPress,
            #QtCore.QEvent.KeyRelease,
            #QtCore.QEvent.DragMove,
            #QtCore.QEvent.DragLeave,
        #}:
            ## log().warn("unknown event: %r %r", event.type(), event)
            #pass
        return super().event(event)

    def closeEvent(self, _event: QtGui.QCloseEvent) -> None:
        """save state before shutting down"""
        #logging.info("got some closish signal, bye")
        #geom = self.geometry()
        #qrm_common.save_json(
            #qrm_common.CFG_FILE,
            #{
                #**self.config,
                #**{
                    #"window_geometry": (geom.x(), geom.y(), geom.width(), geom.height()),
                #},
            #},
        #)


def main() -> None:
    """Typical PyQt5 boilerplate main entry point"""
    logging.getLogger().setLevel(logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    window = MEditWindow()

    for s in (signal.SIGABRT, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
        signal.signal(s, lambda signal, frame: window.close())

    # catch the interpreter every now and then to be able to catch signals
    timer = QtCore.QTimer()
    timer.start(200)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
