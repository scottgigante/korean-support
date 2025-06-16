# -*- coding: utf-8 -*-
# Copyright 2012, 2013 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import mw, gui_hooks
import aqt

from .config import korean_support_config as config
from .edit_behavior import updateFields


class EditManager:
    def __init__(self):
        gui_hooks.editor_did_init_buttons.append(self.setupButton)
        gui_hooks.editor_did_load_note.append(self.updateButton)
        gui_hooks.editor_did_unfocus_field.append(self.onFocusLost)
        gui_hooks.editor_state_did_change.append(self.onStateChange)

    def setupButton(self, buttons, editor):
        self.editor = editor
        self.buttonOn = False

        button = editor.addButton(
            icon=None,
            cmd="koreanSupport",
            func=self.onToggle,
            tip="Korean Support",
            label="<b>한글</b>",
            id="koreanSupport",
            toggleable=True,
        )

        buttons.append(button)

    def onToggle(self, editor):
        self.buttonOn = not self.buttonOn

        mid = str(editor.note.note_type()["id"])

        if self.buttonOn and mid not in config.options["enabledModels"]:
            config.options["enabledModels"].append(mid)
        elif not self.buttonOn and mid in config.options["enabledModels"]:
            config.options["enabledModels"].remove(mid)

        config.save()
        self.updateButton(editor)

    def onStateChange(self, editor, new_state, old_state):
        if old_state is aqt.editor.EditorState.INITIAL:
            self.updateButton(editor)
            self.buttonOn = (
                str(editor.note.note_type()["id"]) in config.options["enabledModels"]
            )

    def updateButton(self, editor):
        enabled = str(editor.note.note_type()["id"]) in config.options["enabledModels"]

        # Styles taken from https://github.com/Gustaf-C/anki-chinese-support-3/blob/main/chinese/edit.py#L92-L112
        if enabled:
            editor.web.eval(
                """
                document.getElementById("koreanSupport").classList.add("active");
                document.getElementById("koreanSupport").style.setProperty("--button-bg", "var(--button-primary-bg)");
                document.getElementById("koreanSupport").style.setProperty("--button-gradient-start", "var(--button-primary-gradient-start)");
                document.getElementById("koreanSupport").style.setProperty("--button-gradient-end", "var(--button-primary-gradient-end)");
                """
            )
        else:
            editor.web.eval(
                """
                document.getElementById("koreanSupport").classList.remove("active");
                document.getElementById("koreanSupport").style.setProperty("--button-bg", "");
                document.getElementById("koreanSupport").style.setProperty("--button-gradient-start", "");
                document.getElementById("koreanSupport").style.setProperty("--button-gradient-end", "");
                """
            )

    def onFocusLost(self, _, note, index):
        if not self.buttonOn:
            return False

        allFields = mw.col.models.field_names(note.note_type())
        field = allFields[index]

        if updateFields(note, field, allFields):
            if index == len(allFields) - 1:
                self.editor.loadNote(focusTo=index)
            else:
                self.editor.loadNote(focusTo=index + 1)

        return False


def appendToneStyling(editor):
    js = "var css = document.styleSheets[0];"

    for line in editor.note.note_type()["css"].split("\n"):
        if line.startswith(".tone"):
            js += 'css.insertRule("{}", css.cssRules.length);'.format(line.rstrip())

    editor.web.eval(js)


gui_hooks.editor_did_load_note.append(appendToneStyling)

EditManager()
