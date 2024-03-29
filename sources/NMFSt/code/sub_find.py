import json

from Bio import Phylo
from Bio import *
from dendropy import Tree
import shutil, os

from dfa_lib_python.dataflow import Dataflow
from dfa_lib_python.transformation import Transformation
from dfa_lib_python.attribute import Attribute
from dfa_lib_python.attribute_type import AttributeType
from dfa_lib_python.set import Set
from dfa_lib_python.set_type import SetType
from dfa_lib_python.task import Task
from dfa_lib_python.dataset import DataSet
from dfa_lib_python.element import Element
from dfa_lib_python.program import Program

INPUT_PATH = '/home/luiz/Pycharm/MAESTRO - NMFSt P/sources/NMFSt/data/out/Trees'
DATA_OUTPUT_PATH = '/home/luiz/Pycharm/MAESTRO - NMFSt P/sources/NMFSt/data/out/Subtrees'

DATA_FORMAT = 'nexus'  # newick ou nexus
match DATA_FORMAT:
    case 'nexus':
        EXTENTION_FORMAT = 'nexus'  # Nexus: 'nexus'

    case 'nwk':
        EXTENTION_FORMAT = 'nwk'  # Newick: 'nwk'

# Limpeza
def clean_dir(path_clean):
    if(os.path.exists(path_clean)):
        for name in os.listdir(path_clean):
            if(name != "file.gitkeep"):
                file_path = os.path.join(path_clean, name)
                os.remove(file_path)
        shutil.rmtree(path_clean)

def clean_files():
    dir_tmp = os.path.join(DATA_OUTPUT_PATH)
    arquivos_tmp = os.listdir(dir_tmp)
    for name_file in arquivos_tmp:
        if name_file != "file.gitkeep":
            os.remove(os.path.join(dir_tmp,name_file))

clean_files()

# Exibe subárvore
def print_trees_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".nexus"):
            filepath = os.path.join(directory, filename)

            print(filename.upper() + "\n")
            tree = Tree.get_from_path(filepath, DATA_FORMAT)
            tree.print_plot()

# Construtor de subárvores
def sub_tree(path, name_subtree):
    # Salva a árvore
    tree = Phylo.read(path, DATA_FORMAT)
    name_subtree = name_subtree.rsplit(".", 1)[0]

    # Lista caminhos das subárvores (que posteriormente serão utilizadas para compor a matriz de subárvores)
    row_subtree = []

    for clade in tree.find_clades():
        subtree = Phylo.BaseTree.Tree(clade)
        if subtree.count_terminals() > 1:
            filepath_out = os.path.join(DATA_OUTPUT_PATH, f'{name_subtree}_{clade.name}.{EXTENTION_FORMAT}')
            Phylo.write(subtree, filepath_out, DATA_FORMAT)
            row_subtree.append(filepath_out)

    return row_subtree

def directory_has_single_file(directory_path):
    if not os.path.isdir(directory_path):
        return False

    files = os.listdir(directory_path)
    if len(files) != 1:
        return False

    return True

# Chamada de funções
# ATENÇÃO: SE A ÁRVORE DE ENTRADA NÃO TIVER FORMATO NEXUS, MUDAR O SCHEMA EM Phylo.write( )
# Diretório de entrada de árvores
arquivos = os.listdir(INPUT_PATH)

# matriz com todas as subárvores
matriz_subtree = []

for name_file in arquivos:
    if(name_file != "file.gitkeep"):
        dir_path_out_epsecif = os.path.join(DATA_OUTPUT_PATH,name_file.split(".")[0])
        file_path = os.path.join(INPUT_PATH,name_file)
        print("===> name file: ",name_file)
        matriz_subtree.append(sub_tree(file_path, name_file))

# máximo de colunas
max_columns = max(len(row) for row in matriz_subtree)
# máximo de linhas
max_rows = len(matriz_subtree)

def preencher_matriz(matriz, valor_preenchimento):
    # Preencher as células vazias com o valor de preenchimento
    for row in matriz:
        while len(row) < max_columns:
            row.append(valor_preenchimento)

    return matriz

print(max_rows, max_columns)

matriz_subtree = preencher_matriz(matriz_subtree, None)

for linha in matriz_subtree:
    print("linha ",linha)

# Comparação das subárvores
def grade_maf(path_1, path_2):
    if (path_1 is None or path_2 is None):
        return -1
    grau = 0

    subtree_1 = Phylo.read(path_1, DATA_FORMAT)
    subtree_2 = Phylo.read(path_2, DATA_FORMAT)

    # Lista todas as clades ( folhas )
    list_1 = [i.name for i in subtree_1.get_terminals()]
    list_2 = [i.name for i in subtree_2.get_terminals()]

    sorted_list1 = sorted(list_1)
    sorted_list2 = sorted(list_2)

    for i in range(len(list_1)):
        for j in range(len(list_2)):
            if sorted_list1[i] == sorted_list2[j]:
                grau += 1
    return grau

dict_maf_database = {}

def fill_dict(dict, max_columns):
    for i in range(max_columns):
        dict[i+1] = {}

    return dict_maf_database

dict_maf_database = fill_dict(dict_maf_database,max_columns)
print("====================",dict_maf_database)

max_maf = 0
for i in range(max_rows):
    for j in range(max_columns):
        dict_aux = {}
        for k in range(max_rows):
            for l in range(max_columns):
                if i != k:
                    if max_maf <= grade_maf(matriz_subtree[i][j],matriz_subtree[k][l]):
                        max_maf = grade_maf(matriz_subtree[i][j],matriz_subtree[k][l])

                    g_maf = grade_maf(matriz_subtree[i][j], matriz_subtree[k][l])
                    if g_maf is not False and g_maf >= 1:
                        if g_maf not in dict_maf_database:
                            dict_maf_database[g_maf] = {}
                        if matriz_subtree[i][j] not in dict_maf_database[g_maf]:
                            dict_maf_database[g_maf][matriz_subtree[i][j]] = []
                        dict_maf_database[g_maf][matriz_subtree[i][j]].append(matriz_subtree[k][l])
print(max_maf)

for i, j in dict_maf_database.items():
    print("==>",i,j)
    task = Task(2, "NMFSt", "Act_sub_tree")
    task_input = DataSet("iAct_sub_tree", [Element(["att_alignment"])])
    task.add_dataset(task_input)
    task.begin()
    json_string = json.dumps(j)
    json_string = json_string.replace("'", '"')

    task_output = DataSet("oAct_sub_tree", [Element([json_string])])
    task.add_dataset(task_output)
    task.end()
    for key, val in j.items():
        # print(i, key, val)
        continue
# arquivo.close()