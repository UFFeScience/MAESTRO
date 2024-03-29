import os

from functions.ProvenanceCalls import insertProspectiveCall
from sources.TemplateExecution import createTemplate
import collections

def verifyMatchBetweenAbstractAndConcreteItems(ontoexpline, abs_wf, options):
    # print(abs_wf)
    # print(options)

    consumedPorts = []
    relations = []
    ports_associated_with_attributes = []

    for op in options:
        if(op):
            for op in options:
                # print("i: ", op[0].is_a)
                result = collections.Counter(op[0].is_a) & collections.Counter(op[1].is_a)
                intersected_list = list(result.elements())
                # print("interseção: ",intersected_list)
                if(len(intersected_list) == 0):
                    print("|**** ERROR Variation Point: Incompatible activity and implementer!", op[0]," and ", op[1])
                    exit(0)

                for program in options:
                    for port in program[1].hasInPort:
                        print("ports: ", port)
                        consumedPorts.append(port)
                # print("Portas consumidas pelos programas variantes: ",consumedPorts)

        else:
            print("Dataflow without variation points..")



    for act in abs_wf:
        print("act: ",act)

        print("=>", act.hasOutputRelation)
        for relation in act.hasOutputRelation:
            for at in relation.composedBy:
                for p in at.wasAssociatedWith:
                    ports_associated_with_attributes.append(p)
            relations.append(relation)
    print(relations)

    #faz a varredura nas portas consumidas pelos programas variantes
    for port in consumedPorts:
        #se as portas consumida por esses programas não forem geradas pelas atividades do abs wf
        #maestro não da continuidade na criação concreta e finaliza
        if not(port in ports_associated_with_attributes):
            search = ontoexpline.search(type = ontoexpline.Relation)
            for r in search:
                for a in r.composedBy:
                    if port in a.wasAssociatedWith:
                        # print(r)
                        search2 = ontoexpline.search(type = ontoexpline.Abstract_activity)
                        for aa in search2:
                            if r in aa.hasOutputRelation:
                                print("WF INVÁLIDO, FALTA A PORTA: ", port, " ASSOCIADA A ", port.wasAssociatedWith,
                                      "\nGerada pela Atividade: ", aa, " QUE NÃO ESTÁ NO WF")
                                exit(0)
        else:
            print("\n|----------------------------------------------------|")
            print("Dependência: (porta)", port.name ," verificada...\nIniciando a instanciação concreta...")
            print("|----------------------------------------------------|")



def absWfToConcreteWf(ontoexpline, abs_wf, options):
    # verifyMatchBetweenAbstractAndConcreteItems(ontoexpline, abs_wf, options)
    print("\n|*** Creating concrete workflow using: ", options," as options...")
    print("|*** Executing: ", os.path.basename(__file__))
    print("\n|*** Inserting DfAnalyzer Prospective Model in prospectiveProvenance.py...: ")
    #insere o modelo prospectivo em prospectiveProvence.py
    insertProspectiveCall(ontoexpline, abs_wf)

    with open("sources/importsWf.txt", 'r') as file:
        originalContent = file.read()
    f = open("sources/wf.py", "w")
    f.write("")
    f.write(originalContent)
    f.close()

    #aa[0] guarda as atividades, aa[1] guarda as dependências de cada atividade
    for aa in abs_wf:
        if((ontoexpline.Variant in aa.is_a)):
            print(aa, "é variante")
            for op in options:
                if((op[1] in aa.executedBy)): #se a atividade e o implementador forem compativeis:
                    print(op[1], "executa ", op[0])
                    createTemplate(ontoexpline, aa, op[1])

        else:
            print(aa,  "é invariante")
            createTemplate(ontoexpline, aa, aa.executedBy)
