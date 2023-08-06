#!/usr/bin/env python3

import sys
import os
import yaml
import json
import inotify.adapters
from contextlib import suppress
import signal
import logging

from PyQt5 import QtWidgets, QtCore, uic

CFG_FILE = "~/.yatl.cfg"


class SafeLineLoader(yaml.loader.SafeLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


def text_from_file(filename):
    with suppress(FileNotFoundError):
        with open(filename) as f:
            return f.read()
    return ""

def parse_with_locations(text):
    def remove_line_info(elem):
        if isinstance(elem, dict):
            if "__line__" in elem:
                del elem["__line__"]
            for e in elem.values():
                remove_line_info(e)
        elif isinstance(elem, list):
            for e in elem:
                remove_line_info(e)

    # todo: respect tree
    # todo: remove __line__ recursively
    locations = {}
    data = yaml.load(text, Loader=SafeLineLoader) or []
    for elem in data:
        if not isinstance(elem, dict):
            continue
        oid, line = id(elem), elem["__line__"]
        #locations[oid] = line
        remove_line_info(elem)
        locations[line] = elem
    return data, locations


def inotify_stuff(dirname, obj, method):
    logging.debug("Start monitoring %s", dirname)
    i = inotify.adapters.Inotify()
    i.add_watch(dirname or ".")
    for _, type_names, path, filename in i.event_gen(yield_nones=False):
        if not filename.endswith('.yaml'):
            continue

        if 'IN_MOVED_TO' not in type_names:
            #logging.debug(type_names)
            continue

        QtCore.QMetaObject.invokeMethod(
            obj, method, QtCore.Qt.QueuedConnection,
            #QtCore.Q_ARG(list, [])
        )


def load_default(filename, default):
    with suppress(FileNotFoundError, json.JSONDecodeError):
        return json.load(open(os.path.expanduser(CFG_FILE)))
    return default


class Yatl(QtWidgets.QMainWindow):
    def __init__(self, filename):
        super().__init__()

        config = load_default(CFG_FILE, {})

        self.filename = os.path.expanduser(filename or config.get("filename", "yatl.yaml"))
        logging.info("use %s", self.filename)
        self.data, self.locations = None, None
        self.dirty = False
        self.setMouseTracking(True)
        self._directory = os.path.dirname(os.path.realpath(__file__))
        self.autoload_thread = QtCore.QThread(self)
        self.autoload_thread.run = (lambda: inotify_stuff(
            os.path.dirname(self.filename), self, "_on_file_changed"))
        self.autoload_thread.start()
        self.autosave_timer = QtCore.QTimer(self)
        self.autosave_timer.timeout.connect(self.on_autosave_timer_timeout)
        uic.loadUi(os.path.join(self._directory, 'yatl.ui'), self)
        self.setGeometry(*config.get("window_geometry", (50, 50, 1000, 500)))
        self.load()
        self.txt_yaml.set_view_state(config.get("editor_view_state"))
        self.show()

    def reset_timer(self):
        logging.debug("reset modification timer")
        self.autosave_timer.start(2500)

    def on_autosave_timer_timeout(self):
        """"""
        self.autosave_timer.stop()
        self.save()

    def on_txt_yaml_textChanged(self):
        self.dirty = True
        self.reset_timer()
        self.parse_text()

    def on_txt_yaml_cursorPositionChanged(self, x, y):
        self.update_current()

    def parse_text(self):
        _text = self.txt_yaml.text()
        try:
            self.data, self.locations = parse_with_locations(_text)
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as exc:
            self.txt_current.setPlainText(str(exc))
            self.data, self.locations = None, None
        self.update_current()

    def render_element(self, element):
        def s(elem, depth):
            return (" " * depth * 2) + str(elem)

        def r(elem, depth):
            if isinstance(elem, dict):
                return tuple(
                    e
                    for k, v in elem.items()
                    for e in ((s(k, depth), '') + r(v, depth + 1) + ('',)))
            if isinstance(elem, list):
                return tuple(
                    e for v in elem
                    for e in r(v, depth + 1))
            if isinstance(elem, (str, float)):
                return (s(elem, depth),)
            return (yaml.dump(elem),)

        lines = r(element, 0)
        return "\n".join(lines)

    def update_current(self):
        if self.locations is None:
            return

        line = self.txt_yaml.getCursorPosition()[0] + 1
        for l, o in reversed(tuple(self.locations.items())):
            if l > line:
                continue
            #self.txt_current.setPlainText(yaml.dump(o, allow_unicode=True))
            self.txt_current.setPlainText(self.render_element(o))
            return
        self.txt_current.setPlainText("-- no content --")

    def load(self):
        logging.info("load from %s", self.filename)
        new_content = text_from_file(self.filename)

        if new_content == self.txt_yaml.text():
            logging.debug("content identical - abort")
            return

        stored_block_signals = self.txt_yaml.blockSignals(True)
        try:
            stored_view_state = self.txt_yaml.view_state()
            self.txt_yaml.setText(new_content)
            self.txt_yaml.set_view_state(stored_view_state)

        finally:
            self.txt_yaml.blockSignals(stored_block_signals)
            self.parse_text()

    @QtCore.pyqtSlot()
    def _on_file_changed(self):
        logging.debug("_on_file_changed")
        self.load()

    def save(self):
        if not self.dirty:
            return
        logging.debug("save to %s", self.filename)
        self.dirty = True
        text_to_save = self.txt_yaml.text()
        if not text_to_save:
            logging.warning("I don't dare to overwrite with empty content..")
            return
        open(self.filename, 'w').write(text_to_save)

    def closeEvent(self,e):
        logging.info("got some closish signal, bye")
        self.autoload_thread.terminate()
        self.autoload_thread.wait()
        self.save()
        g = self.geometry()
        json.dump({
            "window_geometry": (g.x(), g.y(), g.width(), g.height()),
            "editor_view_state": self.txt_yaml.view_state(),
            "filename": self.filename,
            }, open(os.path.expanduser(CFG_FILE), "w")
        )

def main():
    logging.getLogger().setLevel(logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    window = Yatl(sys.argv[1] if len(sys.argv) > 1 else None)

    for s in {signal.SIGABRT, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM}:
        signal.signal(s, lambda signal, frame: window.close())

    # catch the interpreter every now and then to be able to catch signals
    timer = QtCore.QTimer()
    timer.start(200)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

