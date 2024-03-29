# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for functions, files, tool windows, actions, and settings.
import os
import statistics

import owlready2
from owlready2 import *
import subprocess
import time
import os, sys, re, shutil as sh, optparse, time, datetime, threading
import sys, random, string, psutil, subprocess, json
import getopt
from optparse import OptionParser

from psutil._common import bytes2human

from functions.AbstractExpLine import *
from functions.Activity import createActivity
from functions.Attribute import *
from functions.DerivationByOptionality import *
from functions.DomainOperation import *
from functions.Port import *
from functions.Program import *
from functions.Relation import *
from functions.Metadata import *
from functions.ConcreteDerivation import *
from functions.AbstractWf import *
from functions.ProvenanceCalls import *
from functions.Experiment import *
# from maestro_analysis import find_data_tranformation_telemetry_metrics, find_program_telemetry_metrics, search_data, \
#     search_by_domain_operation
from sources.TemplateExecution import createTemplate
# from dfa_lib_python-OLD.dataflow import Dataflow
import glob


global dataflow
def cleanOntology(ontoexpline):
    busca = ontoexpline.search(type=ontoexpline.Experiment_Line)
    print("|*** Instancias Expline deletadas para iniciar: ", busca)
    for individual in busca:
        destroy_entity(individual)
        # print(individual)

    busca = ontoexpline.search(type=ontoexpline.ProvOne)
    print("|*** Instancias ProvONE deletadas para iniciar: ", busca)
    # print(busca)
    for individual in busca:
        destroy_entity(individual)
        print(individual)
    ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
def cleanActivityDirectory():
    files = glob.glob('sources/activities/*')
    for f in files:
        os.remove(f)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    df = Dataflow('NMFST')
    ontoexpline = get_ontology("ontologies/ontoexpline.owl").load()
    cleanOntology(ontoexpline)
    # cleanActivityDirectory()

    dataflow = createExperiment(ontoexpline, "NMFSt")

    ###########################################################################################
    # Definindo as operações de domínio EDAM
    op_validation = domainOperation(ontoexpline, "Sequencing_quality_control")
    op_alignment = domainOperation(ontoexpline, "Sequence_alignment_operation_0292")
    op_conversion = domainOperation(ontoexpline, "Sequence_alignment_conversion_operation_0260")
    op_model = domainOperation(ontoexpline, "Sequence_alignment_refinament_operation_2089")
    op_tree = domainOperation(ontoexpline, "Phylogenetic_tree_generation_operation_0547")

    ###########################################################################################
    #Definindo dependências de atividade
    # Atributo e porta de entrada
    att_sequences_input_path = createAttribute(ontoexpline, "ATT_INPUT_SEQUENCE")  # atributo sequencia de entrada
    port_path_sequences = createPort(ontoexpline, "full_dataset_plasmodium")  # arquivo consumido pelo programa
    associatePortAtt(port_path_sequences, att_sequences_input_path)  # associando att na porta

    att_sequences_output_format = createAttribute(ontoexpline, "ATT_SEQUENCES_OUTPUT_FORMAT")  # atributo sequencia de entrada
    port_sequences_output_format = createPort(ontoexpline, "nexus")  # arquivo consumido pelo programa
    associatePortAtt(port_sequences_output_format, att_sequences_output_format)  # associando att na porta


    # Atributo e porta de saída
    att_tree_output = createAttribute(ontoexpline, "ATT_TREE_OUTPUT")  # atributo sequencia de entrada
    port_tree = createPort(ontoexpline, "PORT_TREE")  # arquivo consumido pelo programa
    associatePortAtt(port_tree, att_tree_output)  # associando atributo a porta

    # relações de I/O
    rel_input_tree_gen = createRelation(ontoexpline, "REL_INPUT_TREE_GEN")  # relação de entrada
    rel_output_tree_gen = createRelation(ontoexpline, "REL_OUTPUT_TREE_GEN")

    # associações de itens abstratos e concretos
    associateRelationAtt(rel_input_tree_gen, [att_sequences_input_path, att_sequences_output_format])
    associateRelationAtt(rel_output_tree_gen, [att_tree_output])

    # definindo implementador para a atividade a ser criada
    clustalw = createProgram(ontoexpline, "ClustalW", op_tree, "constructor2.py", dataflow)
    associateProgramPort(clustalw, [port_path_sequences, port_sequences_output_format], [port_tree])
    clustalw.hasRetrospectiveCall = [False]

    ###########################################################################################
    #instanciando a atividade 1
    act_tree_generation = createActivity(ontoexpline, "Act_tree_gen", op_tree, [rel_input_tree_gen],

                         [rel_output_tree_gen], False, [clustalw], True, dataflow)

    ###########################################################################################

    att_subtrees = createAttribute(ontoexpline, "ATT_SUBTREES")  # atributo sequencia de entrada
    port_subtrees = createPort(ontoexpline, "PORT_SUBTREES")  # arquivo gerado pelo programa
    associatePortAtt(port_subtrees, att_subtrees)  # associando att na porta

    rel_output_subtrees = createRelation(ontoexpline, "REL_OUTPUT_SUBTREES")
    associateRelationAtt(rel_output_subtrees, [att_subtrees])

    subtree_program = createProgram(ontoexpline, "SubTree_Program", op_tree, "sources/NMFSt/code/sub_find.py", dataflow)
    associateProgramPort(subtree_program, [port_tree], [port_subtrees])
    subtree_program.hasRetrospectiveCall = [False]

    ###########################################################################################
    # instanciando a atividade 2
    act_sub_trees_generation = createActivity(ontoexpline, "Act_sub_tree", op_tree, [rel_output_tree_gen],

                                         [rel_output_subtrees], False, [subtree_program], False, dataflow)

    ###########################################################################################


# searchByDomainOperation(ontoexpline, op_tree, parameters={"attribute":"ATT_TREE_OUTPUT", "port_value": "tree_ORTHOMCL371" })
# searchByDomainOperation_out(ontoexpline, op_tree, parameters={"attribute":"ATT_FILE", "port_value": "ORTHOMCL256" })
#
# "../data/out/Trees/tree_ORTHOMCL256.nexus"
# {
#     "Dataflows” :
#     {
#         "Operation": "Tree_Generation",
#         "Dataflow_id": 1,
#         "Attribute:": "Tree_output",
#         "Value": "tree_ORTHOMCL371",
#         "Tasks_exec_id": 8,
#     }
# }

{
    "Dataflows” :
   {
       "Operation": "Tree_Generation",
       "Dataflow_id": 1,
       "Attribute:": "Att_file",
       "Value": "nexus",
       "Tasks_exec_id": [1, 2, 3, 4,5,6]
   }
}



ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")

absWfUser= [act_tree_generation, act_sub_trees_generation]
x = isValid(ontoexpline, absWfUser)
abs_wf = absWfDependences(ontoexpline, absWfUser)
absWfToConcreteWf(ontoexpline, absWfUser, [[], []])
createProvenanceCalls(ontoexpline, abs_wf, dataflow,[[], []])


# showExpLine() #está ok
# abstractDerivationByOptionality(ontoexpline) #está ok, ainda não plota o gráfico

# createTemplate(ontoexpline, remove_pipe) #está ok, insere chamadas retrospectiva nos scripts - inserir essas chamadas na função de derivação
# createTemplate(ontoexpline, mafft)
# createTemplate(ontoexpline, mrbayes)


# inicio = time.time()
# absWfUser= [aa, aa2, aa3, aa4, aa5]
# x = isValid(ontoexpline, absWfUser)
#
# print("|----------------------------------------------------|")
# abs_wf = absWfDependences(ontoexpline, absWfUser)
# # print("DEPENDENCES: ", abs_wf)
# # print("|*** Executed file: ",os.path.basename(__file__),"\n")
# print("|----------------------------------------------------|")
# absWfToConcreteWf(ontoexpline, absWfUser, [[aa2, mafft], [aa5, mrbayes]])
# print("|----------------------------------------------------|")
# createProvenanceCalls(ontoexpline, abs_wf, dataflow, [[aa2, mafft], [aa5, mrbayes]])
# print("|----------------------------------------------------|")









# #Função para retornar elementos que estão na ontologia
# # print("\nWF abstrato [[atividade, [dependências]]]: ",abs_wf)
# print("** ",abs_wf)

# createProvenanceCalls(ontoexpline, abs_wf, dataflow, [[aa2, mafft], [aa5, mrbayes]])
# fim = time.time()
# print("===> Tempo para derivar e criar chamadas de proveniencia:", fim-inicio)

# isValid(ontoexpline, [aa, aa2, aa3, aa4, aa5])
# getAbsWf(ontoexpline, [aa, aa2, aa3, aa4, aa5])
# getVariabilities(ontoexpline, [aa, aa2, aa3, aa4, aa5])
# getOptionalities(ontoexpline, [aa, aa2, aa3, aa4, aa5])
# getActivityCompatibilities(ontoexpline, aa2)
# getRelations(ontoexpline, aa2)
# getInputRelations(ontoexpline, aa2)
# getOutputRelations(ontoexpline, aa2)
# getAttributesConsumedByActivity(ontoexpline, aa2)
# getAttributesGeneratedByActivity(ontoexpline, aa2)
# getAttributesFromRelation(ontoexpline, rel_output_alignment)
# getPortConsumedByProgram(ontoexpline, mafft)
# getPortGeneratedByProgram(ontoexpline,mafft)
# getAttributeGeneratedByProgram(ontoexpline, converted_alignment_att)
# getAttributeGeneratedByProgram(ontoexpline, mafft)
# getProgramCompatibilities(ontoexpline, mafft)

###########################################################################################
# absIsValid([aax, aay,..., aaz]) -> verifica se o conjunto de atividades gera um wf válido (retorna booleano) - Check
# getAbsWf([ax, aay, ..., aaz]) -> retorna uma lista de atividades + suas dependências  (retorna lista) - check
# getVariabilities(abs_wf) -> retorna as variabilidades de um wf (retorna lista) - check
# getOptionailies(abs_wf) -> retorna as opcionalidades de um wf (retorna lista) - check
# getActivityCompatibilities(aa) --> retorna as compatibilidades de e/s de uma aa (retorna dicionario) - check
# absWfToConcreteWf(abs_wf) --> constroi o wf concreto (cria a sequencia de execução no arquivo wf.py) - check
# concreteIsValid(concreteWf, [aa, program]) (retorna booleano) - to do

###########################################################################################
# getRelations(aa) -> retorna relações de entrada saída de uma atividade (retorna dicionario) - check
# getInputRelations(aa) -> retorna as relações de entrada de uma atividade (retorna lista) - check
# getOutputRelations(aa) -> retorna as relações de saída de uma atividade (retorna lista) - check
# getAttributesConsumedByActivity(ontoexpline, aa2) -> retorna atributos consumidos por uma atividade (retorna lista de listas, pois consumir varias relações) - check
# getAttributesGeneratedByActivity(ontoexpline, aa2) -> retorna atributos gerados por uma atividade (retorna lista de listas pois pode gerar varias relações) - check
# getAttributesFromRelation(relation) -> retorna os atributos de uma relação (retorna lista) - check
# getPortConsumedByProgram(program) -> retorna as portas de um programa (retorna lista) - check
# getPortGeneratedByProgram(program) -> retorna portas geradas por um programa - (retorna lista) check
# getAttributeGeneratedByProgram(Att) -> retorna os programas que geram (relacionados) um atributo (retorna lista) - check
# getAttributeConsumedByProgram(program) -> retornam atributos consumidos (relacionados) por um programa (retorna lista) - check
# getProgramCompatibilities(Program) -> retorna programas que geram dados para o programa x, e programas que consomem dados gerados pelo programa x (retorna dicionario) - check

# cleanOntology(ontoexpline)
# ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
# Abstract_activity and (hasInputRelation some (Relation and composedBy value alignment_att)) and (hasOutputRelation some (Relation and composedBy value atribuxo_x or composedBy value evolutiveModel_att))
# inicio = time.time()
# owlready2.JAVA_EXE = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"
# ontoexpline = get_ontology("ontologies/ontoexpline.owl").load()
# with ontoexpline:
#     class Equivalence(ontoexpline.Entity):
#         equivalent_to = [ontoexpline.Abstract_activity and (ontoexpline.hasInputRelation.some(ontoexpline.Relation and ontoexpline.composedBy.value(ontoexpline.alignment_att))) and (ontoexpline.hasOutputRelation.some(ontoexpline.Relation and ontoexpline.composedBy.value(converted_alignment_att_eq)))]
#
#     ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
#     # close_world(Thing)
#
#     # sync_reasoner(infer_property_values = True)
#
#
# # eq = ontoexpline.Abstract_activity()
# eq = ontoexpline.search(type = ontoexpline.Equivalence)
# # print(eq)
# fim = time.time()
# print("===> Tempo para calculo da equivalencia:", fim-inicio)
# print(aa4, aa4.is_a)

# find_data_tranformation_telemetry_metrics(26)
# find_program_telemetry_metrics(read_seq, ontoexpline)
# find_program_telemetry_metrics(mafft, ontoexpline)
# find_program_telemetry_metrics(clustalw, ontoexpline)

# find_program_telemetry_metrics(mrbayes, ontoexpline)
# find_program_telemetry_metrics(raxml, ontoexpline)
# ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")

# find_program_telemetry_metrics(model_generator, ontoexpline)
#Program and (memoryUsageAverage some xsd:int[>6])
# with ontoexpline:
#     search = ontoexpline.search(type=ontoexpline.Program and ontoexpline.Phylogenetic_tree_generation_operation_0547)
#     program_list = []
#     for program in search:
#         if program.memoryUsageAverage:
#             metric = float(program.memoryUsageAverage)
#             program_list.append(metric)
#             print("programa na lista: ", program, " memory average: ", program.memoryUsageAverage)
#     print(program_list)
#     print(statistics.median(program_list))
#     for program in search:
#         if program.memoryUsageAverage and (float(program.memoryUsageAverage) < statistics.median(program_list)):
#             print("O programa ", program," é recomendado pois consome menor memoria que a média. \nMédia: ", bytes2human(statistics.median(program_list)), "\nMemoria consumida: ", bytes2human(program.memoryUsageAverage))
#             with ontoexpline:
#                 class Recomended(ontoexpline.Entity):
#                     recomended = [ontoexpline.Program and ontoexpline.memoryUsageAverage.value(program.memoryUsageAverage)]
#                 # recomended = [ontoexpline.Program and (ontoexpline.memoryUsageAverage.some(value.xsd.float < float(6)))]
#                 ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
#
#         # class Recomended(ontoexpline.Entity):
#     #     equivalent_to = [ontoexpline.Abstract_activity and (ontoexpline.hasInputRelation.some(ontoexpline.Relation and ontoexpline.composedBy.value(ontoexpline.alignment_att))) and (ontoexpline.hasOutputRelation.some(ontoexpline.Relation and ontoexpline.composedBy.value(converted_alignment_att_eq)))]
#     #
#     # ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
#     # close_world(Thing)
#
#     # sync_reasoner(infer_property_values = True)

# search_by_domain_operation(ontoexpline, op_model, parameters={'attribute': evolutiveModel_att, 'port_value': 'JTT'})
#quais entradas geram um atributo não relacionado a ela: Quais arquivos validados geram o modelo evolutivo RtREV?
# indirect_search(ontoexpline, op_validation, attributes={"model": "RtREV"})




