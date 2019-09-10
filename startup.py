# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startup.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StartupDialog(object):
    def setupUi(self, StartupDialog):
        StartupDialog.setObjectName("StartupDialog")
        self.gridLayout = QtWidgets.QGridLayout(StartupDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.ImgDirButton = QtWidgets.QPushButton(StartupDialog)
        self.ImgDirButton.setObjectName("ImgDirButton")
        self.gridLayout.addWidget(self.ImgDirButton, 0, 0, 1, 1)
        self.OrigAnnoDirButton = QtWidgets.QPushButton(StartupDialog)
        self.OrigAnnoDirButton.setObjectName("OrigAnnoDirButton")
        self.gridLayout.addWidget(self.OrigAnnoDirButton, 1, 0, 1, 1)
        self.CheckedAnnoDirButton = QtWidgets.QPushButton(StartupDialog)
        self.CheckedAnnoDirButton.setObjectName("CheckedAnnoDirButton")
        self.gridLayout.addWidget(self.CheckedAnnoDirButton, 2, 0, 1, 1)
        self.StartButton = QtWidgets.QPushButton(StartupDialog)
        self.StartButton.setObjectName("StartButton")
        self.gridLayout.addWidget(self.StartButton, 3, 0, 1, 1)

        self.retranslateUi(StartupDialog)
        QtCore.QMetaObject.connectSlotsByName(StartupDialog)

    def retranslateUi(self, StartupDialog):
        _translate = QtCore.QCoreApplication.translate
        StartupDialog.setWindowTitle(_translate("StartupDialog", "Dialog"))
        self.CheckedAnnoDirButton.setText(_translate("StartupDialog", "Checked Annotation Directory\n"
                                                                      ""))
        self.ImgDirButton.setText(_translate("StartupDialog", "Image Directory\n"
                                                              ""))
        self.OrigAnnoDirButton.setText(_translate("StartupDialog", "Original Annotation Directory\n"
                                                                   ""))
        self.StartButton.setText(_translate("StartupDialog", "Start!"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    StartupDialog = QtWidgets.QDialog()
    ui = Ui_StartupDialog()
    ui.setupUi(StartupDialog)
    StartupDialog.show()
    sys.exit(app.exec_())