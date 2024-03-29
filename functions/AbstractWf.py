import json
import os
from pathlib import Path

def verifyCompatibility(a, activities):
    dependency = []
    for input_relation in a.hasInputRelation:
        for act in activities:
            if input_relation in act.hasOutputRelation:
                for i in input_relation.generatedBy:
                    dependency.append(i)


    return(dependency)

def absWfDependences(ontoexpline, activities):

    abs_wf = []
    valid_wf = True

    for aa in activities:
        act_dependences = []
        dependences = []
        act_dependences.append(aa)

        for relation in aa.hasInputRelation:
            # print(aa.hasInputRelation)

            #se a atividade for a primeira o algoritmo salva a atividade + o tipo First
            if not(relation.generatedBy):
                dependences.append(ontoexpline.First)
                act_dependences.append(dependences)
            else:
                for dep in relation.generatedBy:
                    dependences.append([dep])
                    if dep in activities:
                        dependences.append(True)
                    else:
                        if(ontoexpline.Mandatory in dep.is_a):
                            dependences.append(False)
                            valid_wf = False
                        elif(ontoexpline.Optional in dep.is_a):
                            dependences.append(ontoexpline.Optional)
                    act_dependences.append(dependences)
                    dependences = []

        abs_wf.append(act_dependences)
    # print(abs_wf)
    print("|*** ABS Wf is: ",valid_wf)
    # print("|*** Starting concrete instantiation... In: " , os.path.basename(__file__))
    return(abs_wf)

def isValid(ontoexpline, activities):
    # Todas as relações atividades são verificadas se uma dependência (relation.generatedBy) não estiver no conjunto activities, é retornado False
    verify = ""
    for aa in activities:
        for relation in aa.hasInputRelation:
            for dep in relation.generatedBy:
                if dep in activities:
                    verify = True
                    print("|*** ABS Wf is: ", verify, ". Starting concrete instantiation....")
                    print(aa.name)
                else:
                    verify = False
                    print("|*** ABS Wf is: ", verify,". Exiting MAESTRO...")
                    print(dep, activities)
                    exit(0)
                    # return verify
    return verify

def getAbsWf(ontoexpline, activities):
    # Verifica todas as atividades passadas em forma de lista, retorna a atividade, suas dependencias e um booleano que diz se ela está ou não no conjunto
    abs_wf = []

    for aa in activities:
        act_dependences = []
        dependences = []
        act_dependences.append(aa)

        for relation in aa.hasInputRelation:
            # se a atividade for a primeira o algoritmo salva a atividade + o tipo First
            if not (relation.generatedBy):
                dependences.append(ontoexpline.First)
                act_dependences.append(dependences)
            else:
                for dep in relation.generatedBy:
                    dependences.append([dep])
                    if dep in activities:
                        dependences.append(True)
                    else:
                        if (ontoexpline.Mandatory in dep.is_a):
                            dependences.append(False)
                        elif (ontoexpline.Optional in dep.is_a):
                            dependences.append(ontoexpline.Optional)
                    act_dependences.append(dependences)
                    dependences = []

        abs_wf.append(act_dependences)
    return(abs_wf)

def getVariabilities(ontoexpline, absWf):
    variabilities = []
    aa_program = []

    for aa in absWf:
        if ontoexpline.Variant in aa.is_a:
            aa_program.append(aa)
            aa_program.append(aa.executedBy)
            variabilities.append(aa_program)
            aa_program = []

    return variabilities

def getOptionalities(ontoexpline, absWf):
    optionalities = []
    aa_program = []

    for aa in absWf:
        if ontoexpline.Optional in aa.is_a:
            aa_program.append(aa)
            aa_program.append(aa.executedBy)
            optionalities.append(aa_program)
            aa_program = []

    return optionalities

def getActivityCompatibilities(ontoexpline, activity):
    out_compatibility = []

    aa = {}
    aa["activity"] = activity
    for in_relation in activity.hasInputRelation:
        aa["consumesFrom"] = in_relation.generatedBy
    for out_relation in activity.hasOutputRelation:
        for act in ontoexpline.search(type = ontoexpline.Abstract_activity):
            if out_relation in act.hasInputRelation:
                out_compatibility.append(act)

        aa["generatesTo"] = out_compatibility

    return(aa)

def getRelations(ontoexpline, activity):
    aa_inputRel_outputRel = {}
    aa_inputRel_outputRel["activity"] = activity
    aa_inputRel_outputRel["inputRelation"] = activity.hasInputRelation
    aa_inputRel_outputRel["outputRelation"] = activity.hasOutputRelation

    return aa_inputRel_outputRel

def getInputRelations(ontoexpline, activity):
    return activity.hasInputRelation

def getOutputRelations(ontoexpline, activity):
    return activity.hasOutputRelation

def getAttributesConsumedByActivity(ontoexpline, activity):
    attributes = []
    for inputRelation in activity.hasInputRelation:
        attributes.append(inputRelation.composedBy)
    return attributes

def getAttributesGeneratedByActivity(ontoexpline, activity):
    attributes = []
    for outputRelation in activity.hasOutputRelation:
        attributes.append(outputRelation.composedBy)
    return attributes

def getAttributesFromRelation(ontoexpline, relation):
    attributes = []
    for att in relation.composedBy:
        attributes.append(att)
    return attributes

def getPortConsumedByProgram(ontoexpline, program):
    ports = []
    for port in program.hasInPort:
        ports.append(port)
    return ports

def getPortGeneratedByProgram(ontoexpline, program):
    ports = []
    for port in program.hasOutPort:
        ports.append(port)
    return ports

def getAttributeConsumedByProgram(ontoexpline, program):
    attributes_list = []
    for port in program.hasInPort:
        attributes_list.append(port.wasAssociatedWith)
    return(attributes_list)

def getAttributeGeneratedByProgram(ontoexpline, program):
    attributes_list = []
    for port in program.hasOutPort:
        attributes_list.append(port.wasAssociatedWith)
    return (attributes_list)

def getProgramCompatibilities(ontoexpline, program):
    compatibilities_input = []
    compatibilities_output = []
    compatibilities = {}

    compatibilities["program"] = program
    for port in program.hasInPort:
        for prog in ontoexpline.search(type = ontoexpline.Program):
            if (prog != program) and port in prog.hasOutPort:
                compatibilities_input.append(prog)

    for port in program.hasOutPort:
        for prog in ontoexpline.search(type = ontoexpline.Program):
            if (prog != program) and port in prog.hasInPort:
                compatibilities_output.append(prog)

    compatibilities["input_compatibility"] = compatibilities_input
    compatibilities["output_compatibility"] = compatibilities_output

    return compatibilities



