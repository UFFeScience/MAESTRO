# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for functions, files, tool windows, actions, and settings.
import os
import statistics

import owlready2
import xds as xds
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
from maestro_analysis import find_data_tranformation_telemetry_metrics, find_program_telemetry_metrics, search_data, \
    search_by_domain_operation
from sources.TemplateExecution import createTemplate
from dfa_lib_python.dataflow import Dataflow

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



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    df = Dataflow('asd')
    ontoexpline = get_ontology("ontologies/ontoexpline.owl").load()
    # cleanOntology(ontoexpline)

    dataflow = createExperiment(ontoexpline, "Experiment_1")

    # Definindo as operações de domínio EDAM
    op_validation = domainOperation(ontoexpline, "Sequencing_quality_control")
    op_alignment = domainOperation(ontoexpline, "Sequence_alignment_operation_0292")
    op_conversion = domainOperation(ontoexpline, "Sequence_alignment_conversion_operation_0260")
    op_model = domainOperation(ontoexpline, "Sequence_alignment_refinament_operation_2089")
    op_tree = domainOperation(ontoexpline, "Phylogenetic_tree_generation_operation_0547")

    # Atributo e porta de entrada
    sequences_input = createAttribute(ontoexpline, "Input_Validation_att")  # atributo sequencia de entrada
    sequences_port = createPort(ontoexpline, "INPUT_SEQUENCE")  # arquivo consumido pelo programa

    # atributo e porta de saída
    sequences_validated = createAttribute(ontoexpline, "Output_Validation_att")
    sequences_validated_port = createPort(ontoexpline, "VALIDATED_SEQUENCE")  # saída do programa

    # relações de I/O
    rel_input_validation = createRelation(ontoexpline, "Rel_Validation_In")  # relação de entrada
    rel_output_validation = createRelation(ontoexpline, "Rel_Validation_Out")

    # associações de itens abstratos e concretos
    # associatePortAtt(sequences_port, sequences_input)  # associando att na porta
    associatePortAtt(sequences_validated_port, sequences_validated)  # associando att na porta

    associateRelationAtt(rel_input_validation, [sequences_input])
    associateRelationAtt(rel_output_validation, [sequences_validated])

    # criando programa
    remove_pipe = createProgram(ontoexpline, "remove_pipe", op_validation, "sources/SciPhy/cgi-bin/arpa.py", dataflow)
    associateProgramPort(remove_pipe, [sequences_port], [sequences_validated_port])
    in_file = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-f")
    data_type = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-t")
    output_dir = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-o")
    a = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-a")

    output_dir.value=["out"]
    addMetadata(ontoexpline, remove_pipe, in_file)
    addMetadata(ontoexpline, remove_pipe, data_type)
    addMetadata(ontoexpline, remove_pipe, output_dir)
    addMetadata(ontoexpline, remove_pipe, a)
    remove_pipe.hasRetrospectiveCall.append(False)

    # criando atividade
    aa = createActivity(ontoexpline, "validation", op_validation, [rel_input_validation],
                        [rel_output_validation], False, [remove_pipe], True, dataflow)
    ###################################################################################################################

    # Atributo e porta de saida do alinhamento
    alignment = createAttribute(ontoexpline, "alignment_att")  # atributo sequencia de entrada
    sequences_aligned_port = createPort(ontoexpline, "SEQUENCES_ALIGNMENT")  # arquivo consumido pelo programa

    # relações de I/O
    rel_output_alignment = createRelation(ontoexpline, "Rel_Alignment_Out")

    # associações de itens abstratos e concretos
    associatePortAtt(sequences_aligned_port, alignment)  # associando att na porta

    associateRelationAtt(rel_output_alignment, [alignment])

    # criando programa
    mafft = createProgram(ontoexpline, "mafft", op_alignment, "sources/SciPhy/cgi-bin/arpa.py", dataflow)
    associateProgramPort(mafft, [sequences_validated_port], [sequences_aligned_port])
    mafft.hasRetrospectiveCall = [False]
    addMetadata(ontoexpline, mafft, data_type)
    addMetadata(ontoexpline, mafft, output_dir)
    addMetadata(ontoexpline, mafft, a)

    clustalw = createProgram(ontoexpline, "clustalw", op_alignment, "sources/SciPhy/cgi-bin/arpa.py", dataflow)
    associateProgramPort(clustalw, [sequences_validated_port], [sequences_aligned_port])
    clustalw.hasRetrospectiveCall = [False]
    addMetadata(ontoexpline, clustalw, data_type)
    addMetadata(ontoexpline, clustalw, output_dir)
    addMetadata(ontoexpline, clustalw, a)



    associateProgramPort(remove_pipe, [sequences_port], [sequences_validated_port])

    # criando atividade
    aa2 = createActivity(ontoexpline, "alinhamento", op_alignment, [rel_output_validation],
                         [rel_output_alignment], False, [mafft, clustalw], False, dataflow)

    ###################################################################################################################
    # Atributo e porta de saida do alinhamento
    evolutiveModel_att = createAttribute(ontoexpline, "evolutiveModel_att")  # atributo sequencia de entrada
    data_transformation_execution_att = createAttribute(ontoexpline, "data_transformation_execution_id_2023_att")  # atributo sequencia de entrada
    evolutiveModel_port = createPort(ontoexpline, "model")  # arquivo consumido pelo programa
    data_transformation_execution_port = createPort(ontoexpline, "data_transformation_execution_id_2023_port")
    # relações de I/O
    rel_output_evolutiveModel = createRelation(ontoexpline, "ds_omodelgeneratormodule_raxml")

    # associações de itens abstratos e concretos
    associatePortAtt(evolutiveModel_att, evolutiveModel_port)  # associando att na porta
    associatePortAtt(data_transformation_execution_att, data_transformation_execution_port)  # associando att na porta


    associateRelationAtt(rel_output_evolutiveModel, [evolutiveModel_att, data_transformation_execution_att])

    # criando programa
    model_generator = createProgram(ontoexpline, "model_generator", op_model, "sources/SciPhy/cgi-bin/arpa.py", dataflow)
    associateProgramPort(model_generator, [sequences_aligned_port], [evolutiveModel_port, data_transformation_execution_port])
    gamma_categories = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-gamma")
    gamma_categories.value = ["GAMMA_CATEGORIES"]
    prog = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-p")

    addMetadata(ontoexpline, model_generator, gamma_categories)
    addMetadata(ontoexpline, model_generator, data_type)
    addMetadata(ontoexpline, model_generator, output_dir)
    addMetadata(ontoexpline, model_generator, prog)
    model_generator.hasRetrospectiveCall = [False]

    # criando atividade
    aa3 = createActivity(ontoexpline, "evolutive_model", op_model, [rel_output_alignment],
                         [rel_output_evolutiveModel], False, [model_generator], False, dataflow)
    ###################################################################################################################

    # Atributo e porta de saida do alinhamento
    converted_alignment_att = createAttribute(ontoexpline, "converted_alignment_att")  # atributo sequencia de entrada
    converted_alignment_port = createPort(ontoexpline, "CONVERTED_ALIGNMENT")  # arquivo consumido pelo programa

    # atributo para a relação de equivalencia
    converted_alignment_att_eq = createAttribute(ontoexpline, "converted_alignment_att_eq")  # atributo sequencia de entrada

    # relações de I/O
    rel_output_converted_alignment = createRelation(ontoexpline, "Rel_Converted_Alignment_Out")
    rel_output_converted_alignment_eq = createRelation(ontoexpline, "Rel_Converted_Alignment_Out_eq")

    # associações de itens abstratos e concretos
    associatePortAtt(converted_alignment_att, converted_alignment_port)  # associando att na porta

    associateRelationAtt(rel_output_converted_alignment, [converted_alignment_att, converted_alignment_att_eq])

    # criando programa
    read_seq = createProgram(ontoexpline, "readseq", op_conversion, "sources/SciPhy/cgi-bin/arpa.py", dataflow)
    read_seq.hasRetrospectiveCall = [False]
    addMetadata(ontoexpline, read_seq, data_type)
    addMetadata(ontoexpline, read_seq, output_dir)
    addMetadata(ontoexpline, read_seq, prog)

    associateProgramPort(read_seq, [sequences_validated_port], [converted_alignment_port])

    # criando atividade
    aa4 = createActivity(ontoexpline, "conversion", op_conversion, [rel_output_alignment],
                         [rel_output_converted_alignment], True, [read_seq], False, dataflow)

    #criando equivalencia para teste
    aa_equivalence = createActivity(ontoexpline, "eq_conversion", op_conversion, [rel_output_alignment],
                         [rel_output_converted_alignment_eq], True, [read_seq], False, dataflow)
    ###################################################################################################################

    # Atributo e porta de saida do alinhamento
    tree_att = createAttribute(ontoexpline, "phylogenomic_tree")  # atributo sequencia de entrada
    tree_port = createPort(ontoexpline, "fileTree")  # arquivo consumido pelo programa

    # relações de I/O
    rel_output_tree_generator = createRelation(ontoexpline, "Rel_Tree_Generator_Out")

    # associações de itens abstratos e concretos
    associatePortAtt(tree_att, tree_port)  # associando att na porta

    associateRelationAtt(rel_output_tree_generator, [tree_att])

    # criando programa
    raxml = createProgram(ontoexpline, "raxml", op_tree, "sources/SciPhy/cgi-bin/arpa.py", dataflow)
    raxml.hasRetrospectiveCall = [False]
    addMetadata(ontoexpline, raxml, prog)
    addMetadata(ontoexpline, raxml, data_type)
    addMetadata(ontoexpline, raxml, output_dir)

    mrbayes = createProgram(ontoexpline, "mrbayes", op_tree, "sources/SciPhy/cgi-bin/arpa.py", dataflow)
    mrbayes.hasRetrospectiveCall = [False]
    nruns = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-nr")
    nruns.value=["nruns"]
    nchains = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-nc")
    nchains.value=["nchains"]
    burnin = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-brn")
    burnin.value=["burnin"]
    printfreq = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-prt")
    printfreq.value=["printfreq"]
    ngen = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-ng")
    ngen.value=["ngen"]
    rates_mrbayes = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-rt")
    rates_mrbayes.value=["rates_mrbayes"]

    addMetadata(ontoexpline, mrbayes, prog)
    addMetadata(ontoexpline, mrbayes, data_type)
    addMetadata(ontoexpline, mrbayes, output_dir)
    addMetadata(ontoexpline, mrbayes, nruns)
    addMetadata(ontoexpline, mrbayes, nchains)
    addMetadata(ontoexpline, mrbayes, burnin)
    addMetadata(ontoexpline, mrbayes, printfreq)
    addMetadata(ontoexpline, mrbayes, ngen)
    addMetadata(ontoexpline, mrbayes, rates_mrbayes)

    associateProgramPort(raxml, [sequences_aligned_port, evolutiveModel_port], [tree_port])
    associateProgramPort(mrbayes, [converted_alignment_port, evolutiveModel_port], [tree_port])


    # criando atividade
    aa5 = createActivity(ontoexpline, "treegenerator", op_tree, [rel_output_alignment, rel_output_evolutiveModel],
                         [rel_output_tree_generator], False, [raxml, mrbayes], False, dataflow)
    ###################################################################################################################

ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
showExpLine() #está ok
# abstractDerivationByOptionality(ontoexpline) #está ok, ainda não plota o gráfico

# createTemplate(ontoexpline, remove_pipe) #está ok, insere chamadas retrospectiva nos scripts - inserir essas chamadas na função de derivação
# createTemplate(ontoexpline, mafft)
# createTemplate(ontoexpline, mrbayes)

inicio = time.time()
absWf = [aa, aa2, aa3, aa4, aa5]
x = isValid(ontoexpline, absWf)

abs_wf = absWfDependences(ontoexpline, absWf)
# print("DEPENDENCES: ", abs_wf)
print("|*** Executing: ",os.path.basename(__file__),"\n")
# #Função para retornar elementos que estão na ontologia
# # print("\nWF abstrato [[atividade, [dependências]]]: ",abs_wf)
# print("** ",abs_wf)

createProvenanceCalls(ontoexpline, abs_wf, dataflow, [[aa2, clustalw], [aa5, mrbayes]])
fim = time.time()
print("===> Tempo para derivar e criar chamadas de proveniencia:", fim-inicio)
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
inicio = time.time()
owlready2.JAVA_EXE = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"
ontoexpline = get_ontology("ontologies/ontoexpline.owl").load()
with ontoexpline:
    class Equivalence(ontoexpline.Entity):
        equivalent_to = [ontoexpline.Abstract_activity and (ontoexpline.hasInputRelation.some(ontoexpline.Relation and ontoexpline.composedBy.value(ontoexpline.alignment_att))) and (ontoexpline.hasOutputRelation.some(ontoexpline.Relation and ontoexpline.composedBy.value(converted_alignment_att_eq)))]

    ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
    # close_world(Thing)

    # sync_reasoner(infer_property_values = True)


# eq = ontoexpline.Abstract_activity()
eq = ontoexpline.search(type = ontoexpline.Equivalence)
print(eq)
fim = time.time()
print("===> Tempo para calculo da equivalencia:", fim-inicio)
print(aa4, aa4.is_a)

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

search_by_domain_operation(ontoexpline, op_model, parameters={'attribute': evolutiveModel_att, 'port_value': 'JTT'})
#quais entradas geram um atributo não relacionado a ela: Quais arquivos validados geram o modelo evolutivo RtREV?
# indirect_search(ontoexpline, op_validation, attributes={"model": "RtREV"})




