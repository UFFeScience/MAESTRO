# -*- coding: utf-8 -*-
"""Constructor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pes6iRDdninpARw4WkanvhTjw0e1gf7c

<h2 align="center"><b>ALINHAMENTO E GERAÇÃO DE ÁRVORE FILOGENÉTICA</b></h2>
<p align="center"><b>IMPORTANTE LEMBRAR:</b></p>

- É necessário ter o clustalw instalado
- Sequências de proteínas devem ser fornecidas do diretório especificado em `input_path`
- O formato das Sequências de proteínas deve ser especificado em `OUTPUT_FORMAT`

<h3 align="center"><b>IMPORTS E CONFIGURAÇÃO DO DIRETÓRIO BASE</b></h3>
"""
import argparse
import sys

from Bio import SeqIO, AlignIO, Phylo
from Bio.Align.Applications import ClustalwCommandline
import Bio
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import os
from pathlib import Path

# parser = argparse.ArgumentParser(description='Descrição do script.')
# parser.add_argument('arg1', type=str, help='dataset de entrada')
# parser.add_argument('arg2', type=str, help='formato da saida')
# parser.add_argument('arg3', type=str, help='programa')
#
# args = parser.parse_args()

# arg1 e arg 2 sao passados no wf.py e são o dataset e o formato respectivamente
INPUT_PATH = 'testset'
OUTPUT_FORMAT = 'nexus'  # newick ou nexus
match OUTPUT_FORMAT:
    case 'nexus':
        EXTENTION_FORMAT = 'nexus'  # Nexus: 'nexus'

    case 'nwk':
        EXTENTION_FORMAT = 'nwk'  # Newick: 'nwk'

DATA_PATH = '../data'
DATA_OUTPUT_PATH = '../data/out'

# listagem de arquivos
dir = os.path.join(DATA_PATH, INPUT_PATH)
files = os.listdir(dir)
print(os.system("ls"))
print(os.path.abspath(dir))

"""<h3 align="center"> <b>LIMPEZA</b> </h3>"""

def clean_Trees():
    dir_Trees = os.path.join(DATA_OUTPUT_PATH,'Trees')
    file_trees = os.listdir(dir_Trees)

    for name_file_trees in file_trees:
        path_trees = os.path.join(dir_Trees,name_file_trees)
        if name_file_trees != "file.gitkeep":
            os.remove(path_trees)

def clean_tmp():
    dir_tmp = os.path.join(DATA_OUTPUT_PATH,'tmp')
    files_tmp = os.listdir(dir_tmp)

    for name_file_tmp in files_tmp:
        path_tmp = os.path.join(dir_tmp,name_file_tmp)
        if name_file_tmp != "file.gitkeep":
            os.remove(path_tmp)


def clean_NoPipe():
    dir_NoPipe = os.path.join(DATA_PATH, INPUT_PATH)

    for file_name in os.listdir(dir_NoPipe):
        if 'NoPipe' in file_name:
            file_path = os.path.join(dir_NoPipe, file_name)
            os.remove(file_path)

clean_NoPipe()
clean_tmp()
clean_Trees()

"""<h3 align="center"> <b>VALIDADORES</b> </h3>

"""

#Função que verifica se todas as sequências são proteínas válidas no formato FASTA"""
def validate_sequences(file_path):
    # Define os caracteres válidos para uma sequência de proteína.
    valid_characters = set('ACDEFGHIKLMNPQRSTVWY')
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('>'):
                    continue  # Pula a linha de cabeçalho
                sequence = line.strip()
                if not set(sequence).issubset(valid_characters):
                    return False
    except FileNotFoundError:
        print(f"O arquivo '{file_path}' não foi encontrado.")
        return False

    return True

def duplicate_names(file_path):
    name_count = {}
    try:
        for record in SeqIO.parse(file_path, 'fasta'):
            name = record.id
            name_count[name] = name_count.get(name, 0) + 1
            if name_count[name] > 1:
                return True
    except FileNotFoundError:
        print(f"O arquivo '{file_path}' não foi encontrado.")
        return False

    return False

"""<h3 align="center"> <b>TRATAMENTO DE SEQUENCIA</b> </h3>

"""

def remove_pipe(name, path_in_fasta):
    sequences = list(SeqIO.parse(path_in_fasta, "fasta"))
    # Criar um dicionário para armazenar as sequências únicas
    unique_sequences = {}
    # Iterar pelas sequências do arquivo de entrada
    for sequence in sequences:
        # Verificar se a sequência já existe no dicionário de sequências únicas
        if str(sequence.seq) not in unique_sequences:
            # Se a sequência é única, armazená-la no dicionário
            unique_sequences[str(sequence.seq)] = sequence
    # Criar uma lista de sequências únicas
    unique_sequences_list = list(unique_sequences.values())
    # Salvar as sequências únicas em um arquivo de saída
    output_file_tmp = os.path.join(DATA_PATH,INPUT_PATH,f'{name}_NoPipe')
    SeqIO.write(unique_sequences_list, output_file_tmp, "fasta")
    return output_file_tmp

"""<h3 align="center"> <b>CONSTRUTUOR</b> </h3>

"""

# Mais informações sobre aplicações biopython e clustalwcommandline - https://biopython.org/docs/1.76/api/Bio.Align.Applications.html
from Bio.Align.Applications import MafftCommandline
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

def constructor_tree(path_in_fasta, path_out_aln, path_out_dnd, path_old_dnd, path_out_tree):
    # Executa o MAFFT para alinhar as sequências
    print("==> ",path_out_aln)

    mafft_cline = MafftCommandline("mafft", input=path_in_fasta, auto=True, outfile=path_out_aln)
    stdout, stderr = mafft_cline()

    # Mover o arquivo de saída .dnd para o diretório "resultados"
    os.rename(path_old_dnd, path_out_dnd)

    # Abre o arquivo de alinhamento
    with open(path_out_aln, "r") as handle:
        alignment = AlignIO.read(handle, "fasta")

    # Calcula a matriz de distância
    calculator = DistanceCalculator('identity')
    distance_matrix = calculator.get_distance(alignment)

    # Constrói a árvore filogenética
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(distance_matrix)

    # Salva a árvore
    Phylo.write(tree, path_out_tree, "newick")


"""<h3 align="center"> <b>PERCORRER E MANIPULA DIRETORIO</b> </h3>

"""

OUTPUT_PATH_TREES = '../data/out/Trees'
OUTPUT_PATH_TMP = '../data/out/tmp'
OUTPUT_PATH_MAF = '../data/out/tmp'

for name_file in files:
    #configurando caminhos relativos padrões do diretorio
    path_in_fasta = os.path.join(DATA_PATH,INPUT_PATH,name_file)
    path_out_aln = os.path.join(OUTPUT_PATH_TMP,f'{Path(name_file).stem}.aln')
    path_out_dnd = os.path.join(OUTPUT_PATH_TMP,f'{Path(name_file).stem}.dnd')
    path_old_dnd = os.path.join(DATA_PATH,INPUT_PATH,f'{Path(name_file).stem}.dnd')
    path_out_tree = os.path.join(OUTPUT_PATH_TREES,f'tree_{Path(name_file).stem}.{OUTPUT_FORMAT}')

    if not(duplicate_names(path_in_fasta)) and validate_sequences(path_in_fasta):
        constructor_tree(path_in_fasta, path_out_aln, path_out_dnd, path_old_dnd, path_out_tree)
    else:
        path_in_fasta = remove_pipe(Path(name_file).stem, path_in_fasta)
        path_old_dnd = os.path.join(f'{path_in_fasta}.dnd')

        constructor_tree(path_in_fasta, path_out_aln, path_out_dnd, path_old_dnd, path_out_tree)

"""<h3 align="center"> <b>Limpeza arquivos temporários</b> </h3>

"""

clean_NoPipe()
clean_tmp()