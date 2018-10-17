# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Prep_Final.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import sys
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets
from CreateBase_UI import Ui_Dialog_Base
from Classe_UI import Ui_Dialog_Classe
from Fechar_UI import Ui_DialogAsk
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import os, os.path, codecs, csv
from tokenizer import LemmaTokenizer, StemTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

numpy.set_printoptions(threshold=sys.maxsize)

class Ui_MainWindow(object):
    def initSignals(self):
        #Só pode ser executada apenas uma vez!!!
        #Inicializa os signals
        self.actionCriar.triggered.connect(self.criarBase)
        self.actionFechar.triggered.connect(self.fechaBase)
        self.actionCarregar_arquivo_s.triggered.connect(self.abrirArquivos)
        self.actionSalvar.triggered.connect(self.generate_external_corpus)
        
        self.pushButtonExecute.clicked.connect(self.preProcess)
        self.flag = False
        
    def init(self):
        #Configura o menu para apresentação inicial
        self.actionSalvar.setDisabled(True)
        self.actionFechar.setDisabled(True)
        self.actionCarregar_arquivo_s.setDisabled(True)
        
        #Inicalizas as varíaveis internas
        self.instCount = None
        self.termCount = None
        self.corpus = list()
        self.class_list = list()
        self.stem = False
        self.stopWords = False
        self.lema = False
        
        self.title = "Nenhum"
        self.author = "Nenhum"
        self.classe = False
        
        self.bagOfWords = False
        self.TfIdf = False
        
        self.row_count = 0
        
    def preProcess(self):
        self.stem = self.checkBox_3.isChecked()
        self.stopWords = self.checkBox.isChecked()
        self.lema = self.checkBox_2.isChecked()
        
        self.bagOfWords = self.radioButton.isChecked()
        self.TfIdf = self.radioButton_2.isChecked()
        
        #Parte de seleção de linguagem removida pois os algoritmos só funcionam bem pra inglês
        #self.lang = self.comboBoxIdioma.currentIndex()
        #if self.lang == 0:
        #    self.lang = 'portuguese'
        #if self.lang == 1:
        #    self.lang = 'english'
        
        #Checagem
        stopWords = None
        tokens = None
        v_min = 1
        v_max = int(self.comboBox.currentIndex()) + 1
        
        if(self.stem):
            tokens = StemTokenizer('english')
        if(self.stopWords):
            stopWords = 'english'
        if(self.lema):
            tokens = LemmaTokenizer()
                
        vectorizer = CountVectorizer(tokenizer = tokens,
                                     stop_words = stopWords,
                                     ngram_range =(v_min,v_max))
        
        X = vectorizer.fit_transform(self.corpus)
        self.feats = vectorizer.get_feature_names()
        
        if(self.TfIdf):
            transformer = TfidfTransformer(smooth_idf=False)    
            tfidf = transformer.fit_transform(X.toarray())
            self.OUTPUT = tfidf.toarray()
                        
        if(self.bagOfWords):
            self.OUTPUT = X.toarray()                                

        self.textEditDict.setText(str(self.feats))
        self.textEditOutput.setText(str(self.OUTPUT))

        self.labelNumTerms.setText(str(len(self.feats)))
        
    def generate_external_corpus(self):
        #pega o nome e o formato desejado do arquivo
        file_name = QFileDialog.getSaveFileName(MainWindow, "Salvar Arquivo", "", "ARFF (*.arff);;CSV (*.csv);;TXT (*.txt)")
        text_file = open(file_name[0], "w")
        string_output = ""
        
        if file_name[1] == 'ARFF (*.arff)':
            string_output = string_output + "%Title of Database: "+ str(self.title) + "\n"
            string_output = string_output + "%Author: " + str(self.author) + "\n\n"
            string_output = string_output + "@relation " + str(self.title) + "\n"
            string_output = string_output + "\n"
            
            if(self.classe):
                if(self.p_coluna):
                    #Inserir atributo na primeira coluna caso exista classe
                    string_output = string_output + '@attribute "' + "class" + '" real' + "\n"
                
            for x in range(len(self.feats)):
                string_output = string_output + '@attribute "' + self.feats[x] + '" real' + "\n"
                
            if(self.classe):
                if(not self.p_coluna):
                    #Inserir atributo na primeira coluna caso exista classe
                    string_output = string_output + '@attribute "' + "class" + '" real' + "\n"
            string_output = string_output + "\n"
            
            string_output = string_output + "@data\n"
            
            for x in range(len(self.OUTPUT)):
                if(self.classe):
                    if(self.p_coluna):
                        txt_classe = str(self.tableWidget.item(x, 0).text())
                        string_output = string_output + txt_classe + ", "
                        
                for y in range(len(self.OUTPUT[x])):
                    string_output = string_output + str(self.OUTPUT[x][y])
                    if (y < len(self.OUTPUT[x])-1):
                        string_output = string_output + ', '
                        
                if(self.classe):
                    if(not self.p_coluna):
                        txt_classe = str(self.tableWidget.item(x, 0).text())
                        string_output = string_output + ", " + txt_classe                
                string_output = string_output + "\n"
                
            text_file.write(string_output)
            text_file.close()
            return
        
        if file_name[1] == 'TXT (*.txt)':
            for x in range(len(self.OUTPUT)):
                if(self.classe):
                    if(self.p_coluna):
                        txt_classe = str(self.tableWidget.item(x, 0).text())
                        string_output = string_output + txt_classe + ", "
                for y in range(len(self.OUTPUT[x])):
                    string_output = string_output + str(self.OUTPUT[x][y])
                    if (y < len(self.OUTPUT[x])-1):
                        string_output = string_output + ', '
                        
                if(self.classe):
                    if(not self.p_coluna):
                        txt_classe = str(self.tableWidget.item(x, 0).text())
                        string_output = string_output + ", " + txt_classe
                string_output = string_output + "\n"
                
            text_file.write(string_output)
            text_file.close()
            return            
        
        if file_name[1] == 'CSV (*.csv)':
            fieldnames = self.feats
            if(self.classe):
                if(self.p_coluna):
                    fieldnames.insert(0, "class")
                else:
                    fieldnames.append("class")
            writer = csv.DictWriter(text_file, fieldnames=fieldnames, lineterminator = '\n')
            writer.writeheader()
            for x in range(len(self.OUTPUT)):
                out = self.OUTPUT[x]
                if(self.classe):
                    if(self.p_coluna):
                        out = numpy.insert(out, 0, int(self.tableWidget.item(x, 0).text()))
                    else:
                        out = numpy.append(out, int(self.tableWidget.item(x, 0).text()))            
                combination = zip(fieldnames, out)
                instance_dict = dict(combination)
                print(instance_dict)
                writer.writerow(instance_dict)
            
            text_file.close()
            return
            
    def criarBase(self):
        dialogBase = QtWidgets.QDialog()
        fileDialog = Ui_Dialog_Base()
        fileDialog.setupUi(dialogBase)
            
        fileDialog.buttonBox.accepted.connect(lambda: self.setInfoBase(fileDialog.lineEditTitle.text(), fileDialog.lineEditAuthor.text(), fileDialog.checkBox.isChecked(), fileDialog.radioButton.isChecked()))
        fileDialog.buttonBox.rejected.connect(dialogBase.reject)

        dialogBase.exec_()
        return
    
    def internalFlag(self, var):
        self.flag = var
        return
    
    def fechaBase(self):
        dialogAsk = QtWidgets.QDialog()
        fileDialog = Ui_DialogAsk()
        fileDialog.setupUi(dialogAsk)
        
        fileDialog.buttonBox.accepted.connect(lambda: self.internalFlag(True))
        fileDialog.buttonBox.rejected.connect(lambda: self.internalFlag(False))
        
        dialogAsk.exec_()

        if(self.flag):
            self.internalFlag(False)
            #Limpa a lista de corpus, e resta os valores nas labels
            self.init()
            self.corpus = None
            self.tableWidget.setRowCount(0)
            self.row_count = 0
            
            self.label_title.setText("Nenhum")
            self.label_author.setText("Nenhum")
            self.labelNumInst.setText("0")
            self.labelNumTerms.setText("0")

        return
        
    def setInfoBase(self, title, author, classe, coluna):
        #Guarda as informações da base
        self.title = title
        self.author = author
        self.classe = classe #booleano
        self.p_coluna = coluna #true -> primeira coluna, false -> ultima coluna
        self.instCount = 0
        self.termCount = 0

        self.actionSalvar.setDisabled(False)
        self.actionFechar.setDisabled(False)
        self.actionCarregar_arquivo_s.setDisabled(False)
        #Altera os valores nas respectivas labels
        self.label_title.setText(self.title)        
        self.label_author.setText(self.author)
        
        return
    
    def abrirArquivos(self):
        try:
            file_path = QFileDialog.getOpenFileNames(MainWindow, "Abrir Arquivo(s)")
            if(str(file_path) == "([], '')"):
                print("Não abriu nada.")
                return
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Erro ao abrir arquivos.')
            return
        
        #Input da classe dos arquivos, caso opção marcada
        if(self.classe):
            dialogClasse = QtWidgets.QDialog()
            fileDialog = Ui_Dialog_Classe()
            fileDialog.setupUi(dialogClasse)
                
            fileDialog.buttonBox.accepted.connect(lambda: self.setClasse(fileDialog.lineEdit.text()))
            fileDialog.buttonBox.rejected.connect(lambda: self.setClasse(""))
            
            dialogClasse.exec_()      
        
        
        # Lista que irá receber o nome de cada arquivo aberto
        if(self.classe):
            if (self.txt_classe == ""):
                print("sem classe")
                return
        else:
            print("Classe: " + str(self.classe))
            
        fileList = list()
        for file in file_path[0]:
            # Loop para passar os nomes para a lista 
            if file == '':
                break
            else:
                aux_file = ''.join(file)
                fileList.append(aux_file)
                
        for file in fileList:
            #Colocando o conteúdo dos arquivos no corpus
            with codecs.open(file, 'r', encoding='utf8') as f:
                
                try:
                    raw = f.read()
                    self.corpus.append(raw)
                    self.instCount = self.instCount + 1
                    f.close()
                except:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('O seguinte arquivo não pode ser aberto: \n' + str(file))
                    error_dialog.exec_()
                    return
            
                
        for file in fileList:
            #Preencher tabela com o nome dos arquivos
            self.tableWidget.setRowCount(self.instCount)
            if(self.classe):
                self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(str(self.txt_classe)))
            self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(str(file)))
            self.row_count = self.row_count + 1
        
        self.labelNumInst.setText(str(self.instCount))
        
    def setClasse(self, classe):
        self.txt_classe = classe
        self.class_list.append(classe) #adiciona classe á lista de classes
        print(self.class_list)
        return
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(527, 527)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.tabOption = QtWidgets.QTabWidget(self.centralwidget)
        self.tabOption.setObjectName("tabOption")
        self.tabParameters = QtWidgets.QWidget()
        self.tabParameters.setObjectName("tabParameters")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tabParameters)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.tabParameters)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_3 = QtWidgets.QCheckBox(self.tabParameters)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout.addWidget(self.checkBox_3)
        self.checkBox_2 = QtWidgets.QCheckBox(self.tabParameters)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.tabOption.addTab(self.tabParameters, "")
        self.tabModel = QtWidgets.QWidget()
        self.tabModel.setObjectName("tabModel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tabModel)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.tabModel)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.tabModel)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_2.addWidget(self.radioButton_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.tabModel)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.comboBox = QtWidgets.QComboBox(self.tabModel)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_6.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.tabOption.addTab(self.tabModel, "")
        self.horizontalLayout_7.addWidget(self.tabOption)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_7.addWidget(self.line_2)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_2.addWidget(self.label_title)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_author = QtWidgets.QLabel(self.centralwidget)
        self.label_author.setObjectName("label_author")
        self.gridLayout.addWidget(self.label_author, 0, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.labelNumInst = QtWidgets.QLabel(self.centralwidget)
        self.labelNumInst.setObjectName("labelNumInst")
        self.horizontalLayout_3.addWidget(self.labelNumInst)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.labelNumTerms = QtWidgets.QLabel(self.centralwidget)
        self.labelNumTerms.setObjectName("labelNumTerms")
        self.horizontalLayout_8.addWidget(self.labelNumTerms)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.tabBase = QtWidgets.QTabWidget(self.centralwidget)
        self.tabBase.setObjectName("tabBase")
        self.tabDict = QtWidgets.QWidget()
        self.tabDict.setObjectName("tabDict")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.tabDict)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.textEditDict = QtWidgets.QTextEdit(self.tabDict)
        self.textEditDict.setObjectName("textEditDict")
        self.horizontalLayout_9.addWidget(self.textEditDict)
        self.tabBase.addTab(self.tabDict, "")
        self.tabTab = QtWidgets.QWidget()
        self.tabTab.setObjectName("tabTab")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.tabTab)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.textEditOutput = QtWidgets.QTextEdit(self.tabTab)
        self.textEditOutput.setObjectName("textEditOutput")
        self.horizontalLayout_10.addWidget(self.textEditOutput)
        self.tabBase.addTab(self.tabTab, "")
        self.verticalLayout_6.addWidget(self.tabBase)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout_5.addWidget(self.tableWidget)
        self.verticalLayout_4.addLayout(self.verticalLayout_5)
        self.pushButtonExecute = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonExecute.setObjectName("pushButtonExecute")
        self.verticalLayout_4.addWidget(self.pushButtonExecute)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 527, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuBase = QtWidgets.QMenu(self.menuMenu)
        self.menuBase.setObjectName("menuBase")
        self.menuTexto = QtWidgets.QMenu(self.menuMenu)
        self.menuTexto.setObjectName("menuTexto")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCriar = QtWidgets.QAction(MainWindow)
        self.actionCriar.setObjectName("actionCriar")
        self.actionSalvar = QtWidgets.QAction(MainWindow)
        self.actionSalvar.setObjectName("actionSalvar")
        self.actionFechar = QtWidgets.QAction(MainWindow)
        self.actionFechar.setObjectName("actionFechar")
        self.actionCarregar_arquivo_s = QtWidgets.QAction(MainWindow)
        self.actionCarregar_arquivo_s.setObjectName("actionCarregar_arquivo_s")
        self.menuBase.addAction(self.actionCriar)
        self.menuBase.addAction(self.actionSalvar)
        self.menuBase.addAction(self.actionFechar)
        self.menuTexto.addAction(self.actionCarregar_arquivo_s)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.menuBase.menuAction())
        self.menuMenu.addAction(self.menuTexto.menuAction())
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabOption.setCurrentIndex(0)
        self.tabBase.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.initSignals()
        self.init()
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pré-Processamento de Texto"))
        self.checkBox.setText(_translate("MainWindow", "Remover StopWords"))
        self.checkBox_3.setText(_translate("MainWindow", "Stemização"))
        self.checkBox_2.setText(_translate("MainWindow", "Lematização"))
        self.tabOption.setTabText(self.tabOption.indexOf(self.tabParameters), _translate("MainWindow", "Parâmetros"))
        self.radioButton.setText(_translate("MainWindow", "Bag of Words"))
        self.radioButton_2.setText(_translate("MainWindow", "Tf-Idf"))
        self.label_8.setText(_translate("MainWindow", "n-grama:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "3"))
        self.comboBox.setItemText(3, _translate("MainWindow", "4"))
        self.comboBox.setItemText(4, _translate("MainWindow", "5"))
        self.tabOption.setTabText(self.tabOption.indexOf(self.tabModel), _translate("MainWindow", "Modelo"))
        self.label_6.setText(_translate("MainWindow", "Base:"))
        self.label_2.setText(_translate("MainWindow", "Título: "))
        self.label_title.setText(_translate("MainWindow", "Nenhum"))
        self.label_3.setText(_translate("MainWindow", "Autor(a): "))
        self.label_author.setText(_translate("MainWindow", "Nenhum"))
        self.label_7.setText(_translate("MainWindow", "# Instâncias:"))
        self.labelNumInst.setText(_translate("MainWindow", "0"))
        self.label_9.setText(_translate("MainWindow", "# Termos:"))
        self.labelNumTerms.setText(_translate("MainWindow", "0"))
        self.tabBase.setTabText(self.tabBase.indexOf(self.tabDict), _translate("MainWindow", "Dicionário"))
        self.tabBase.setTabText(self.tabBase.indexOf(self.tabTab), _translate("MainWindow", "Saída"))
        self.label.setText(_translate("MainWindow", "Tabela de Arquivos:"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Classe"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Arquivo"))
        self.pushButtonExecute.setText(_translate("MainWindow", "Executar"))
        self.menuMenu.setTitle(_translate("MainWindow", "Arquivo"))
        self.menuBase.setTitle(_translate("MainWindow", "Base"))
        self.menuTexto.setTitle(_translate("MainWindow", "Texto"))
        self.actionCriar.setText(_translate("MainWindow", "Criar"))
        self.actionCriar.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSalvar.setText(_translate("MainWindow", "Salvar"))
        self.actionSalvar.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionFechar.setText(_translate("MainWindow", "Fechar"))
        self.actionFechar.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionCarregar_arquivo_s.setText(_translate("MainWindow", "Carregar arquivo(s)"))
        self.actionCarregar_arquivo_s.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.textEditOutput.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

