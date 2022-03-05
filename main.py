# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for functions, files, tool windows, actions, and settings.
import os
from owlready2 import *
import subprocess
import os, sys, re, shutil as sh, optparse, time, datetime, threading
import sys, random, string, psutil, subprocess, json
import getopt
from optparse import OptionParser

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
from sources.TemplateExecution import createTemplate
from dfa_lib_python.dataflow import Dataflow


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
        # print(individual)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    df = Dataflow('asd')
    ontoexpline = get_ontology("ontologies/ontoexpline.owl").load()
    cleanOntology(ontoexpline)

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
    associatePortAtt(sequences_port, sequences_input)  # associando att na porta
    associatePortAtt(sequences_validated_port, sequences_validated)  # associando att na porta

    associateRelationAtt(rel_input_validation, [sequences_input])
    associateRelationAtt(rel_output_validation, [sequences_validated])

    # criando programa
    remove_pipe = createProgram(ontoexpline, "Remove_Pipe", op_validation, "sources/programs/remove_pipe.py")
    associateProgramPort(remove_pipe, [sequences_port], [sequences_validated_port])

    # criando atividade
    aa = createActivity(ontoexpline, "Atividade_Validation", op_validation, [rel_input_validation],
                        [rel_output_validation], False, [remove_pipe], True)
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
    mafft = createProgram(ontoexpline, "Mafft", op_alignment, "sources/programs/mafft.py")
    associateProgramPort(mafft, [sequences_validated_port], [sequences_aligned_port])

    clustalw = createProgram(ontoexpline, "ClustalW", op_alignment, "sources/programs/clustalw.py")
    associateProgramPort(clustalw, [sequences_validated_port], [sequences_aligned_port])
    clustalw_out_format = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-OUTPUT")
    clustalw_out_format.value = ["OUTPUT"]
    addMetadata(ontoexpline, clustalw, clustalw_out_format)


    associateProgramPort(remove_pipe, [sequences_port], [sequences_validated_port])

    # criando atividade
    aa2 = createActivity(ontoexpline, "Atividade_Alignment", op_alignment, [rel_output_validation],
                         [rel_output_alignment], False, [mafft, clustalw], False)

    ###################################################################################################################
    # Atributo e porta de saida do alinhamento
    evolutiveModel_att = createAttribute(ontoexpline, "evolutiveModel_att")  # atributo sequencia de entrada
    evolutiveModel_port = createPort(ontoexpline, "fileEvolutiveModel")  # arquivo consumido pelo programa

    # relações de I/O
    rel_output_evolutiveModel = createRelation(ontoexpline, "Rel_Evolutive_Model_Out")

    # associações de itens abstratos e concretos
    associatePortAtt(evolutiveModel_att, evolutiveModel_port)  # associando att na porta

    associateRelationAtt(rel_output_evolutiveModel, [evolutiveModel_att])

    # criando programa
    model_generator = createProgram(ontoexpline, "Model_Generator", op_model, "sources/programs/model_generator.py")
    associateProgramPort(model_generator, [sequences_aligned_port], [evolutiveModel_port])
    gamma_categories = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "-gamma")
    gamma_categories.value = ["GAMMA_CATEGORIES"]
    addMetadata(ontoexpline, model_generator, gamma_categories)

    # criando atividade
    aa3 = createActivity(ontoexpline, "Atividade_Evolutive_Model", op_model, [rel_output_alignment],
                         [rel_output_evolutiveModel], False, [model_generator], False)
    ###################################################################################################################

    # Atributo e porta de saida do alinhamento
    converted_alignment_att = createAttribute(ontoexpline, "converted_alignment_att")  # atributo sequencia de entrada
    converted_alignment_port = createPort(ontoexpline, "CONVERTED_ALIGNMENT")  # arquivo consumido pelo programa

    # relações de I/O
    rel_output_converted_alignment = createRelation(ontoexpline, "Rel_Converted_Alignment_Out")

    # associações de itens abstratos e concretos
    associatePortAtt(converted_alignment_att, converted_alignment_port)  # associando att na porta

    associateRelationAtt(rel_output_converted_alignment, [converted_alignment_att])

    # criando programa
    read_seq = createProgram(ontoexpline, "Read_Seq", op_conversion, "sources/programs/read_seq.py")

    associateProgramPort(read_seq, [sequences_validated_port], [converted_alignment_port])

    # criando atividade
    aa4 = createActivity(ontoexpline, "Atividade_Sequences_Converter", op_conversion, [rel_output_alignment],
                         [rel_output_converted_alignment], True, [read_seq], False)
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
    raxml = createProgram(ontoexpline, "Raxml", op_tree, "sources/programs/raxml.py")


    mrbayes = createProgram(ontoexpline, "MrBayes", op_tree, "sources/programs/mrbayes.py")
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


    addMetadata(ontoexpline, mrbayes, nruns)
    addMetadata(ontoexpline, mrbayes, nchains)
    addMetadata(ontoexpline, mrbayes, burnin)
    addMetadata(ontoexpline, mrbayes, printfreq)
    addMetadata(ontoexpline, mrbayes, ngen)
    addMetadata(ontoexpline, mrbayes, rates_mrbayes)

    associateProgramPort(raxml, [sequences_aligned_port, evolutiveModel_port], [tree_port])
    associateProgramPort(mrbayes, [converted_alignment_port, evolutiveModel_port], [tree_port])


    # criando atividade
    aa5 = createActivity(ontoexpline, "Atividade_Tree_Generation", op_tree, [rel_output_alignment, rel_output_converted_alignment, rel_output_evolutiveModel],
                         [rel_output_tree_generator], False, [raxml, mrbayes], False)
    ###################################################################################################################

ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
# showExpLine() #está ok
# abstractDerivationByOptionality(ontoexpline) #está ok, ainda não plota o gráfico

# createTemplate(ontoexpline, remove_pipe) #está ok, insere chamadas retrospectiva nos scripts - inserir essas chamadas na função de derivação
# createTemplate(ontoexpline, mafft)
# createTemplate(ontoexpline, mrbayes)

# deriveByOptionality(ontoexpline, [[ontoexpline.Atividade_Alinhamento, mafft],[ontoexpline.Atividade_Tree_Generation, raxml]]) #está ok, ainda não plota o gráfico
absWf = [aa, aa2, aa3, aa4, aa5]
x = isValid(ontoexpline, absWf)
print("++ ",x)

abs_wf = absWfDependences(ontoexpline, absWf)
#Função para retornar elementos que estão na ontologia
# print("\nWF abstrato [[atividade, [dependências]]]: ",abs_wf)
print("** ",abs_wf)
absWfToConcreteWf(ontoexpline, abs_wf, [[aa2, mafft], [aa5, mrbayes]])

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



