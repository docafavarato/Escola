from mailbox import NotEmptyError
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
from fpdf import FPDF
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import os

banco = sqlite3.connect('pythonbase.db')
cursor = banco.cursor()

def listardados():
    cursor.execute("SELECT * FROM Alunos")
    dados_lidos = cursor.fetchall()
    window.alunos.setRowCount(len(dados_lidos))
    window.alunos.setColumnCount(5)
    window.alunos.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            window.alunos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
     

def salvardados():
    rgm = window.rgmIn.text()
    nome = window.nomeIn.text()
    idade = window.idadeIn.text()
    nascimento = window.nascIn.text()
    cpf = window.cpfIn.text()

    cursor.execute("INSERT INTO Alunos VALUES ('"+rgm+"', '"+nome+"', '"+idade+"', '"+cpf+"', '"+nascimento+"')")
        
    banco.commit()
    listardados()

    window.rgmIn.clear()
    window.nomeIn.clear()
    window.idadeIn.clear()
    window.nascIn.clear()
    window.cpfIn.clear()


def deletardados():
    drgm = window.rgmDelete.text()
    dnome = window.nomeDelete.text()
    
    cursor.execute(f"""DELETE FROM ALUNOS WHERE RGM='{drgm}';""")
    cursor.execute(f"""DELETE FROM ALUNOS WHERE Nome='{dnome}';""")
    banco.commit()
    listardados()

    window.rgmDelete.clear()
    window.nomeDelete.clear()

def editardados():
    rgm = window.rgmEdit.text()
    nome = window.nomeEdit.text()
    idade = window.idadeEdit.text()
    nascimento = window.nascEdit.text()
    cpf = window.cpfEdit.text()

    try:
        cursor.execute(f"""UPDATE Alunos SET Nome = '{nome}', Idade = '{idade}', Nascimento = '{nascimento}', CPF = '{cpf}' WHERE RGM = {rgm};""")

        banco.commit()
        listardados()
    
    except sqlite3.OperationalError:
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText("Letras não são aceitas!")
        msg.exec_()
        
    window.rgmEdit.clear()
    window.nomeEdit.clear()
    window.idadeEdit.clear()
    window.nascEdit.clear()
    window.cpfEdit.clear()

def buscardados():
    try:
        rgm = window.rgmSearch.text()
        cursor.execute(f"""SELECT * FROM Alunos WHERE RGM = {rgm};""")
        dados_lidos = cursor.fetchall()
        window.alunos_2.setRowCount(len(dados_lidos))
        window.alunos_2.setColumnCount(5)
        window.alunos_2.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
        for i in range(0, len(dados_lidos)):
            for j in range(0, 5):
                window.alunos_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

        banco.commit()
        listardados()

        window.rgmSearch.clear()
    except sqlite3.OperationalError:
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText("Letras não são aceitas!")
        msg.exec_()

def buscarCpf():
    cpf = window.cpfSearch.text()
    
    cursor.execute(f"""SELECT * FROM Alunos WHERE CPF = '{cpf}';""")
    dados_lidos = cursor.fetchall()
    window.alunos_2.setRowCount(len(dados_lidos))
    window.alunos_2.setColumnCount(5)
    window.alunos_2.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            window.alunos_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    banco.commit()
    window.cpfSearch.clear()


def ordenaridade():
    cursor.execute(f"""SELECT * FROM Alunos ORDER BY Idade DESC;""")
    dados_lidos = cursor.fetchall()
    window.alunos_2.setRowCount(len(dados_lidos))
    window.alunos_2.setColumnCount(5)
    window.alunos_2.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            window.alunos_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    banco.commit()
    listardados()

def ordenarnasc():
    cursor.execute(f"""SELECT * FROM Alunos ORDER BY Nascimento DESC;""")
    dados_lidos = cursor.fetchall()
    window.alunos_2.setRowCount(len(dados_lidos))
    window.alunos_2.setColumnCount(5)
    window.alunos_2.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            window.alunos_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    banco.commit()
    listardados()

def salvartxt():
    rgm = window.rgmIn.text()
    nome = window.nomeIn.text()
    idade = window.idadeIn.text()
    nascimento = window.nascIn.text()
    cpf = window.cpfIn.text()
    f = open(f"rgm{rgm}.txt", "a")
    f.write(f"RGM: {rgm}\nNome: {nome}\nIdade: {idade}\nNascimento: {nascimento}\nCPF: {cpf}")
    f.close()

def pdf():
    nome = window.nomeIn.text()
    rgm = window.rgmIn.text()
    idade = window.idadeIn.text()
    nascimento = window.nascIn.text()
    cpf = window.cpfIn.text()
    
    fileName = f'rgm{rgm}.pdf'
    documentTitle = f'{nome}'
    title = f'{nome}'
    subTitle = f'{nome}'
    textLines = [
        f'RGM: {rgm}',
        f'Nome: {nome}',
        f'Idade: {idade}',
        f'Nascimento: {nascimento}',
        f'CPF: {cpf}'
    ]
 
    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)
    pdf.drawCentredString(300, 770, subTitle)
    pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont("Courier-Bold", 24)
    pdf.line(30, 710, 550, 710)
    text = pdf.beginText(40, 680)
    text.setFont("Courier", 18)
    text.setFillColor(colors.red)
    for line in textLines:
        text.textLine(line)
    pdf.drawText(text)
    pdf.save()
    path = f'rgm{rgm}.pdf'
    os.system(path)


app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi('alunos.ui')
listardados()
window.alunos.horizontalHeader().setStretchLastSection(True)
window.alunos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

window.cadastrar.clicked.connect(salvardados)
window.deletar.clicked.connect(deletardados)
window.editar.clicked.connect(editardados)
window.buscar.clicked.connect(buscardados)
window.ordIdade.clicked.connect(ordenaridade)
window.buscarCpf.clicked.connect(buscarCpf)
window.ordnasc.clicked.connect(ordenarnasc)
window.salvartxt_3.triggered.connect(salvartxt)
window.pdf.triggered.connect(pdf)
    

window.show()
app.exec()

banco.close()
