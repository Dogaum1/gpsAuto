from PyQt5 import QtWidgets, uic
from core import Core
import os

class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        self.core = Core()
        self.setupUi()
        self.setupComboBox()
        self.connectButtons()
        self.show()

    def setupUi(self):
        try:
            uic.loadUi(f"{os.getcwd()}/assets/qt/interface3.ui", self)
        except:
            uic.loadUi("C:/Users/INSS/Documents/python/gpsauto/source/assets/qt/interface3.ui", self)
        
        self.changeScreen(0)

    def changeScreen(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def setupComboBox(self):
        self.categoryInput.addItem('CONTRIBUINTE INDIVIDUAL', ['1007 - CONTRIBUINTE INDIVIDUAL - RECOLHIMENTO MENSAL NIT/PIS/PASEP', '1163 - CONTRIBUINTE INDIVIDUAL - OPÇÃO 11% (ART. 80 DA LC 123/2006) RECOLHIMENTO MENSAL - NIT/PIS/PASEP', '1120 - CONTRIBUINTE INDIVIDUAL - RECOLHIMENTO MENSAL - COM DEDUCAO DE 45% (LEI  9.876/99) - NIT/PIS/PASEP', '1236 - CI OPTANTE LC 123 MENSAL RURAL', '1287 - CI MENSAL RURAL', '1805 - CI COM DIREITO A DEDUCAO MENSAL - RURAL'])
        self.categoryInput.addItem('DOMESTICO', ['1600 - EMPREGADO DOMESTICO MENSAL - NIT /PIS/PASEP'])
        self.categoryInput.addItem('FACULTATIVO', ['1406 - FACULTATIVO MENSAL - NIT/PIS/PASEP', '1473 - FACULTATIVO - OPÇÃO 11% (ART. 80 DA LC 123/2006) RECOLHIMENTO MENSAL - NIT/PIS/PASEP', '1929 - FACULTATIVO BAIXA RENDA - RECOLHIMENTO MENSAL - NIT/PIS/PASEP'])
        self.categoryInput.addItem('SEGURADO ESPECIAL', ['1503 - SEGURADO ESPECIAL MENSAL - NIT/PIS/PASEP'])

        self.categoryInput.currentIndexChanged.connect(self.updatePaymentValueCombo)
        self.updatePaymentValueCombo(self.categoryInput.currentIndex())

    def connectButtons(self):
        self.startButton.clicked.connect(self.startCore)
        self.continueButton.clicked.connect(self.phaseOne)
        self.continueButton2.clicked.connect(self.phaseTwo)
        self.gerateButton.clicked.connect(self.phaseTwoAlt)

    def startCore(self):
        self.changeScreen(1)
        self.core.start()

    def phaseOne(self):
        self.changeScreen(2)
        category = ['AUTONOMO','DOMESTICO', 'FACULTATIVO', 'SEGURADO_ESPECIAL']
        self.core.phaseOne(category[self.categoryInput.currentIndex()], self.nitInput.text(), self.captchaInput.text())

    def phaseTwo(self):
        if self.allYearInput.isChecked():
            self.core.phaseTwo(self.yearInput.text(), self.salaryInput.text(), str(self.paymentCodeInput.currentText())[0:4], self.core.allYearMode)
        else:
            self.changeScreen(3)

    def phaseTwoAlt(self):
        self.core.phaseTwo(self.yearInput.text(), self.salaryInput.text(), str(self.paymentCodeInput.currentText())[0:4], self.verifyMode(), self.collectCheckBoxInfo())

    def verifyMode(self):
        if self.exceptInput.isChecked():
            return self.core.exceptMode
        elif self.intervalInput.isChecked():
            return self.core.intervalMode
        else:
            return self.core.specificMode

    def collectCheckBoxInfo(self):
        checkBoxList = self.page4.findChildren(QtWidgets.QCheckBox)
        checked = []
        
        for c in range(len(checkBoxList)):
            if(checkBoxList[c].isChecked()):
                checked.append(checkBoxList[c].text().replace(" ", "")[0:2])        
        return checked

    def updatePaymentValueCombo(self, index):
        self.paymentCodeInput.clear()
        values = self.categoryInput.itemData(index)
        if values:
            self.paymentCodeInput.addItems(values)   
