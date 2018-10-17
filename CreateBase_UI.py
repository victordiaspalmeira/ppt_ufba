# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateBase_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_Base(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(312, 171)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelInsert = QtWidgets.QLabel(Dialog)
        self.labelInsert.setObjectName("labelInsert")
        self.verticalLayout.addWidget(self.labelInsert)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelName = QtWidgets.QLabel(Dialog)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout_2.addWidget(self.labelName)
        self.lineEditTitle = QtWidgets.QLineEdit(Dialog)
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.horizontalLayout_2.addWidget(self.lineEditTitle)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelName_2 = QtWidgets.QLabel(Dialog)
        self.labelName_2.setObjectName("labelName_2")
        self.horizontalLayout_3.addWidget(self.labelName_2)
        self.lineEditAuthor = QtWidgets.QLineEdit(Dialog)
        self.lineEditAuthor.setObjectName("lineEditAuthor")
        self.horizontalLayout_3.addWidget(self.lineEditAuthor)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.labelName.setBuddy(self.lineEditTitle)
        self.labelName_2.setBuddy(self.lineEditAuthor)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Criação de Base"))
        self.labelInsert.setText(_translate("Dialog", "Insira as informações da base:"))
        self.labelName.setText(_translate("Dialog", "Título:     "))
        self.labelName_2.setText(_translate("Dialog", "Autor(a):"))
        self.checkBox.setText(_translate("Dialog", "Incluir Classes"))
        self.radioButton.setText(_translate("Dialog", "Primeira Coluna"))
        self.radioButton_2.setText(_translate("Dialog", "Última Coluna"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

