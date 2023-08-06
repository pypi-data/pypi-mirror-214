
import PyQt5.QtWidgets

# Ensure PyQt is initialised
app = PyQt5.QtWidgets.QApplication.instance()
if app is None:
    app = PyQt5.QtWidgets.QApplication([])


from .main import MainWin as VTable
