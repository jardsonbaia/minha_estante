# encoding: utf-8
#conexao com  o banco de dados
import psycopg2
# socket
import socket

HOST = "200.129.39.74"    # Endereco IP do Servidor

PORT = 30005            # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (HOST, PORT)
# Colocando um endereco IP e uma porta no Socket
tcp.bind(origem)
# Colocando o Socket em modo passivo
tcp.listen(1)
print('\nServidor TCP iniciado no IP', HOST, 'na porta', PORT)

def  cadastro_user():
	print("\n ================= CADASTRAR NOVO USUARIO ===================== \n ")
	 # Recebendo as mensagens atraves da conexao o nome do usuario
	usuario = tcp.recv(1024) 
	print(usuario) 
	s1 = tcp.recv(1024)
	print(s1)
	senha=s1
	# Connect to an existing database
	conn = psycopg2.connect(dbname='tcpbanco', user='postgres',password='alunoufc',host='localhost')
# Open a cursor to perform database operations
	cur = conn.cursor()
	#Verificar se usuario ja existe
	cur.execute("SELECT login FROM cadastro_usuario;")
	lent= []
	print (lent)
	lent = cur.fetchall()
	print len(lent)
	if len(lent)>= 4:
		tcp.send(str("Erro não ouver Cadastro"))		
	else:
		login = usuario
		#guardar_usuario no banco de dados 
		cur.execute("INSERT INTO cadastro_usuario (login,senha ) VALUES (%s, %s)",(login,senha))
		print("\n  Usuario cadastrado!\n")
		tcp.send(str("Usuario cadastrado!\n"))
		conn.commit()
		
	
# Make the changes to the database persistent
	conn.commit()

# Close communication with the database
	cur.close()
	conn.close()

# Remover Livro
def remover_livro():
	conn = psycopg2.connect(dbname='tcpbanco', user='postgres',password='alunoufc',host='localhost')
	cur = conn.cursor()
	titulo = tcp.recv(1024)
	autor = tcp.recv(1024)
	cur.execute("SELECT titulo,autor FROM livros where titulo = %(titulo)s and autor = %(autor)s;",{'titulo':titulo,'autor':autor})
	rows = cur.fetchall()
	if len(rows)!= 0:
		cur.execute("DELETE FROM livros where titulo = %(titulo)s and autor = %(autor)s;",{'titulo':titulo,'autor':autor})
		tcp.send(str("ok"))
		conn.commit()
	else:
		tcp.send(str("erro"))
def ver_livros():
	conn = psycopg2.connect(dbname='tcpbanco', user='postgres',password='alunoufc',host='localhost')
	#Open a cursor to perform database operations
	cur = conn.cursor()
	id_user = tcp.recv(1024)
	cur.execute("SELECT titulo FROM livros where id_usuario = %(id_user)s",{'id_user':id_user})
	rows = cur.fetchall()
	
	if len(rows)!=0:
		rows=str(rows)
		tcp.send(rows)
	else:
		tcp.send(str("Lista de Livros Vazia "))

	
def guardar_livro():
	conn = psycopg2.connect(dbname='tcpbanco', user='postgres',password='alunoufc',host='localhost')
	cur = conn.cursor()
	titulo = tcp.recv(1024)
	autor = tcp.recv(1024)
	genero = tcp.recv(1024)
	id_usuario = tcp.recv(1024)
	cur.execute("SELECT titulo,autor FROM livros where titulo = %(titulo)s and autor = %(autor)s;",{'titulo':titulo,'autor':autor})
	rows = cur.fetchall()
	if len(rows)!= 0:
		print "errrrrrrrrrrooo"
		tcp.send(str("erro"))
	else:
		#guardar_usuario no banco de dados 
			cur.execute("INSERT INTO livros (titulo,autor,genero,id_usuario) VALUES (%s,%s,%s,%s)",(titulo,autor,genero,id_usuario))
			tcp.send(str("ok"))
			conn.commit()
def iniciar_biblioteca():
	while True:
		menu = tcp.recv(1024)
		if menu == "1":
			guardar_livro()
		if menu == "2":
			ver_livros()
		if menu == "3":
			remover_livro()
	print ("\n░░░░ Fim da consulta!")
def  login():
	print("\n ================= Login ===================== \n ")
	usuario = tcp.recv(1024)
	s1 = tcp.recv(1024)
	conn = psycopg2.connect(dbname='tcpbanco', user='postgres',password='alunoufc',host='localhost')
	# Open a cursor to perform database operations
	cur = conn.cursor()
	#Verificar se usuario existe
	cur.execute("SELECT login FROM cadastro_usuario;")
	rows = cur.fetchall()
	if len(rows) != 0:
		cur.execute("SELECT senha FROM cadastro_usuario where login = %(usuario)s;",{'usuario':usuario})
		sen=cur.fetchall()
		if sen !=0: 
			tcp.send(str("ok"))
			iniciar_biblioteca()
		else:
			tcp.send(str("senha"))
	else:
		tcp.send(str("login"))
	 

while True:

   # Aceitando uma nova conexao

   tcp, cliente = tcp.accept()

   print('\nConexao realizada por:', cliente)

   while True:
	   mensagem = tcp.recv(1024)
	   if mensagem == "1":
		   login()
	   if mensagem == "2":
		   cadastro_user()			

       # Exibindo a mensagem recebida

print("\n Cliente..: ", cliente)

print("Mensagem.:", mensagem.decode())

print("Finalizando conexao do cliente", cliente)

   
