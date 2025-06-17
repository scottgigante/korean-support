import sys
from unittest.mock import MagicMock


sys.modules["anki"] = MagicMock()
sys.modules["anki.hooks"] = MagicMock()
sys.modules["anki.stdmodels"] = MagicMock()
sys.modules["anki.lang"] = MagicMock()
sys.modules["anki.find"] = MagicMock()
sys.modules["aqt"] = MagicMock()
sys.modules["aqt.qt"] = MagicMock()
sys.modules["aqt.utils"] = MagicMock()
sys.modules["korean.lib.gtts"] = MagicMock()
sys.modules["korean.lib.gtts.tts"] = MagicMock()
sys.modules["korean.lib.navertts"] = MagicMock()
sys.modules["korean.lib.navertts.tts"] = MagicMock()
sys.modules["korean.lib.kengdic"] = MagicMock()
sys.modules["korean.lib.krdict.src"] = MagicMock()
sys.modules["korean.ui"] = MagicMock()
sys.modules["korean.lib"] = MagicMock()
