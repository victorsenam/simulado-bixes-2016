#!/bin/bash

#
# Autor: Marcio T. I. Oshiro 06/04/2015
#
# Gera arquivos de entrada/saida finais para cada problema e executa os verificadores neles
# 

# $1 path para o checker
# $2 arquivo de entrada a ser verificado
# $3 arquivo de saida correspondente a $2
# $2 ou $3 podem ser vazios, mas nunca ambos ao mesmo tempo
function executaChk() { 
	echo "Checando arquivo de entrada usando $chk"
	# verifica em qual linguagem esta implementado o checker
	if [ $( echo "$1" | egrep ".rb$" ) ]; then
		ruby "$1" "$2" "$3" > /dev/null
		RESP="$?"
	elif [ $( echo "$1" | egrep ".py$" ) ]; then
		python "$1" "$2" "$3" > /dev/null
		RESP="$?"
	elif [ $( echo "$1" | egrep ".cpp$" ) ]; then
		g++ "$1" -O2 -lm
		./a.out "$2" "$3" > /dev/null
		RESP="$?"
		rm -f a.out
	fi
	if [ "$RESP" -eq 0 ]; then
		echo "Checagem OK."
	else
		echo "Erro detectado !!!"
		echo "Execute os verificadores manualmente para mais detalhes."
		exit 2
	fi
}


# Assume que no diretorio principal existem os diretorios "boca" e "scripts"
if [ !	 -d "boca" -a -d "scripts" ]; then
	echo "!!! Este script deve ser rodado a partir do diretorio que contem os diretorios dos problemas !!!" 
	exit 4
fi
	

# Se nao for passado os problemas a serem finalizados como parametro,
# entao executa para todos os problemas
PSET=""
if [ "$1" != "" ]; then
	while [ "$1" != "" ]; do
		PSET="$PSET $1"
		shift
	done
else
	for x in $( ls ); do
		if [ -d "$x" -a "$x" != "esqueleto" -a "$x" != "scripts" -a "$x" != "boca" ]; then
			PSET="$PSET $x"
		fi
	done
fi


# for p in $PSET; do 
# 	echo "rm -f $p/*~"
# 	echo "rm -f $p/checkers/*~"
# 	echo "rm -f $p/docs/*~"
# 	echo "rm -f $p/generator/*~"
# 	echo "rm -f $p/sols/*~ "
# done

for prob in $PSET; do
	echo ""
	echo "Finalizando entrada/saida de $prob"
	# note que a linha abaixo resultara em um arquivo errado se o
	# padrao de nomes de arquivos nao for seguido corretamente
	echo "Gerando arquivo de entrada final..."
	cat "$prob"/tests/in[0-9]* > "$prob/tests/final.in"
	
	# Supondo que sempre existira solucao em C ou C++
	echo "Compilando solucao AC..."
	ac=$( ls "$prob"/sols/ | egrep "ac.c" | head -n 1 )
	if [ "$ac" ==  "" ]; then
		echo "Quero uma solucao AC em C/C++ !!!"
		exit 5
	fi
	if [ $(echo "$ac" | grep "ac.cpp") ]; then
		g++ "$prob"/sols/"$ac" -O2 -lm
	else
		gcc "$prob"/sols/"$ac" -O2 -lm
	fi
	echo "Gerando arquivo de saida final..."
	./a.out < "$prob/tests/final.in" > "$prob/tests/final.out"
	echo "Apagando binario AC..."
	rm -f a.out

	chk="./$( ls $prob/checkers/chk-input.* 2> /dev/null )"
	if [ -f "$chk" ]; then
		executaChk "$chk" "$prob/tests/final.in" ""
	fi
	chk="./$( ls $prob/checkers/chk-output.* 2> /dev/null )"
	if [ -f "$chk" ]; then
		executaChk "$chk" "" "$prob/tests/final.out"
	fi
	chk=./$( ls "$prob"/checkers/chk-io.* 2> /dev/null )
	if [ -f "$chk" ]; then
		executaChk "$chk" "$prob/tests/final.in" "$prob/tests/final.out"
	fi
	echo "-------------------------------------------------------"
done

