# Projeto de Redes de Computadores


## Este projeto foi desenvolvido por:

	- David Calhas, nº 80980, Curso: LEIC-A
	- João Silveira, nº 80789, Curso: LEIC-A
	- Pedro Orvalho, nº 81151, Curso: LEIC-A

Este projecto foi desenvolvido de acordo com o enunciado em português com a data 27/09/2016

# Como correr:

### 	TCS server:

Para correr o TCS :
```
python TCS.py -p TCSport
```

###		TRS Server:

Para correr o TRS:

```
python TRS.py LANGUAGE -p TRSport -n TCSname -e TCSport
```

LANGUAGE é o nome da linguagem e da pasta onde se encontram os ficheiros para tradução e os dicionários da linguagem respectiva, e estes têm de ser colocados nesta pasta.

### 	User App:

Para correr a aplicação utilizador:

```

python userApp.py -n TCSname -p TCSport
```

Nota: Os parâmetros -p, -n ou -e são opcionais.
