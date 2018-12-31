# -*- coding: utf-8 -*-
# Copyright 2013 Chris Hatch <foonugget@gmail.com>
# Copyright 2014 Thomas TEMPE <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from time import sleep
import re

from anki.find import Finder
from aqt import mw
from aqt.utils import showInfo, askUser

from .config import korean_support_config as config
from .edit_behavior import (update_Sound_fields,
                            update_Meaning_fields,
                            update_Silhouette_fields)
from .edit_functions import has_field, get_any, cleanup


def no_html(txt):
    return re.sub("<.*?>", "", txt)


def fill_sounds():
    prompt = '''<div>This will update the <i>Sound</i> fields in the current
                deck, if they exist and are empty, using the selected speech
                engine.</div>
                <div>Please back-up your Anki deck first!</div>
                <div>(Please also note that there will be a 5 second delay
                between each sound request, to reduce burden on the server.
                This may therefore take a while.)</div>
                <div><b>Continue?</b></div>'''

    if not askUser(prompt):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_already_had_sound = 0
    d_success = 0
    d_failed = 0

    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict

        if has_field(config.options['fields']['sound'], note_dict) \
                and has_field(config.options['fields']['hangul'], note_dict):
            d_has_fields += 1

            hangul = get_any(config.options['fields']['hangul'], note_dict)

            if get_any(config.options['fields']['sound'], note_dict):
                d_already_had_sound += 1
            else:
                msg_string = ("<b>Processing:</b> {hangul:s}<br>"
                              "<b>Updated:</b> {d_success:d} notes<br>"
                              "<b>Failed:</b> {d_failed:d} notes").format(
                    hangul=cleanup(no_html(get_any(
                        config.options['fields']['hangul'], note_dict))),
                    d_success=d_success,
                    d_failed=d_failed)
                mw.progress.update(label=msg_string, value=d_scanned)
                s, f = update_Sound_fields(hangul, note_dict)
                d_success += s
                d_failed += f

                # write back to note from dict and flush
                for f in config.options['fields']['sound']:
                    if f in note_dict and note_dict[f] != note[f]:
                        note[f] = note_dict[f]
                note.flush()
                sleep(5)

    mw.progress.finish()
    msg_string = """
{d_success:d} new pronunciations downloaded

{d_failed:d} downloads failed

{have:d}/{d_has_fields:d} notes now have pronunciation
""".format(d_success=d_success, d_failed=d_failed,
           have=d_already_had_sound + d_success,
           d_has_fields=d_has_fields)
    if d_failed > 0:
        msg_string = msg_string + ("\n\nTTS is taken from an on-line source. "
                                   "It may not always be fully responsive. "
                                   "Please check your network connexion, "
                                   "or retry later.\n\nIf failures persist, "
                                   "please set Korean Support to debug mode "
                                   "and submit a bug report from the help "
                                   "menu.")
    showInfo(msg_string)

#############################################################


def fill_translation():
    if not(askUser(
            "<div>This will update the <i>Meaning</i> field in the current "
            "deck, if they exist and are empty.</div>"
            "<b>Learning tip:</b><div>Automatic dictionary lookup tends to "
            "produce very long text, often with multiple translations.</div>"
            "\n\n""<div>For more effective memorization, it's highly "
            "recommended to trim them down to just a few words, only one "
            "meaning, and possibly add some mnemonics.</div>\n\n"
            "<div>Dictionary lookup is simply meant as a way to save you time "
            "when typing; please consider editing each definition by hand when"
            " you're done.</div>\n\n"
            "<div>Please back-up your Anki deck first!</div>\n\n"
            "<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    d_failed = 0
    failed_hangul = []
    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict

        if has_field(config.options['fields']['meaning'], note_dict) and \
                has_field(config.options['fields']['hangul'], note_dict):
            d_has_fields += 1

            msg_string = ("<b>Processing:</b> {hangul:s}<br>"
                          "<b>Korean notes:</b> {has_fields:d}<br>"
                          "<b>Translated:</b> {filled:d}<br>"
                          "<b>Failed:</b> {failed:d}").format(
                hangul=cleanup(no_html(get_any(
                    config.options['fields']['hangul'], note_dict))),
                has_fields=d_has_fields,
                filled=d_success,
                failed=d_failed)
            mw.progress.update(label=msg_string, value=d_scanned)

            hangul = get_any(config.options['fields']['hangul'], note_dict)
            empty = len(
                get_any(config.options['fields']['meaning'], note_dict))
            empty += len(get_any(config.options['fields']
                                 ['english'], note_dict))
            empty += len(get_any(config.options['fields']
                                 ['german'], note_dict))
            empty += len(get_any(config.options['fields']
                                 ['french'], note_dict))
            if not(empty):
                result = update_Meaning_fields(hangul, note_dict)

                if result == 0:
                    d_failed += 1
                    if d_failed < 20:
                        failed_hangul += [
                            cleanup(no_html(get_any(
                                config.options['fields']['hangul'],
                                note_dict)))]
                else:
                    d_success += 1

            def write_back(fields):
                for f in fields:
                    if f in note_dict and note_dict[f] != note[f]:
                        note[f] = note_dict[f]
                return

            # write back to note from dict and flush
            write_back(config.options['fields']['meaning'])
            note.flush()

    msg_string = ("<b>Translation complete</b> <br>"
                  "<b>Korean notes:</b> {has_fields:d}<br>"
                  "<b>Translated:</b> {filled:d}<br>"
                  "<b>Failed:</b> {failed:d}").format(
        has_fields=d_has_fields,
        filled=d_success,
        failed=d_failed)
    if d_failed > 0:
        msg_string += ("\n\n<div>Translation failures may come either from "
                       "connection issues (if you're using an on-line "
                       "translation service), or because some words are not in"
                       " the dictionary (for local dictionaries).</div>")
        msg_string += "<div>The following notes failed: {}</div>".format(
            ", ".join(failed_hangul))
    mw.progress.finish()

    showInfo(msg_string)


############################################################

def fill_silhouette():
    if not(askUser("<div>This will update the <i>Silhouette</i> fields in the "
                   "current deck.</div>\n\n"
                   "<div>Please back-up your Anki deck first!</div>\n\n"
                   "<div><b>Continue?</b></div>")):
        return False

    query_str = "deck:current"
    d_scanned = 0
    d_has_fields = 0
    d_success = 0
    notes = Finder(mw.col).findNotes(query_str)
    mw.progress.start(immediate=True, min=0, max=len(notes))
    for noteId in notes:
        d_scanned += 1
        note = mw.col.getNote(noteId)
        note_dict = dict(note)      # edit_function routines require a dict
        if has_field(config.options['fields']['silhouette'], note_dict):
            d_has_fields += 1

            msg_string = ("<b>Processing:</b> {hangul:s}<br>"
                          "<b>Updated:</b> {filled:d}").format(
                hangul=cleanup(no_html(get_any(
                    config.options['fields']['hangul'], note_dict))),
                filled=d_success)
            mw.progress.update(label=msg_string, value=d_scanned)

            hangul = get_any(config.options['fields']['hangul'], note_dict)

            # Update Silhouette
            update_Silhouette_fields(hangul, note_dict)

            # write back to note from dict and flush
            for f in config.options['fields']['silhouette']:
                if f in note_dict and note_dict[f] != note[f]:
                    note[f] = note_dict[f]
                    d_success += 1
            note.flush()

    msg_string = ("<b>Update complete!</b> {hangul:s}<br>"
                  "<b>Updated:</b> {filled:d}").format(
        hangul=cleanup(no_html(get_any(
            config.options['fields']['hangul'], note_dict))),
        filled=d_success)
    mw.progress.finish()
    showInfo(msg_string)
