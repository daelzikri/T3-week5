# Nama : Pudael Zikri
# NIM  : F1D02310088
# Kelas: C

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMessageBox, QFontDialog, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QDialogButtonBox,
    QStatusBar, QToolBar, QMenuBar
)
from PySide6.QtGui import (
    QAction, QKeySequence, QFont, QIcon, QTextCursor
)
from PySide6.QtCore import Qt, QSize


QSS = """
QMainWindow {
    background-color: #1e1e2e;
}

QMenuBar {
    background-color: #181825;
    color: #cdd6f4;
    font-size: 13px;
    padding: 2px;
    border-bottom: 1px solid #313244;
}

QMenuBar::item {
    background-color: transparent;
    padding: 5px 10px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #313244;
    color: #89b4fa;
}

QMenu {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 4px;
}

QMenu::item {
    padding: 6px 24px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #313244;
    color: #89b4fa;
}

QMenu::separator {
    height: 1px;
    background: #45475a;
    margin: 4px 8px;
}

QToolBar {
    background-color: #181825;
    border-bottom: 1px solid #313244;
    padding: 4px 6px;
    spacing: 4px;
}

QToolBar::separator {
    width: 1px;
    background: #45475a;
    margin: 4px 6px;
}

QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 5px;
    padding: 5px 12px;
    font-size: 12px;
    min-width: 60px;
}

QPushButton:hover {
    background-color: #45475a;
    border-color: #89b4fa;
    color: #89b4fa;
}

QPushButton:pressed {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QTextEdit {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border: none;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    padding: 12px;
    selection-background-color: #45475a;
    selection-color: #cdd6f4;
    line-height: 1.6;
}

QStatusBar {
    background-color: #89b4fa;
    color: #1e1e2e;
    font-size: 12px;
    font-weight: bold;
    padding: 2px 8px;
    border-top: 1px solid #7287fd;
}

QDialog {
    background-color: #1e1e2e;
    color: #cdd6f4;
}

QLabel {
    color: #cdd6f4;
    font-size: 13px;
}

QLineEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #89b4fa;
}

QCheckBox {
    color: #cdd6f4;
    font-size: 13px;
    spacing: 6px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid #45475a;
    background-color: #313244;
}

QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}

QScrollBar:vertical {
    background: #181825;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #45475a;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #89b4fa;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #181825;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background: #45475a;
    border-radius: 5px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background: #89b4fa;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}
"""

class FindReplaceDialog(QDialog):
    def __init__(self, editor: QTextEdit, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Find & Replace")
        self.setMinimumWidth(420)
        self.setModal(False)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        find_row = QHBoxLayout()
        find_row.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Cari teks...")
        find_row.addWidget(self.find_input)
        layout.addLayout(find_row)

        replace_row = QHBoxLayout()
        replace_row.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Ganti dengan...")
        replace_row.addWidget(self.replace_input)
        layout.addLayout(replace_row)

        self.case_cb = QCheckBox("Case Sensitive")
        layout.addWidget(self.case_cb)

        btn_layout = QHBoxLayout()
        self.btn_find_next    = QPushButton("Find Next")
        self.btn_replace      = QPushButton("Replace")
        self.btn_replace_all  = QPushButton("Replace All")
        self.btn_close        = QPushButton("Close")

        for btn in [self.btn_find_next, self.btn_replace, self.btn_replace_all, self.btn_close]:
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.btn_find_next.clicked.connect(self.find_next)
        self.btn_replace.clicked.connect(self.replace_one)
        self.btn_replace_all.clicked.connect(self.replace_all)
        self.btn_close.clicked.connect(self.close)

    def _flags(self):
        flags = QTextDocument.FindFlags() if hasattr(Qt, 'FindCaseSensitively') else QTextCursor.MoveAnchor
        flags = 0
        if self.case_cb.isChecked():
            from PySide6.QtGui import QTextDocument
            flags = QTextDocument.FindFlag.FindCaseSensitively
        return flags

    def find_next(self):
        text = self.find_input.text()
        if not text:
            return
        from PySide6.QtGui import QTextDocument
        flags = QTextDocument.FindFlag.FindCaseSensitively if self.case_cb.isChecked() else QTextDocument.FindFlag(0)
        found = self.editor.find(text, flags)
        if not found:
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            self.editor.setTextCursor(cursor)
            self.editor.find(text, flags)

    def replace_one(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == self.find_input.text():
            cursor.insertText(self.replace_input.text())
        self.find_next()

    def replace_all(self):
        text     = self.find_input.text()
        replace  = self.replace_input.text()
        if not text:
            return
        content  = self.editor.toPlainText()
        flags    = 0 if self.case_cb.isChecked() else re.IGNORECASE
        import re
        new_content = re.sub(re.escape(text), replace, content, flags=flags)
        count = len(re.findall(re.escape(text), content, flags=flags))
        self.editor.setPlainText(new_content)
        QMessageBox.information(self, "Replace All", f"{count} penggantian dilakukan.")


class NotepadClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file  = None
        self.is_modified   = False
        self._find_dialog  = None

        self._init_ui()
        self._update_title()
        self._update_status()

    def _init_ui(self):
        self.setWindowTitle("Notepad")
        self.resize(900, 620)

        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 13))
        self.setCentralWidget(self.editor)

        self.editor.textChanged.connect(self._on_text_changed)
        self.editor.cursorPositionChanged.connect(self._update_status)

        self._build_menubar()
        self._build_toolbar()
        self._build_statusbar()

    def _build_menubar(self):
        mb = self.menuBar()

        file_menu = mb.addMenu("File")

        act_new  = QAction("New",     self, shortcut=QKeySequence.StandardKey.New)
        act_open = QAction("Open…",   self, shortcut=QKeySequence.StandardKey.Open)
        act_save = QAction("Save",    self, shortcut=QKeySequence.StandardKey.Save)
        act_saveas = QAction("Save As…", self, shortcut=QKeySequence("Ctrl+Shift+S"))
        act_exit = QAction("Exit",    self, shortcut=QKeySequence.StandardKey.Quit)

        act_new.triggered.connect(self.new_file)
        act_open.triggered.connect(self.open_file)
        act_save.triggered.connect(self.save_file)
        act_saveas.triggered.connect(self.save_file_as)
        act_exit.triggered.connect(self.close)

        file_menu.addAction(act_new)
        file_menu.addAction(act_open)
        file_menu.addSeparator()
        file_menu.addAction(act_save)
        file_menu.addAction(act_saveas)
        file_menu.addSeparator()
        file_menu.addAction(act_exit)

        edit_menu = mb.addMenu("Edit")

        act_undo   = QAction("Undo",       self, shortcut=QKeySequence.StandardKey.Undo)
        act_redo   = QAction("Redo",       self, shortcut=QKeySequence.StandardKey.Redo)
        act_cut    = QAction("Cut",        self, shortcut=QKeySequence.StandardKey.Cut)
        act_copy   = QAction("Copy",       self, shortcut=QKeySequence.StandardKey.Copy)
        act_paste  = QAction("Paste",      self, shortcut=QKeySequence.StandardKey.Paste)
        act_selall = QAction("Select All", self, shortcut=QKeySequence.StandardKey.SelectAll)
        act_find   = QAction("Find & Replace…", self, shortcut=QKeySequence("Ctrl+H"))

        act_undo.triggered.connect(self.editor.undo)
        act_redo.triggered.connect(self.editor.redo)
        act_cut.triggered.connect(self.editor.cut)
        act_copy.triggered.connect(self.editor.copy)
        act_paste.triggered.connect(self.editor.paste)
        act_selall.triggered.connect(self.editor.selectAll)
        act_find.triggered.connect(self.open_find_replace)

        edit_menu.addAction(act_undo)
        edit_menu.addAction(act_redo)
        edit_menu.addSeparator()
        edit_menu.addAction(act_cut)
        edit_menu.addAction(act_copy)
        edit_menu.addAction(act_paste)
        edit_menu.addSeparator()
        edit_menu.addAction(act_selall)
        edit_menu.addSeparator()
        edit_menu.addAction(act_find)

        fmt_menu = mb.addMenu("Format")

        act_font = QAction("Font…", self)
        act_font.triggered.connect(self.choose_font)

        self.act_wordwrap = QAction("Word Wrap", self, checkable=True, checked=True)
        self.act_wordwrap.triggered.connect(self.toggle_word_wrap)
        self.editor.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        fmt_menu.addAction(act_font)
        fmt_menu.addAction(self.act_wordwrap)

        help_menu = mb.addMenu("Help")
        act_about = QAction("About", self)
        act_about.triggered.connect(self._show_about)
        help_menu.addAction(act_about)

    def _build_toolbar(self):
        tb = self.addToolBar("Main")
        tb.setMovable(False)
        tb.setIconSize(QSize(16, 16))

        def _btn(label, slot):
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            tb.addWidget(btn)
            return btn

        _btn("⬜ New",   self.new_file)
        _btn("📂 Open",  self.open_file)
        _btn("💾 Save",  self.save_file)
        tb.addSeparator()
        _btn("✂ Cut",   self.editor.cut)
        _btn("📋 Copy",  self.editor.copy)
        _btn("📌 Paste", self.editor.paste)
        tb.addSeparator()
        _btn("🔍 Find",  self.open_find_replace)

    def _build_statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Baris: 1 | Karakter: 0")
        self.status_bar.addWidget(self.status_label)

    def _update_title(self):
        name = os.path.basename(self.current_file) if self.current_file else "Untitled"
        mod  = " *" if self.is_modified else ""
        self.setWindowTitle(f"{name}{mod} — Notepad")

    def _update_status(self):
        cursor = self.editor.textCursor()
        line   = cursor.blockNumber() + 1
        chars  = len(self.editor.toPlainText())
        self.status_label.setText(f"Baris: {line} | Karakter: {chars}")

    def _on_text_changed(self):
        if not self.is_modified:
            self.is_modified = True
            self._update_title()
        self._update_status()

    def _confirm_discard(self) -> bool:
        """Return True if it's safe to discard current content."""
        if not self.is_modified:
            return True
        reply = QMessageBox.question(
            self, "Simpan perubahan?",
            "Dokumen belum disimpan. Simpan sekarang?",
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Save:
            return self.save_file()
        return reply == QMessageBox.StandardButton.Discard

    def new_file(self):
        if not self._confirm_discard():
            return
        self.editor.clear()
        self.current_file = None
        self.is_modified  = False
        self._update_title()

    def open_file(self):
        if not self._confirm_discard():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Buka File", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
            self.current_file = path
            self.is_modified  = False
            self._update_title()

    def save_file(self) -> bool:
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.is_modified = False
            self._update_title()
            return True
        return self.save_file_as()

    def save_file_as(self) -> bool:
        path, _ = QFileDialog.getSaveFileName(
            self, "Simpan File", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.current_file = path
            return self.save_file()
        return False

    def choose_font(self):
        ok, font = QFontDialog.getFont(self.editor.font(), self)
        if ok:
            self.editor.setFont(font)

    def toggle_word_wrap(self):
        if self.act_wordwrap.isChecked():
            self.editor.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        else:
            self.editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def open_find_replace(self):
        if self._find_dialog is None or not self._find_dialog.isVisible():
            self._find_dialog = FindReplaceDialog(self.editor, self)
        self._find_dialog.show()
        self._find_dialog.raise_()
        self._find_dialog.find_input.setFocus()

    def _show_about(self):
        QMessageBox.about(
            self, "About Notepad Clone",
            "<b>Notepad Clone</b><br>"
            "Dibuat dengan PySide6<br><br>"
            "Fitur: New/Open/Save, Undo/Redo, Cut/Copy/Paste,<br>"
            "Find & Replace, Font Dialog, Word Wrap, StatusBar."
        )

    def closeEvent(self, event):
        if self._confirm_discard():
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    window = NotepadClone()
    window.show()
    sys.exit(app.exec())
