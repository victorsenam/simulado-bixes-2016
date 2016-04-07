#!/usr/bin/env python3

#
# Autor: Marcio T. I. Oshiro
# 
# Usado para gerar pacote do BOCA para um problema
# 

import os
import shutil
import re
import sys
import subprocess
from fractions import Fraction
from math import ceil


def copiaEsqueleto(prob, letra = ''):
    os.chdir('boca')
    if os.path.exists(letra+prob): # remove pacote existente para criar novo
        shutil.rmtree(letra+prob)
    shutil.copytree('probtemplate', letra+prob)
    os.chdir('..')

def ajustaDescricao(prob,letra = ''):
    with open(os.path.join(prob, 'docs', 'enunciado.tex'), 'r') as fp:
        enunciado = fp.read()
    # vai dar erro na linha abaixo se existir quebra de linha no nome do problema no enunciado
    nome_completo = re.search(r"Letra: (.*?)(\}|\\footnote)", enunciado).group(1)
    nome_curto = re.search(r"arquivoProblema\{(.*?)\}", enunciado).group(1)
    print('-  basename = %s\n-  fullname = %s' % (nome_curto, nome_completo))
    if re.search(r"\\|\{|\}|\$", nome_completo):
        usar = input('   Caracteres suspeitos no fullname.\n   Digite novo nome ou deixe vazio para mante-lo: ')
        if usar != '':
            nome_completo = usar

    with open(os.path.join('boca', letra+prob, 'description', 'problem.info'), 'w') as fp:
        fp.write('basename=%s\nfullname=%s\n\n' % (nome_curto, nome_completo))


def copiaES(prob, letra = ''):
    shutil.copy(os.path.join(prob, 'tests', 'final.in'),
        os.path.join('boca', letra+prob, 'input', 'file1'))
    shutil.copy(os.path.join(prob, 'tests', 'final.out'),
        os.path.join('boca', letra+prob, 'output', 'file1'))


def ajustaTLE(prob, letra = ''):
    args = checaTempo.Arguments()
    args.problem = prob

    cpp_time, java_time = checaTempo.check_times(args)

    # multiplicadores semi-arbitrarios
    if cpp_time.ac_av != -1:
        tempo = cpp_time.ac_av * 3
    else:
        tempo = java_time.ac_av * 1.3
    cpp_tl, cpp_repetition = aproximaParaInteiro(tempo)
    if java_time.ac_av != -1:
        tempo = java_time.ac_av * 2
    else:
        tempo = cpp_time.ac_av * 4
    java_tl, java_repetition = aproximaParaInteiro(tempo)
    memory_repetition = 512
    file_size = 1024

    print('Sugestao para C/C++: %ds para %d repeticoes (~%.4f por rep.)' % (cpp_tl, cpp_repetition, cpp_tl/cpp_repetition))
    print('Sugestao para JAVA: %ds para %d repeticoes (~%.4f por rep.)' % (java_tl, java_repetition, java_tl/java_repetition))
    usar = input('Usar sugestao? ([s]/n): ')

    if usar == 'n' or usar == 'N':
        usar = input('TL para C/C++ no formato <tempo_em_segundos_int> [num_repeticoes]: ')
        cpp_tl, cpp_repetition = map(int, usar.split())
        usar = input('TL para JAVA no formato <tempo_em_segundos_int> [num_repeticoes]: ')
        java_tl, java_repetition = map(int, usar.split())

    with open(os.path.join('boca', letra+prob, 'limits', 'c'), 'w') as fp:
        fp.write('#!/bin/bash\necho %d\necho %d\necho %d\necho %d\necho 0\n' % 
            (cpp_tl, cpp_repetition, memory_repetition, file_size))
    with open(os.path.join('boca', letra+prob, 'limits', 'cpp'), 'w') as fp:
        fp.write('#!/bin/bash\necho %d\necho %d\necho %d\necho %d\necho 0\n' % 
            (cpp_tl, cpp_repetition, memory_repetition, file_size))
    with open(os.path.join('boca', letra+prob, 'limits', 'java'), 'w') as fp:
        fp.write('#!/bin/bash\necho %d\necho %d\necho %d\necho %d\necho 0\n' % 
            (java_tl, java_repetition, memory_repetition, file_size))


# Tenta encontrar o menor numero de vezes que eh preciso
# executar o teste para o tempo total ser o mais proximo 
# possivel de um inteiro menor que max_time.
# O tempo de uma execucao eh x.
# Devolve (tempo_total, numero_de_execucoes)
def aproximaParaInteiro(x, max_time = 12):
    if x > 9.9999:
        return (ceil(x), 1)

    eps = 0.2
    max_tempo = 10
    max_rep = 50
    frac = Fraction(x).limit_denominator(max_rep)
    tempo = frac.numerator
    if tempo >= 1 and tempo <= max_tempo:
        melhor_rep = frac.denominator
        melhor_tempo = tempo
    else:
        melhor_rep = -1
        melhor_tempo = max_tempo + 1
    rep = frac.denominator
    while tempo > 1 and rep > 1:
        frac = Fraction(x).limit_denominator(rep - 1)
        rep = frac.denominator
        tempo = frac.numerator
        if abs(x - float(frac)) < eps and tempo < melhor_tempo:
            melhor_rep = rep
            melhor_tempo = tempo

    if melhor_rep == -1 or melhor_tempo > max_tempo:
        melhor_rep = 1
        melhor_tempo = ceil(x)
    if melhor_tempo == 0:
        melhor_tempo = 1
        melhor_rep = 50

    return (melhor_tempo, melhor_rep)

def zipaPacote(prob,letra = ''):
    os.chdir(os.path.join(os.getcwd(), 'boca', letra+prob))
    nome = os.path.join('..', letra+prob+'-pack.zip')
    subprocess.call('zip -r '+nome+' * > /dev/null', shell=True)
    os.chdir(os.path.join('..', '..'))

def empacota(prob, letra = ''):
    print('Empacotando %s' % (prob))
    print('Copiando esqueleto...')
    copiaEsqueleto(prob, letra)
    print('Ajustando descricao...')
    ajustaDescricao(prob, letra)
    print('Copiando arquivos de entrada e saida...')
    copiaES(prob, letra)
    print('Verificando tempo dos codigos...')
    ajustaTLE(prob, letra)
    print('Zipando...')
    zipaPacote(prob, letra)
    print('------------------------------------')
    
def todosProblemas():
    todos = []
    for p in os.listdir('.'):
        if os.path.isdir(p):
            todos += [p]

    todos.remove('esqueleto')
    todos.remove('boca')
    todos.remove('scripts')
    return todos

if __name__ == '__main__':
    scripts_dir = os.path.split(sys.argv[0])[0]
    if scripts_dir != 'scripts' and scripts_dir != './scripts':
        print(scripts_dir)
        raise NameError('Este script deve ser executado no diretorio que contem os problemas.\nNao parece ser o caso.')


    scripts_dir = os.path.join(os.getcwd(), scripts_dir)
    sys.path.append(scripts_dir)
    import checaTempo

    if len(sys.argv) == 1:
        probs = todosProblemas()
        for prob in probs:
            empacota(prob)
    else:
        empacota(sys.argv[1])


    