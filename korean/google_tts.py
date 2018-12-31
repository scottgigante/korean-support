# -*- coding: utf-8 -*-
# Copyright 2012 Roland Sieker <ospalh@gmail.com>o
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Pu Anlai
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>
# Inspiration: Tymon Warecki
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


import os
import re

from aqt import mw

from .lib.gtts.tts import gTTS


def get_word_from_google(source, lang='ko', attempts=3):
    filename, path = getFilename('_'.join([source, 'G', lang]), '.mp3')

    if os.path.exists(path) and os.stat(path).st_size > 0:
        return filename

    for attempt in range(attempts):
        try:
            tts = gTTS(source, lang=lang)
            tts.save(path)
            break
        except Exception as e:
            error = str(e)
            tts = None
    if tts is not None:
        return filename
    else:
        raise RuntimeError(error)


def getFilename(base, ext):
    filename = stripInvalidChars(base) + ext
    path = os.path.join(mw.col.media.dir(), filename)
    return (filename, path)


def stripInvalidChars(s):
    return re.sub('[\\/:\*?"<>\|]', '', s)
