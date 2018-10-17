# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogAskFechar.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogAsk(object):
    def setupUi(self, DialogAsk):
        DialogAsk.setObjectName("DialogAsk")
        DialogAsk.resize(280, 90)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DialogAsk)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelAsk = QtWidgets.QLabel(DialogAsk)
        self.labelAsk.setObjectName("labelAsk")
        self.verticalLayout.addWidget(self.labelAsk)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogAsk)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DialogAsk)
        self.buttonBox.accepted.connect(DialogAsk.accept)
        self.buttonBox.rejected.connect(DialogAsk.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAsk)

    def retranslateUi(self, DialogAsk):
        _translate = QtCore.QCoreApplication.translate
        DialogAsk.setWindowTitle(_translate("DialogAsk", "Fechar Base"))
        self.labelAsk.setText(_translate("DialogAsk", "Dados não salvos serão perdidos. Deseja Continuar?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogAsk = QtWidgets.QDialog()
    ui = Ui_DialogAsk()
    ui.setupUi(DialogAsk)
    DialogAsk.show()
    sys.exit(app.exec_())

