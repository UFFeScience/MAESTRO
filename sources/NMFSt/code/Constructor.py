#!/usr/bin/env python
# coding: utf-8

# <h2 align="center"><b>ALINHAMENTO E GERAÇÃO DE ÁRVORE FILOGENÉTICA</b></h2>
# <p align="center"><b>IMPORTANTE LEMBRAR:</b></p>
# 
# - É necessário ter o clustalw instalado
# - Sequências de proteínas devem ser fornecidas do diretório especificado em `input_path`
# - O formato das Sequências de proteínas deve ser especificado em `OUTPUT_FORMAT`
# 
# <h3 align="center"><b>IMPORTS E CONFIGURAÇÃO DO DIRETÓRIO BASE</b></h3>

# In[ ]:


from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO, Phylo, SeqIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import os
from pathlib import Path

# Substitua pelo caminho do diretório que você deseja listar e o formato das seqências
INPUT_PATH = 'testset' 
OUTPUT_FORMAT = 'nexus' # newick ou nexus
match OUTPUT_FORMAT:
    case 'nexus':
        EXTENTION_FORMAT = 'nexus' # Nexus: 'nexus'
   
    case 'nwk':
        EXTENTION_FORMAT = 'nwk' # Newick: 'nwk'

DATA_PATH = '../data'
DATA_OUTPUT_PATH = '../data/out'

# listagem de arquivos
dir = os.path.join(DATA_PATH, INPUT_PATH)
files = os.listdir(dir)


# <h3 align="center"> <b>LIMPEZA</b> </h3>

# In[ ]:


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


# <h3 align="center"> <b>VALIDADORES</b> </h3>
# 

# In[ ]:


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


# <h3 align="center"> <b>TRATAMENTO DE SEQUENCIA</b> </h3>
# 

# In[ ]:


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


# <h3 align="center"> <b>CONSTRUTUOR</b> </h3>
# 

# In[ ]:


# Mais informações sobre aplicações biopython e clustalwcommandline - https://biopython.org/docs/1.76/api/Bio.Align.Applications.html
def constructor_tree(path_in_fasta, path_out_aln, path_out_dnd, path_old_dnd, path_out_tree):
    # Executa o Clustalw para alinhar as sequências
    clustalw_cline = ClustalwCommandline("clustalw", infile=path_in_fasta, outfile=path_out_aln)# Executa o programa clustalw sem precisar da linha de comando.
    clustalw_cline()#  Executa o comando ClustalW com base nos parâmetros definidos no objeto ClustalwCommandline e retorna os resultados da execução na forma de uma tupla de strings.

    # Mover o arquivo de saída .dnd para o diretório "resultados"
    os.rename(path_old_dnd, path_out_dnd)

    '''
    Clustalw_cline() - gera 2 arquivos de saida por padrão

    Nesse caso:
    - ORTHOMCL256.aln: Contendo a sequência de ORTHOMCL256 alinhada em formato clustal
    - ORTHOMCL256.dnd: Contendo informações sobre o agrupamento hierárquico das sequências alinhadas.
    '''

    # Abre o arquivo de alinhamento
    with open(path_out_aln, "r") as handle:
        alignment = AlignIO.read(handle, "clustal")# O objeto MultipleSeqAlignment retornado é armazenado na variável.

    # Calcula a matriz de distância
    # argumento 'identity', que indica que a distância entre as sequências será medida pelo número de identidades, ou seja, a fração de posições nas sequências que possuem o mesmo nucleotídeo ou aminoácido.
    calculator = DistanceCalculator('identity') 
    # Calcula a matriz de distâncias entre as sequências
    distance_matrix = calculator.get_distance(alignment) 

    # Constrói a árvore filogenética
    # Constrói árvores filogenéticas a partir de matrizes de distâncias entre sequências.
    constructor = DistanceTreeConstructor() 
    tree = constructor.nj(distance_matrix)

    # Salva a árvore
    
    Phylo.write(tree, path_out_tree, OUTPUT_FORMAT)


# <h3 align="center"> <b>PERCORRER E MANIPULA DIRETORIO</b> </h3>
# 

# In[ ]:


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


# <h3 align="center"> <b>Limpeza arquivos temporários</b> </h3>
# 

# In[ ]:


clean_NoPipe()
clean_tmp()

