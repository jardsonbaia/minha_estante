# encoding: utf-8
import socket
#conexao ao servidor  
HOST =raw_input("informe o Endereço: ")

PORT=input("informe o Porta: ")
# Criando a conexao

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

destino = (HOST, PORT)

tcp.connect(destino)
def mostrar_menu():
	print (19*"░" + " MINHA ESTANTE " + 20*"░")
	print ("░░░[1]➔ Guardar Livro        [2]➔ Ver Livros      ░░░░")
	print (17*"░" + " [3] RETIRAR LIVRO " + 18*"░")


#tela menu login e senha  
def tela_cadrastro_ou_login():
	print (19*"░" + " Tela de Login" + 20*"░")
	print ("░░░░░░░[1]➔ tele de login"+ 28*"░")
	print ("░░░░░░░[2]➔ Cadastrar um novo usuario"+ 17*"░")
	menu2 = raw_input("⦾ MENU: ")
	tcp.send(str(menu2).encode())
	if menu2 =="1":
		login()
	if menu2 =="2":
		cadastro_user()
### guardar livro
def guardar_livro():    
	titulo = raw_input("Título: ").upper()
	tcp.send(str(titulo).encode())
	autor = raw_input("Autor: ").upper()
	tcp.send(str(autor).encode())
	genero = raw_input("Gênero: ").upper()
	tcp.send(str(autor).encode())
	id_usuario = raw_input("Informe seu ID: ").upper()
	tcp.send(str(id_usuario).encode())
	msg = tcp.recv(1024)
	print "test"
	if msg == "erro":
		print ("\n ⚠ Opps! Você já guardou este livro.\n")
	elif msg == "ok":
		print ("\n ✔ Livro guardado!\n")	
def  cadastro_user():
	print("\n ================= CADASTRAR NOVO USUARIO ===================== \n ")
	print("========Escolha um login maior do 4 Caracteres =========")
	usuario = raw_input("Digite o nome do usuario: ")
	tcp.send(str(usuario).encode())
	s1 = raw_input("Digite uma senha: ")
	tcp.send(str(s1).encode())
	msg = tcp.recv(1024)
	print(msg)
	tcp.close()
#ver livros		
def ver_livros():
	id_user = raw_input("Informe seu ID: ")
	tcp.send(str(id_user).encode())
	mensg=tcp.recv(2024)
	print (mensg)
		# Remover Livro
def remover_livro():
	titulo = raw_input("Título: ").upper()
	tcp.send(str(titulo).encode())
	autor = raw_input("Autor: ").upper()
	tcp.send(str(autor).encode())
	msg=tcp.recv(1024)
	if msg =="ok":
		print("Livro Deletado")
	if msg =="erro":
		print("Não existe esse livro")
			
def iniciar_biblioteca():
	while True:
		mostrar_menu()
		menu = int(raw_input("⦾ MENU: "))
		tcp.send(str(menu).encode())
		if menu == 1:
			print "test"
			guardar_livro()
		if menu == 2:
			ver_livros()
		if menu == 3:
			remover_livro()
	print ("\n░░░░ Fim da consulta!")

	
def  login():
	print("\n ================= login ===================== \n ")
	usuario = raw_input("Digite o nome do usuario: ")
	tcp.send(str(usuario).encode())
	s1 = raw_input("Digite uma senha: ")
	tcp.send(str(s1).encode())
	msg = tcp.recv(1024)
	if msg =="ok":
		iniciar_biblioteca()
	elif msg =="senha":
		print("Senha Errada")
	elif msg =="login":
		print("Login Errada")

# Recebendo a mensagem do usuário final pelo teclado
tela_cadrastro_ou_login()
