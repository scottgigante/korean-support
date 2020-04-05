# -*- coding: utf-8 -*-
# Copyright 2012-2015 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>

# You can read about all available functions at:
# https://github.com/ttempe/chinese-support-addon/wiki/Edit-behavior
# Also, see the Python tutorial at http://docs.python.org/2/tutorial

from .config import korean_support_config as config
from .edit_functions import (
    get_any,
    has_field,
    setAll,
    silhouette,
    sound,
    hanja,
    english,
)


# Returns 1 if a translation was found in the dictionary, otherwise returns 0
def update_Meaning_fields(hangul, dico):
    # Update Meaning field only if empty
    m = ""
    if get_any(config.options["fields"]["meaning"], dico) == "":
        m = english(hangul)
        if not m:  # Translation is empty
            return 0
        setAll(config.options["fields"]["meaning"], dico, to=m)

    return 1


def update_Silhouette_fields(hangul, dico):
    m = silhouette(hangul)
    setAll(config.options["fields"]["silhouette"], dico, to=m)


# Returns 1 if a sound was added, otherwise returns 0
def update_Sound_fields(hangul, dico):
    # Update Sound field from Hangul field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if (
        has_field(config.options["fields"]["sound"], dico)
        and get_any(config.options["fields"]["sound"], dico) == ""
    ):
        s = sound(hangul)
        if s:
            setAll(config.options["fields"]["sound"], dico, to=s)
            return 1, 0  # 1 field filled, 0 errors
        return 0, 1
    return 0, 0


# Returns 1 if hanja was added, otherwise returns 0
def update_Hanja_fields(hangul, dico):
    # Update Sound field from Hangul field if non-empty (only if field actually
    # exists, as it implies downloading a soundfile from Internet)
    if get_any(config.options["fields"]["hanja"], dico) == "":
        h = hanja(hangul)
        if not h:
            return 0
        setAll(config.options["fields"]["hanja"], dico, to=h)

    return 1


def eraseFields(note):
    for fields in config.options["fields"].values():
        setAll(fields, note, to="")


def updateFields(note, currentField, fieldNames):
    fieldsCopy = dict(note)

    if currentField in config.options["fields"]["hangul"]:
        if fieldsCopy[currentField]:
            update_Meaning_fields(fieldsCopy[currentField], fieldsCopy)
            update_Sound_fields(fieldsCopy[currentField], fieldsCopy)
            update_Silhouette_fields(fieldsCopy[currentField], fieldsCopy)
            update_Hanja_fields(fieldsCopy[currentField], fieldsCopy)
        else:
            eraseFields(fieldsCopy)

    updated = False

    for f in fieldNames:
        if note[f] != fieldsCopy[f]:
            note[f] = fieldsCopy[f]
            updated = True

    return updated
