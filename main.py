import PySimpleGUI as sg
import pyodbc
import pandas as pd

dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-3PKKPL3\SQLEXPRESS;"
    "Database=PythonSQL;"
)

conexao = pyodbc.connect(dados_conexao)
print("Conexão Bem Sucedida")
cursor = conexao.cursor()

query = "SELECT * FROM Alunos;"
df = pd.read_sql(query, conexao)
print(df.head(26))





layoutCadastro = [
    [sg.Text('RGM:'), sg.Text('      '), sg.InputText(size=(12, 12), key='rgm'), sg.Text(' '*5)],
    [sg.Text('Nome:'), sg.Text('     '),  sg.InputText(size=(12, 12), key='nome'), sg.Text(' '*35)],
    [sg.Text('Idade:'), sg.Text('      '),  sg.InputText(size=(12, 12), key='idade')],
    [sg.Text('Nascimento:'),  sg.InputText(size=(12, 12), key='nasc')],
    [sg.Text('CPF:'), sg.Text('       '),  sg.InputText(size=(12, 12), key='cpf')],
    [sg.Radio('Masculino', 'RADIO1', key='masc'), sg.Radio('Feminino', 'RADIO2', key='fem')],
    [sg.Button('Enviar', key='cadastro')]
]

layoutDeletar = [
    [sg.Text('Deletar por RGM:'), sg.InputText(size=(12,12), key='deletergm')],
    [sg.Text('Deletar por Nome:'), sg.InputText(size=(12,12), key='deletenome')],
    [sg.Button('Deletar', key='deletar')]
]


layoutMain = [
    [sg.Frame('', layout=layoutCadastro, size=(410,220))]
]

tabs = [
    [sg.TabGroup([[sg.Tab('Cadastro', layoutMain), sg.Tab('Deletar', layoutDeletar)]])]
]


mainlayout = [
    [sg.Frame('', layout=tabs), sg.Multiline(df, size=(70,16), key='multi', background_color='#075c92', text_color='white')]
]


window = sg.Window('Escola', mainlayout, resizable=True)


while True:
    event, values = window.read()

    rgmIn = values['rgm']
    nomeIn = values['nome']  
    idadeIn = values['idade']
    nascIn = values['nasc']
    cpfIn = values['cpf']
    deletarrgm = values['deletergm']
    deletarnome = values['deletenome']

    if event == sg.WIN_CLOSED:
        break

    if event == 'cadastro':
        if values['masc'] == True and values['fem'] == False:
            comando = f"""INSERT INTO Alunos(RGM, Nome, Idade, Nascimento, CPF, Sexo)
            VALUES
                ({rgmIn}, '{nomeIn}', '{idadeIn}', '{nascIn}', '{cpfIn}', 'Masculino')"""

            cursor.execute(comando)
            cursor.commit()
            window['rgm']('')
            window['nome']('')
            window['idade']('')
            window['nasc']('')
            window['cpf']('')
            window.Element('masc').TKIntVar.set(0)
            c = pyodbc.connect(dados_conexao)
            cursor = c.cursor()
            query = "SELECT * FROM Alunos;"
            df = pd.read_sql(query, c)
    
            window['multi']('{}'.format(df))
    
        elif values['fem'] == True and values['masc'] == False:
            comando = f"""INSERT INTO Alunos(RGM, Nome, Idade, Nascimento, CPF, Sexo)
            VALUES
                ({rgmIn}, '{nomeIn}', '{idadeIn}', '{nascIn}', '{cpfIn}', 'Feminino')"""

            cursor.execute(comando)
            cursor.commit()
            window['rgm']('')
            window['nome']('')
            window['idade']('')
            window['nasc']('')
            window['cpf']('')
            window.Element('fem').TKIntVar.set(0)
            c = pyodbc.connect(dados_conexao)
            cursor = c.cursor()
            query = "SELECT * FROM Alunos;"
            df = pd.read_sql(query, c)
            window['multi']('{}'.format(df))


    if event == 'deletar':
        #print(values[0])
        #print(values[1])
        #print(values[2])
        #print(values[3])
        #print(values[4])
        #print(values[5])
        
        sg.Popup(f'Deseja deletar o RGM {deletarrgm}?', title='')
        comando = f"""DELETE FROM Alunos WHERE RGM='{deletarrgm}';
                      DELETE FROM Alunos WHERE Nome='{deletarnome}';"""

        cursor.execute(comando)
        cursor.commit()
        window['deletergm']('')
        window['deletenome']('')
        c = pyodbc.connect(dados_conexao)
        cursor = c.cursor()
        query = "SELECT * FROM Alunos;"
        df = pd.read_sql(query, c)
        window['multi'](df)




window.close()
