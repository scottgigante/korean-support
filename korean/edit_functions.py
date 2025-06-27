# -*- coding: utf-8 -*-
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from functools import reduce
import re
import os
from aqt.utils import showInfo
import sys
import traceback
import types


# Monkey patch for other systems that might crash trying to import non existing library
class FakePkgResources(types.ModuleType):
    def __getattr__(self, name):
        raise ModuleNotFoundError("pkg_resources is not available")


sys.modules["pkg_resources"] = FakePkgResources("pkg_resources")


from .lib import kengdic
from .lib.krdict.src import krdict
from . import tts
from .config import korean_support_config

# from .microsofttranslator import Translator as MSTranslator

# Essential Edit functions
##################################################################
#
# You may call any of these functions from the edit_behavior.py file.


def no_color(text):
    "Remove tone color info and other HTML pollutions"
    if text is None:
        return ""
    text = text.replace(r"&nbsp;", "")
    text = no_hidden(text)
    # remove color info
    text = re.sub(r"<font color=.*?>(.*?)</font>", r"\1", text)
    # remove Anki1 Pinyin Toolkit coloring
    text = re.sub(r"<span style=.*?>(.*?)</span>", r"\1", text)
    return text


def silhouette(hangul):
    """Replaces each Chinese character by a blank space.

    Eg: 以A为B -> _A_B
    Eg: 哈密瓜 -> _ _ _
    """

    def insert_spaces(p):
        r = ""
        for i in p.group(0):
            r += i + " "
        return r[:-1]

    hangul_unicode = "[\u1100-\u11ff|\uac00-\ud7af|\u3130-\u318f]"
    hangul = re.sub("{}+".format(hangul_unicode), insert_spaces, hangul)
    txt = re.sub(hangul_unicode, "_", hangul)
    return txt


def no_hidden(text):
    """Remove hidden keyword string"""
    return re.sub(r"<!--.*?-->", "", text)


def explanation(text):
    if korean_support_config.options["krdictApiKey"] == "":
        if korean_support_config.options["debug"]:
            print("No krdictApiKey found")
        return ""
    krdict.set_key(korean_support_config.options["krdictApiKey"])
    response = krdict.search(query=text, raise_api_errors=True)
    data = response.data
    if data.total_results > 0:
        matching_results = [r for r in data.results if r.word == text]

        formatted_sections = []
        for result in matching_results:
            origin = result.origin or "(no origin)"
            definitions = result.definitions
            definitions_text = "<br>".join(
                f"{i+1}. {d.definition}" for i, d in enumerate(definitions)
            )
            section = f"{origin}<br>{definitions_text}"
            formatted_sections.append(section)

        return "<br><br>".join(formatted_sections)
    else:
        return ""


def translate_local(text):
    """Translate using local dictionary."""
    words = db.search(korean=text)
    return words


def english(hangul):
    """Get English from local dictionary
    Eg: '사랑' becomes 'Love'
    """
    words = translate_local(hangul)
    english = [word.english for word in words if word.english is not None]
    res = "\n<br>".join(english)
    return res


def hanja(hangul):
    """Get Hanja from local dictionary
    Eg: '일월' becomes '一月'
    """
    words = translate_local(hangul)
    hanja = [word.hanja for word in words if word.hanja is not None]
    res = "，".join(hanja)
    return res


def translate(text, from_lang="ko", to_lang=None, progress_bar=True):
    """Translate to a different language.
    Only installed dictionaries can be used.

    to_lang possible values : "local_en"
    TODO: or a 2-letter ISO language code for MS Translate

    if to_lang is unspecified, the default language will be used.
    if progress_bar is True, then will display a progress bar.
    """
    global MS_translator_object
    text = cleanup(text)
    if "" == text:
        return ""
    if to_lang is None:
        to_lang = korean_support_config.options["dictionary"]
        if "None" == to_lang:
            return ""
    if to_lang == "local_en":  # Local dict
        return translate_local(text)
    else:  # Ms translate
        raise NotImplementedError(
            "{} translation not currently supported".format(to_lang)
        )
    #     ret = ""
    #     if progress_bar:
    #         mw.progress.start(label="MS Translator lookup", immediate=True)
    #     if None == MS_translator_object:
    #         MS_translator_object = MSTranslator("chinese-support-add-on",
    #                       "Mh+X5YY17LZZ8rO9hzJXYD3I02V3E+ltItF15ep7qG8=")
    #     try:
    #         ret = MS_translator_object.translate(text, to_lang)
    #     except:
    #         pass
    #     if "ArgumentException:" == ret[:18]:
    #         #Token has probably expired
    #         ret=""
    #     if progress_bar:
    #         mw.progress.finish()
    #     return ret


def cleanup(txt):
    """Remove all HTML, tags, and others."""
    if not txt:
        return ""
    txt = re.sub(r"<.*?>", "", txt, flags=re.S)
    txt = txt.replace("&nbsp;", " ")
    txt = re.sub(r"^\s*", "", txt)
    txt = re.sub(r"\s*$", "", txt)
    # txt = re.sub(r"[\s+]", " ", txt)
    txt = re.sub(r"\{\{c[0-9]+::(.*?)(::.*?)?\}\}", r"\1", txt)
    return txt


def sound(text, source=None):
    """
    Returns sound tag for a given Hangul string.

    If the sound does not already exist in the media directory, then
    attempt to obtain it from the specified source.
    if the specified source is omitted, use the one selected in the
    tools menu.
    If it fails (eg: no network connexion while trying to retrieve
    speech from Google TTS), return empty string.

    Does not work with pinyin or other transcriptions.

    Source is either the TTS speech engine name.
    If empty, taking the one from the menu.
    """
    text = cleanup(text)
    if source is None:
        source = korean_support_config.options["speech"]

    text = no_sound(text)
    text = re.sub("<.*?>", "", text)
    if "" == text:
        return ""

    if source in ["Google TTS", "NAVER Papago"]:
        try:
            return "[sound:{}]".format(tts.download(text, "ko", service=source))
        except Exception as e:
            if korean_support_config.options["debug"]:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                showInfo(
                    "{} failed.\n{}".format(
                        source,
                        "".join(
                            traceback.format_exception(
                                exc_type, exc_value, exc_traceback
                            )
                        ),
                    )
                )
            return ""
    else:
        return ""


def get_any(fields, dico):
    """Get the 1st valid field from a list
    Scans all field names listed as "fields", to find one that exists,
    then returns its value.
    If none exists, returns an empty string.

    Case-insensitive.
    """
    for f in fields:
        for k, v in dico.items():
            try:
                if str(f.lower()) == str(k.lower()):
                    return dico[k]
            except:
                pass
    return ""


def setAll(fields, note, to):
    fields = [f.lower() for f in fields]

    for f in note.keys():
        if f.lower() in fields:
            note[f] = to


def has_field(fields, dico):
    """
    Check if one of the named fields exists in the field list

    Case-insensitive.
    """
    for d, v in dico.items():
        for f in fields:
            try:
                if str(f.lower()) == str(d.lower()):
                    return True
            except:
                pass
    return False


def no_sound(text):
    """
    Removes the [sound:xxx.mp3] tag that's added by Anki when you record
    sound into a field.

    If you don't remove it before taking data from one field to another,
    it will likely be duplicated, and the sound will play twice.
    """
    return re.sub(r"\[sound:.*?]", "", text)


# Extra support functions and parameters
##################################################################

MS_translator_object = None

# monkey patch missing pkg_resources
kengdic.Kengdic.__sqlite_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "lib",
    "kendic",
    "kengdic",
    "sqlite",
    "kengdic_2011.sqlite",
)
db = kengdic.Kengdic()


def extract_sound_tags(text):
    sound_tags = re.findall(r"\[sound:.*?\]", text)
    if [] == sound_tags:
        sound_tags = ""
    else:
        sound_tags = reduce(lambda a, b: a + b, sound_tags)
    nosound = re.sub(r"\[sound:.*?\]", r"", text)
    return nosound, sound_tags


def add_diaeresis(text):
    try:
        return re.sub("v", "ü", text)
    except:
        return ""
