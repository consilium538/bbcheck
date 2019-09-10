from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from startup import Ui_StartupDialog
from bboxshow import BBoxShow


class StartupDialog(QDialog):
    def __init__(self):
        super(StartupDialog, self).__init__()
        self.statedict = {
            'imgdir': './img',
            'origdir': './orig',
            'changedir': './checked',
        }
        # self.statedict = dict()
        self.workwindow = None

        # Setup UI from QT Designer
        self.ui = Ui_StartupDialog()
        self.ui.setupUi(self)

        # Make some local modifications
        self.ui.ImgDirButton.clicked.connect(self.imgdirselect)
        self.ui.OrigAnnoDirButton.clicked.connect(self.origdirselect)
        self.ui.CheckedAnnoDirButton.clicked.connect(self.changedirselect)
        self.ui.StartButton.clicked.connect(self.startchecking)

    def imgdirselect(self):
        self.statedict['imgdir'] = str(QFileDialog.getExistingDirectory(None, "Select Image Directory", './'))
        self.ui.ImgDirButton.setText(f'Image Directory\n{self.statedict["imgdir"]}')

    def origdirselect(self):
        self.statedict['origdir'] = str(QFileDialog.getExistingDirectory(None, "Select Original Annotation Directory", './'))
        self.ui.OrigAnnoDirButton.setText(f'Original Annotation Directory\n{self.statedict["origdir"]}')

    def changedirselect(self):
        self.statedict['changedir'] = str(QFileDialog.getExistingDirectory(None, "Select Changed Annotation Directory", './'))
        self.ui.CheckedAnnoDirButton.setText(f'Changed Annotation  Directory\n{self.statedict["changedir"]}')

    def startchecking(self):
        if 'imgdir' not in self.statedict or 'origdir' not in self.statedict or 'changedir' not in self.statedict:
            QMessageBox.warning(None, "Directory Not speficied",
                                "All directory MUST be set.")
            return
        if self.workwindow:
            del self.workwindow
        self.workwindow = BBoxShow(self)
        self.workwindow.show()
        self.hide()

