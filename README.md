# Projeto da cadeira de Redes de Computadores	


## Este projeto foi desenvolvido por:

	- David Calhas, nº 80980, Curso: LEIC-A
	- João Silveira, nº 80789, Curso: LEIC-A
	- Pedro Orvalho, nº 81151, Curso: LEIC-A

# Ficheiros (código):

### TCS.py

Servidor que aceita pedidos dos utilizadores e comunica com os servidores TRS por UDP.

### TRS.py

Servidor que faz a produção das palavras. Comunica com os utilizadores por TCP e comunica com o servidor TCS por UDP. Podem existir vários servidores TRS.

### userApp.py

Aplicação pela qual o utilizador faz os pedidos de tradução.


# Como correr:

### 	TCS server:


Para começar o TCS (TCSport é o porto onde é feita a comunicação):
```
% python TCS.py -p TCSport
```

###		TRS Server:

Para começar o TRS (LANGUAGE é a linguagem que este servidor traduz, TRSport é o porto do servidor TRS, TCSname é o endereço do TCS, TCSPORT é o porto de conexão com o TCS):

```

% python TRS.py LANGUAGE -p TRSport -n TCSname -e TCSport
```

### 	User App:

Para começar a aplicação do utilizador (TCSname é o nome do servidor TCS, TCSport é o porto do servidor TCS):

```

% python userApp.py -n TCSname -p TCSport
```

Nota: Todos os parâmetros que são precedidos de -p, -n ou -e são opcionais, ou seja, podem ser lançadas as aplicações sem a existência dos parâmetros.


