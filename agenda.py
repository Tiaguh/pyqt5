from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

# https://github.com/theflutterfactory/React-Native-Tutorials/blob/react-native-maps_example/src/CarouselMap.js

contact_id = 0

banco = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database= "agenda"
)

contactId = None

def cadastrarContato():
  campoNome = agenda.input_name.text()
  campoEmail = agenda.input_email.text()
  campoTelefone = agenda.input_telefone.text()

  if agenda.residencial_check.isChecked():
    tipoTelefone = "Residencial"
  elif agenda.telefone_check.isChecked():
    tipoTelefone = "Celular"
  else: 
    tipoTelefone = "Não informado"

  cursor = banco.cursor()
  comando_SQL = "INSERT INTO contatos (nome, email, telefone, tipoTelefone) VALUES (%s, %s, %s, %s)"
  dados = (str(campoNome), str(campoEmail), str(campoTelefone), tipoTelefone)
  cursor.execute(comando_SQL, dados)
  banco.commit()
  agenda.hide()
  consultarContatos()

def consultarContatos():
  agenda.hide()
  tabela.show()

  cursor = banco.cursor()
  comando_SQL = "SELECT * FROM contatos"
  cursor.execute(comando_SQL)
  contatosLidos = cursor.fetchall()

  tabela.tabelaContatos.setRowCount(len(contatosLidos))
  tabela.tabelaContatos.setColumnCount(5)

  for i in range (0, len(contatosLidos)):
    for f in range(0, 5):
      tabela.tabelaContatos.setItem(i, f, QtWidgets.QTableWidgetItem(str(contatosLidos[i][f])))

  linhaContato = tabela.tabelaContatos.currentRow()

def gerarPdf():
  cursor = banco.cursor()
  comando_SQL = "SELECT * FROM contatos"
  cursor.execute(comando_SQL)
  contatos_lidos = cursor.fetchall()

  y = 0
  pdf = canvas.Canvas("lista_contatos.pdf")
  pdf.setFont("Times-Bold", 25)
  pdf.drawString(200, 800, "Lista de Contatos")

  pdf.setFont("Times-Bold", 18)
  pdf.drawString(10, 750, "ID")
  pdf.drawString(110, 750, "NOME")
  pdf.drawString(210, 750, "EMAIL")
  pdf.drawString(410, 750, "TELEFONE")
  pdf.drawString(510, 750, "TIPO DE CONTATO")

  for i in range(0, len(contatos_lidos)):
    y = y + 50
    pdf.drawString(10, 750 -y, str(contatos_lidos[i][0]))
    pdf.drawString(110, 750 -y, str(contatos_lidos[i][1]))
    pdf.drawString(210, 750 -y, str(contatos_lidos[i][2]))
    pdf.drawString(410, 750 -y, str(contatos_lidos[i][3]))
    pdf.drawString(510, 750 -y, str(contatos_lidos[i][4]))

    pdf.save()
    print("PDF gerado com sucesso!")

def excluirContato():
  linhaContato = tabela.tabelaContatos.currentRow()
  tabela.tabelaContatos.removeRow(linhaContato)

  cursor = banco.cursor()
  comando_SQL = "SELECT id FROM contatos"
  cursor.execute(comando_SQL)
  contatos_lidos = cursor.fetchall()
  valorId = contatos_lidos[linhaContato][0]
  cursor.execute("DELETE FROM contatos WHERE id=" + str(valorId))
  banco.commit()

def atualizarContatos():
  global contact_id
  campoNome = atualizarContato.input_name.text()
  campoEmail = atualizarContato.input_email.text()
  campoTelefone = atualizarContato.input_telefone.text()

  tipoTelefone = "Não informado"

  if atualizarContato.residencial_check.isChecked():
    tipoTelefone = "Residencial"
  elif atualizarContato.telefone_check.isChecked():
    tipoTelefone = "Celular"

  cursor = banco.cursor()
  comando_SQL = ("UPDATE contatos SET nome = %s, email = %s, telefone = %s, tipoTelefone = %s WHERE id =" + str(contact_id))
  dados = (str(campoNome), str(campoEmail), str(campoTelefone), tipoTelefone)
  cursor.execute(comando_SQL, dados)
  banco.commit()
  consultarContatos()

def changeScreen():
  global contact_id

  linhaContato = tabela.tabelaContatos.currentRow()

  cursor = banco.cursor()
  comando_SQL = "SELECT id FROM contatos"
  cursor.execute(comando_SQL)
  contatos_lidos = cursor.fetchall()

  contact_id = contatos_lidos[linhaContato][0]

  print(contact_id)
  
  atualizarContato.show()
  tabela.hide()

def backScreen():
  agenda.show()
  tabela.hide()

app = QtWidgets.QApplication([])
agenda = uic.loadUi("agenda.ui")
tabela = uic.loadUi("contatos.ui")
atualizarContato = uic.loadUi("atualizarCadastro.ui")

agenda.btnCadastro.clicked.connect(cadastrarContato)
agenda.btnConsulta.clicked.connect(consultarContatos)

tabela.btnExcluirContato.clicked.connect(excluirContato)
tabela.btnGeraPdf.clicked.connect(gerarPdf)
tabela.btnAlterarContato.clicked.connect(changeScreen)
tabela.btnVoltar.clicked.connect(backScreen)

atualizarContato.btnAtualizar.clicked.connect(atualizarContatos)


agenda.show()
app.exec()