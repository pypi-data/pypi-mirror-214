#!/usr/bin/env python3
# https://stackoverflow.com/questions/40002373/qscintilla-based-text-editor-in-pyqt5-with-clickable-functions-and-variables

from PyQt6 import Qsci, QtGui

class MEditor(Qsci.QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)

        font = QtGui.QFont()
        font.setFamily('DejaVu Sans Mono')
        font.setFixedPitch(True)
        font.setPointSize(14)
        self.setFont(font)
        self.setMarginsFont(font)
        #self.zoomIn()
        #self.zoomOut()

        # Margin 0 is used for line numbers
        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginsFont(font)
        #self.setMarginWidth(0, fontmetrics.width("000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QtGui.QColor("#cccccc"))

        #self._marker = None
        # Clickable margin 1 for showing markers
        # self.setMarginSensitivity(1, True)
        # self.connect(self,
        #    SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),
        #    self.on_margin_clicked)
        #self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        #self.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)

        #self.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QtGui.QColor("#ffe4e4"))

        lexer = Qsci.QsciLexerYAML()
        lexer.setFont(font)
        self.setLexer(lexer)
        self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, 'Courier'.encode())

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # self.setWrapMode(Qsci.QsciScintilla.WrapWord)
        #self.setEolMode(Qsci.QsciScintilla.EolUnix)
        self.setEolVisibility(False)
        #self.setWhitespaceVisibility(True)

    def view_state(self):
        # In Qt5/PyQt5 how do I restore exact visible area and cursor
        #  position of QTextEdit?:
        # https://stackoverflow.com/questions/67751888

        # relative approach
        #try:
            #hPos = hBar.value() / hBar.maximum()
        #except ZeroDivisionError:
            #hPos = 0
        #try:
            #vPos = vBar.value() / vBar.maximum()
        #except ZeroDivisionError:
            #vPos = 0

        state = {
            "cursor_position": self.getCursorPosition(),
            "zoom": 0, # TODO: how to get?
            "hbar_pos": self.horizontalScrollBar().value(),
            "vbar_pos": self.verticalScrollBar().value(),
        }
        return state

    def set_view_state(self, state):
        if not state:
            return
        self.setCursorPosition(*state["cursor_position"])
        # hBar.setValue(hPos * hBar.maximum())  # relative approach
        # vBar.setValue(vPos * vBar.maximum())
        self.horizontalScrollBar().setValue(state["hbar_pos"])
        self.verticalScrollBar().setValue(state["vbar_pos"])
