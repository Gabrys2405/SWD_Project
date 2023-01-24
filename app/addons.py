from PySide6 import QtGui

def get_default_font() -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(int(font.pointSize() * 1))
    return font

def converter__str_to_bool(s: str) -> bool:
    if s == "True":
        return True
    if s == "False":
        return False
    return float(s) != 0