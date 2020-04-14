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
from .lib.navertts.tts import NaverTTS
from .config import korean_support_config


def download(text, lang="ko", service="Google TTS", attempts=3):
    slow = korean_support_config.options["tts_slow"]
    gender = korean_support_config.options["naver_tts_gender"]

    filename = [text, service[0], lang]
    if slow:
        filename.append("slow")
    if service == "NAVER Papago" and gender == "m":
        filename.append("male")
    filename, path = getFilename("_".join(filename), ".mp3")

    if os.path.exists(path) and os.stat(path).st_size > 0:
        return filename

    for attempt in range(attempts):
        try:
            if service == "Google TTS":
                tts = gTTS(text, lang=lang, slow=slow)
            elif service == "NAVER Papago":
                speed = "slow" if slow else "normal"
                tts = NaverTTS(text, lang=lang, speed=speed, gender=gender)
            else:
                raise ValueError("Unrecognized service {}".format(service))
            tts.save(path)
            return filename
        except:
            if attempt >= attempts - 1:
                raise
            else:
                pass


def getFilename(base, ext):
    filename = stripInvalidChars(base) + ext
    path = os.path.join(mw.col.media.dir(), filename)
    return (filename, path)


def stripInvalidChars(s):
    return re.sub('[\\/:\*?"<>\|]', "", s)
