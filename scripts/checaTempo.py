#!/usr/bin/env python3

#
# Autor: Gabriel Peixoto
# Atualizacoes: 
#   Marcio T. I. Oshiro 06/04/2015 --> cada codigo java tem seu proprio diretorio
#   Marcio T. I. Oshiro 07/04/2015 --> adaptacao para ser chamado por outro script
#   Marcio T. I. Oshiro 07/04/2015 --> mudanca no tempo sugerido
#   Marcio T. I. Oshiro 25/04/2015 --> classe Times e remocao da sugestao de tempo
#

import os
import sys
import subprocess
import argparse
import re
import math
import threading

INF = float('inf')

class Arguments:
    def __init__(self, t = 10, i = 'final.in', o = 'final.out', p = '.'):
        self.time_limit = t
        self.input = i
        self.output = o
        self.problem = p


class Times:
    def __init__(self, language):
        self.ac_max = 0
        self.ac_av = -1
        self.tle_min = INF
        self.lang = language


class RunCommand(threading.Thread):
    def __init__(self, cmd, input_path, output_path):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.input_path = input_path
        self.output_path = output_path
        self.time_spent = None
        self.proc = None

    def run(self):
        with open(self.input_path, 'rb') as fin:
            with open(self.output_path, 'wb') as fout:
                with open(os.devnull, 'wb') as devnull:
                    # start_time = os.times()[2]
                    start_time = os.times()
                    self.proc = subprocess.Popen(self.cmd, stdin = fin,
                                                 stdout = fout,
                                                 stderr = devnull)
                    self.proc.communicate()
                    # end_time = os.times()[2]
                    end_time = os.times()
        # self.time_spent = end_time - start_time
        self.time_spent = (end_time[1] + end_time[2]) - (start_time[1] + start_time[2])

    def stop(self):
        try:
            self.proc.terminate()
        except subprocess.ProcessLookupError:
            if self.proc.pool() is None:
                raise

# return a tupple (time_spent, output_data)
# If the program is killed after reaching time_limit
# then time_spent == INF
def execute_solution(cmd, input_path, output_path, time_limit):
    t = RunCommand(cmd, input_path, output_path)
    t.start()
    t.join(time_limit)
    if t.is_alive():
        t.stop()
        return(INF, None)

    with open(output_path, 'rb') as fp:
        return (t.time_spent, fp.read())


# Returns a tupple like execute_solution
def compile_and_run_cpp(source_path, input_path, time_limit):
    (exec_path, ext) = os.path.splitext(source_path)
    if ext == '.c':
        compiler = 'gcc'
    else:
        compiler = 'g++'
    subprocess.call([compiler, source_path, '-O2', '-o', exec_path])
    output_path = exec_path+'.out'
    ret = execute_solution([exec_path],
                           input_path, output_path,
                           time_limit)

    os.remove(exec_path)
    os.remove(output_path)
    return ret

# Returns a tupple like execute_solution
def compile_and_run_java(source_path, input_path, time_limit):
    (folder, base_source) = os.path.split(source_path)
    (class_name, ext) = os.path.splitext(base_source)

    subprocess.call(['javac', source_path])
    output_path = os.path.join(folder, class_name+'.out')
    ret = execute_solution(['java', '-classpath', folder, class_name], 
                           input_path, output_path,
                           time_limit)

    os.remove(os.path.join(folder, class_name+'.class'))
    os.remove(output_path)
    return ret

# Return an iterator over tupples
# (solution_path, time_spent, output_data)
# where (time_spent, output_data) is like execute_solution
def solutions_generator(input_path, time_limit):
    problem_name = os.path.split(os.getcwd())[1]
    for sol in os.listdir('sols'):
        (basename, ext) = os.path.splitext(sol)
        if ext in ('.cpp', '.c'):
            (t, out) = compile_and_run_cpp(os.path.join('sols', sol), input_path, time_limit)
            yield (sol, t, out)
        elif ext == '.java':
            (t, out) = compile_and_run_java(os.path.join('sols', sol, problem_name+'.java'), input_path, time_limit)
            yield (sol, t, out)


def process_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time-limit', type=int, default = 10,
                        help = 'Tempo (em segundos) depois do qual devemos parar uma solucao (padrao=10s)')
    parser.add_argument('-i', '--input', action='store', default = 'final.in',
                        help = 'Arquivo para usar de entrada (padrao = final.in)')
    parser.add_argument('-o', '--output', action='store', default = 'final.out',
                        help = 'Arquivo para usar de saida (padrao = final.out)')
    parser.add_argument('-p', '--problem', action='store', default = '.',
                        help = 'Arquivo para usar de saida (padrao = final.out)')
    return parser.parse_args()


def format_time(t, tl = 10):
    if not math.isfinite(t):
        return '> %d' % (tl) # inf
    return '{:.4f}'.format(t)

def check_times(args):
    if args.problem != '.' and os.path.split(os.getcwd())[1] != args.problem:
        os.chdir(args.problem)

    with open(os.path.join('tests', args.output), 'rb') as fp:
        output_data = fp.read()
    input_path = os.path.join('tests', args.input)


    cpp_time = Times(1)
    java_time = Times(2)
    sum_ac_cpp = 0
    n_ac_cpp = 0
    n_tle_cpp = 0
    sum_ac_java = 0
    n_ac_java = 0
    n_tle_java = 0

    for (sol, t, out) in solutions_generator(input_path, args.time_limit):
        equal = '' if out == output_data else 'WA ou TLE'
        sol_name = os.path.basename(sol)
        print('{:<20s} {:>7s} {}'.format(sol_name, format_time(t, args.time_limit), equal))

        if sol.endswith('.cpp') or sol.endswith('.c'):
            if re.search('ac\.c', sol):
                n_ac_cpp += 1
                cpp_time.ac_max = max(cpp_time.ac_max, t)
                sum_ac_cpp += t
            elif re.search('tle\.c', sol):
                n_tle_cpp += 1
                cpp_time.tle_min = min(cpp_time.tle_min, t)
        elif sol.endswith('.java'):
            if re.search('ac\.java', sol):
                n_ac_java += 1
                java_time.ac_max = max(java_time.ac_max, t)
                sum_ac_java += t
            elif re.search('tle\.java', sol):
                n_tle_java += 1
                java_time.tle_min = min(java_time.tle_min, t)

    print()
    if n_ac_cpp > 0:
        cpp_time.ac_av = sum_ac_cpp / n_ac_cpp
        print('Tempo maximo  AC em C/C++:', format_time(cpp_time.ac_max))
        print('Tempo medio  AC em C/C++:', format_time(cpp_time.ac_av))
    else:
        print('Sem codigo AC em C/C++ !?!?!?!?!?!?')
    if n_tle_cpp > 0:
        print('Tempo minimo TLE em C/C++:', format_time(cpp_time.tle_min))
    else:
        print('Sem codigo TLE em C/C++')
    if n_ac_java > 0:
        java_time.ac_av = sum_ac_java / n_ac_java
        print('Tempo maximo  AC em Java:', format_time(java_time.ac_max))
        print('Tempo medio  AC em Java:', format_time(java_time.ac_av))
    else:
        print('Sem codigo AC em Java')
    if n_tle_java > 0:
        print('Tempo minimo TLE em Java:', format_time(java_time.tle_min))
    else:
        print('Sem codigo TLE em Java')
    print()
    
    if os.path.split(os.getcwd())[1] == args.problem:
        os.chdir('..')    

    return (cpp_time, java_time)


if __name__ == '__main__':
    args = process_arguments()
    check_times(args)
