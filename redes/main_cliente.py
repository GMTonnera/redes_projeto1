import jogocliente
import curses



nome = input("digite seu nome:\n")

a = jogocliente.JogoCliente(("127.0.0.1", 65432), nome)
a.main()
