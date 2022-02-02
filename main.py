from mailbox import NotEmptyError
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
import sqlite3


def listardados():
    banco = sqlite3.connect('pythonbase.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM Alunos")
    dados_lidos = cursor.fetchall()
    window.alunos.setRowCount(len(dados_lidos))
    window.alunos.setColumnCount(5)
    window.alunos.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            window.alunos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        
    banco.close()

def salvardados():
    rgm = window.rgmIn.text()
    nome = window.nomeIn.text()
    idade = window.idadeIn.text()
    nascimento = window.nascIn.text()
    cpf = window.cpfIn.text()

    
    banco = sqlite3.connect('pythonbase.db')
    cursor = banco.cursor()
    cursor.execute("INSERT INTO Alunos VALUES ('"+rgm+"', '"+nome+"', '"+idade+"', '"+cpf+"', '"+nascimento+"')")
        
    banco.commit()
    banco.close()
    listardados()

    window.rgmIn.clear()
    window.nomeIn.clear()
    window.idadeIn.clear()
    window.nascIn.clear()
    window.cpfIn.clear()


def deletardados():
    drgm = window.rgmDelete.text()
    dnome = window.nomeDelete.text()

    banco = sqlite3.connect('pythonbase.db')
    cursor = banco.cursor()
    cursor.execute(f"""DELETE FROM ALUNOS WHERE RGM='{drgm}';""")
    cursor.execute(f"""DELETE FROM ALUNOS WHERE Nome='{dnome}';""")
    banco.commit()
    banco.close()
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
        banco = sqlite3.connect('pythonbase.db')
        cursor = banco.cursor()

        cursor.execute(f"""UPDATE Alunos SET Nome = '{nome}', Idade = '{idade}', Nascimento = '{nascimento}', CPF = '{cpf}' WHERE RGM = {rgm};""")

        banco.commit()
        banco.close()
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
        
        banco = sqlite3.connect('pythonbase.db')
        cursor = banco.cursor()
        cursor.execute(f"""SELECT * FROM Alunos WHERE RGM = {rgm};""")
        dados_lidos = cursor.fetchall()
        window.alunos_2.setRowCount(len(dados_lidos))
        window.alunos_2.setColumnCount(5)
        window.alunos_2.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
        for i in range(0, len(dados_lidos)):
            for j in range(0, 5):
                window.alunos_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

        banco.commit()
        banco.close()
        listardados()

        window.rgmSearch.clear()
    except sqlite3.OperationalError:
        msg = QMessageBox()
        msg.setWindowTitle("Erro")
        msg.setText("Letras não são aceitas!")
        msg.exec_()

def buscarCpf():
    cpf = window.cpfSearch.text()

    banco = sqlite3.connect('pythonbase.db')
    cursor = banco.cursor()
    cursor.execute(f"""SELECT * FROM Alunos WHERE CPF = '{cpf}';""")
    dados_lidos = cursor.fetchall()
    window.alunos_2.setRowCount(len(dados_lidos))
    window.alunos_2.setColumnCount(5)
    window.alunos_2.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            window.alunos_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    banco.commit()
    banco.close()
    window.cpfSearch.clear()

def ordenaridade():
       
    banco = sqlite3.connect('pythonbase.db')
    cursor = banco.cursor()
    cursor.execute(f"""SELECT * FROM Alunos ORDER BY Idade DESC;""")
    dados_lidos = cursor.fetchall()
    window.alunos_2.setRowCount(len(dados_lidos))
    window.alunos_2.setColumnCount(5)
    window.alunos_2.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            window.alunos_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    banco.commit()
    banco.close()
    listardados()

def ordenarnasc():
    banco = sqlite3.connect('pythonbase.db')
    cursor = banco.cursor()
    cursor.execute(f"""SELECT * FROM Alunos ORDER BY Nascimento DESC;""")
    dados_lidos = cursor.fetchall()
    window.alunos_2.setRowCount(len(dados_lidos))
    window.alunos_2.setColumnCount(5)
    window.alunos_2.setHorizontalHeaderLabels(['RGM', 'Nome', 'Idade', 'CPF', 'Nascimento'])
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            window.alunos_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    banco.commit()
    banco.close()
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




app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi('alunos.ui')
listardados()

window.cadastrar.clicked.connect(salvardados)
window.deletar.clicked.connect(deletardados)
window.editar.clicked.connect(editardados)
window.buscar.clicked.connect(buscardados)
window.ordIdade.clicked.connect(ordenaridade)
window.buscarCpf.clicked.connect(buscarCpf)
window.ordnasc.clicked.connect(ordenarnasc)
window.salvartxt_3.triggered.connect(salvartxt)


window.show()
app.exec()
