import os
import re
import string


def pathleaf(x):
    return os.path.basename(os.path.normpath(x))


def cleanup(x):
    chars = re.escape(string.punctuation)
    x = x.replace("_", " ")
    return re.sub(r"[" + chars + "]", "", x)
