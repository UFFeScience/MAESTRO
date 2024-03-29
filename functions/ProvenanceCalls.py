import os

from dfa_lib_python.dataflow import Dataflow
from dfa_lib_python.dataflow import Dataflow
from dfa_lib_python.dependency import Dependency
from dfa_lib_python.transformation import Transformation
from dfa_lib_python.attribute import Attribute
from dfa_lib_python.attribute_type import AttributeType
from dfa_lib_python.set import Set
from dfa_lib_python.set_type import SetType
from dfa_lib_python.task import Task
from dfa_lib_python.dataset import DataSet
from dfa_lib_python.element import Element
from pathlib import Path

# from sources.TemplateExecution import createTemplate


def createProvenanceCalls(ontoexpline, abs_wf, dataflow, options):
    print(dataflow.name)
    createProspectiveCall(ontoexpline,abs_wf, dataflow)


    for aa in abs_wf:
        # aa[0] guarda as atividades, aa[1] guarda as dependências de cada atividade
        for aa in abs_wf:
            # insertProspectiveCall(ontoexpline, aa)
            retrospectiveProvenanceFile = "sources/activities/" + aa[0].name + ".py"
            if (ontoexpline.Variant in aa[0].is_a):
                for op in options:  # se a aa é variante e está dentro de op enviado via usuário, está coerente
                    if (aa[0] in op) and (op[1] in aa[0].executedBy):
                        # print(aa[0]," é variante e pode ser executada por ", op[1].name)

                        createtRetrospectiveCall(ontoexpline, op[1], retrospectiveProvenanceFile, dataflow)
            else:
                # print(aa[0], "é mandatória e é executada por ",aa[0].executedBy)
                for program in aa[0].executedBy:  # esse for é retórico, a API da ontologia sempre devolve uma lista com um elemento pra cada atividade mandatória
                    createtRetrospectiveCall(ontoexpline, program, retrospectiveProvenanceFile, dataflow)

def insertingDfaImports(dfImportsFile, fileToInsertImports):
    os.remove(fileToInsertImports)
    imports_dfanalyzer = open(dfImportsFile, "r")
    imports = ""
    for line in imports_dfanalyzer:
        imports = imports + line
    f = open(fileToInsertImports, "a+")
    # limpando o arquivo que contém o modelo de dados de proveniência (prospectiveProvenance.py)
    if not (os.path.getsize(fileToInsertImports) == 0):
        print("|*** Prospective Provenance file is not empty! Cleaning file..")
        file_to_delete = open(fileToInsertImports, 'w')
        file_to_delete.write("")
        file_to_delete.close()
    # inserindo a tag do dataflow
    f.write(str(imports))

def createProspectiveCall(ontoexpline, abs_wf, dataflow):
    df = "\n\ndf = Dataflow('"+dataflow.name+"')\n"
    # provenance_file_path = "sources/Provenance/prospectiveProvenance.py"
    # imports_DfAnalyzer_path = "sources/Provenance/importsDfanalyzer.txt"
    # os.remove(provenance_file_path)
    # imports_dfanalyzer = open(imports_DfAnalyzer_path, "r")
    # imports = ""
    # for line in imports_dfanalyzer:
    #     imports = imports+line
    # f = open(provenance_file_path, "a+")
    # #limpando o arquivo que contém o modelo de dados de proveniência (prospectiveProvenance.py)
    # if not(os.path.getsize("sources/prospectiveProvenance.py") == 0):
    #     print("|*** Prospective Provenance file is not empty! Cleaning file..")
    #     file_to_delete = open("sources/prospectiveProvenance.py", 'w')
    #     file_to_delete.write("")
    #     file_to_delete.close()
    # #inserindo a tag do dataflow
    # f.write(str(imports))
    f = open("sources/prospectiveProvenance.py", "a+")
    insertingDfaImports("sources/Provenance/importsDfanalyzer.txt", "sources/prospectiveProvenance.py")
    f.write(df)

    for activity in abs_wf:
        print("CREATING PROSPECTIVE CALL TO: ",activity[0].name)
        input_attributes = ""
        output_attributes = ""

        #captura os atributos de entrada da atividade para definir como atributos da dfanalyzer
        for in_rel in activity[0].hasInputRelation:
            for in_att in in_rel.composedBy:
                input_attributes = " "
                if(len(in_rel.composedBy) > 1) and ((in_rel.composedBy.index(in_att) != len(in_rel.composedBy) - 1 )):
                    # se a lista for maior que 1 atributo e o atributo nao for o ultimo, adiciona a virgula na lista de atributos, senão não
                    input_attributes = input_attributes + "Attribute('" + in_att.name + "', AttributeType.TEXT),"
                else:
                    input_attributes = input_attributes + "Attribute('" + in_att.name + "', AttributeType.TEXT)"
        #captura os atributos de saida da atividade para definir como atributos da dfanalyzer
        for out_rel in activity[0].hasOutputRelation:
            for out_att in out_rel.composedBy:
                output_attributes = output_attributes+"Attribute('"+out_att.name+"', AttributeType.TEXT)"

        prospectiveCall = "\n"+str(activity[0].name)+" = Transformation('"+str(activity[0].name)+"')\n" +\
                          str(activity[0].name)+"_input = Set('i"+str(activity[0].name)+"', SetType.INPUT,\n" +\
                          "["+input_attributes+"])\n" + \
                          str(activity[0].name)+"_output = Set('o"+str(activity[0].name)+"', SetType.OUTPUT,\n"+\
                          "["+output_attributes+"])\n" + \
                          str(activity[0].name)+".set_sets(["+str(activity[0].name)+"_input, "+str(activity[0].name)+"_output])\n" +\
                          "df.add_transformation("+str(activity[0].name)+")\n"

        f.write(prospectiveCall)
    f.write("\ndf.save()")
    f.close()

#def insertProspectiveCall é usada na versão que instancia a versão concreta (com arquivos py para cada atividade)
def insertProspectiveCall(ontoexpline, abs_wf):

    df = "df = Dataflow('df_tag')\n\n"
    f = open("sources/prospectiveProvenance.py", "a+")

    #limpando o arquivo que contém o modelo de dados de proveniência (prospectiveProvenance.py)
    if not(os.path.getsize("sources/prospectiveProvenance.py") == 0):
        print("prospectiveProvenance file is not empty! Cleaning file..")
        file_to_delete = open("sources/prospectiveProvenance.py", 'w')
        file_to_delete.write("")
        file_to_delete.close()

    #inserindo a tag do dataflow
    f.write(df)

    for activity in abs_wf:
        print("PROSPECTIVE CALL ABOUT: ",activity)
        input_attributes = ""
        output_attributes = ""

        #captura os atributos de entrada da atividade para definir como atributos da dfanalyzer
        for in_rel in activity.hasInputRelation:
            for in_att in in_rel.composedBy:
                input_attributes = input_attributes+"Attribute("+in_att.name+", AttributeType.TEXT)"

        #captura os atributos de saida da atividade para definir como atributos da dfanalyzer
        for out_rel in activity.hasOutputRelation:
            for out_att in out_rel.composedBy:
                output_attributes = output_attributes+"Attribute("+out_att.name+", AttributeType.TEXT)"

        prospectiveCall = "tf_"+str(activity.name)+" = Transformation("+str(activity.name)+")\n" +\
                          "tf_"+str(activity.name)+"_input = Set('"+str(activity.name)+"', SetType.INPUT,\n" +\
                          "['"+input_attributes+"'])\n" + \
                          "tf_"+str(activity.name)+"_output = Set('"+str(activity.name)+"', SetType.OUTPUT,\n"+\
                          "[Attribute('Alignmt', AttributeType.TEXT),\n" +\
                          "["+output_attributes+"])\n" + \
                          "tf_"+str(activity.name)+".set_sets([tf_"+str(activity.name)+"_input, tf_"+str(activity.name)+"_output])\n" +\
                          "df.add_transformation(tf_"+str(activity.name)+")\n\n"
        f.write(prospectiveCall)
        f.write("\ndf.save()")
    f.close()


def createPortParser(ontoexpline, program):
    content = "\nparser = argparse.ArgumentParser(description='Descrição do script.')\n"
    ports = ""

    for p in program.hasInPort:
        content = content + "parser.add_argument('"+p.name+"', type=str, help='Descrição do argumento 1')\n"

    content = content + "parser.add_argument('"+program.name+"', type=str, help='Descrição do argumento 1')\n"
    content = content + "args = parser.parse_args()\n"
    for p in program.hasInPort:
        content = content + p.name+" = args."+p.name+"\n"
        ports = ports + " "+p.name
    content = content + program.name + " = args." + program.name + "\n"
    # ports = ports +" "+program.name

    print("****** ",ports)
    palavras = ports.split()

    # Juntar as palavras usando vírgula como separador
    texto_com_virgulas = ", ".join(palavras)
    print(texto_com_virgulas)

    return content, texto_com_virgulas



def createtRetrospectiveCall(ontoexpline, program, source, dataflow):
    '''Essa função separa o que é import do que é conteudo executável,
    depois de separar ela insere as chamadas de proveniencia deixando o arquivo com estrutura:
    imports, inicio da chamada de proveniencia, conteudo do script, final da chamada de proveniência.'''
    if (False in program.hasRetrospectiveCall):
        #procura o metadado referente ao arquivo py que vai executar a atividade e insere as chamadas de proveniencia

        # originalProgram = open(source, "r")
        # createTemplate(ontoexpline, ac)
        # retrospectiveProvenanceFile = open('sources/Provenance/retrospectiveProvenance.py', "a")

        print("|*** Inserting DfAnalyzer retrospective calls on: ", source)
        print("|*** Using program: ", program, " to run: ", source,"\n")

        with open(source, 'r') as file:
            originalContent = file.read()

        inports = []
        for i in program.hasInPort:
            inports.append(i.name)

        # t1 = Task(1, dataflow_tag, "ExtrairNumeros")
        # t1_input = DataSet("iExtrairNumeros", [Element(["/home/debora/Documents/numeros", "nexus"])])
        # t1.add_dataset(t1_input)
        #
        # t1.begin()

        prospective_model = "\n"
        dt = ""


        for d in program.implements:
            dt = d.name
            if ontoexpline.First in d.is_a:
                prospective_model = "\n\nos.system(\"python3 Provenance/prospectiveProvenance.py\")"

        portsParses = createPortParser(ontoexpline, program)
        act = ""
        for a in program.implements:
            act = a.name

        provenance_start = "\ntask = Task("+str(program.hasId)+", \""+ dataflow.name +"\",\""+ act +"\")\n" +\
                "task_input = DataSet(\""+"i"+ dt +"\", [Element(["+str(portsParses[1])+ ", "+program.name+"])])\n"+\
                "task.add_dataset(task_input)\n"+\
                "task.begin()"

        insertingDfaImports("sources/Provenance/importsDfanalyzer.txt", source)
        source = open(source, "a+")
        source.write(prospective_model)
        source.write(portsParses[0])
        source.write(str("\n"+provenance_start+"\n"))
        source.write(originalContent)

        outports = []
        for i in program.hasOutPort:
            outports.append(i.name)

        provenance_end =    "task_output = DataSet(\""+"o"+ dt +"\", [Element("+str(outports)+")])\n"+\
                            "task.add_dataset(task_output)\n" + \
                            "task.save()\n" + \
                            "task.end()\n"

        source.write(str("\n"+provenance_end+"\n"))
        source.close()

        program.hasRetrospectiveCall = [True]
        ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")

#def insertRetrospectiveCall é usada na versão que instancia a versão concreta (com arquivos py para cada atividade)
def insertRetrospectiveCall(ontoexpline, program, source):
    '''Essa função separa o que é import do que é conteudo executável,
    depois de separar ela insere as chamadas de proveniencia deixando o arquivo com estrutura:
    imports, inicio da chamada de proveniencia, conteudo do script, final da chamada de proveniência.'''
    if (False in program.hasRetrospectiveCall):
        #procura o metadado referente ao arquivo py que vai executar a atividade e insere as chamadas de proveniencia
        # print("meta name:", source)
        originalProgram = open(source, "w")
        retrospectiveProvenanceFile = open("/sources/Provenance/retrospectiveProvenance.py", "w")

        print("|*** Inserting DfAnalyzer retrospective calls on: ", source)
        print("|*** original program: ", originalProgram, " to run: ", str(source.name),"\n")
        print("|*** Using program: ", program, " to run: ", str(source.name),"\n")

        originalContent = originalProgram.readlines()

        imports = []
        content = []
        for line in originalContent:
            if ((("#") in line) or (("import") in line)) :
                imports.append(line)
            else:
                content.append(line)

        f = open(source, "w")
        for line in imports:
            f.write(str(line))

        inports = []
        for i in program.hasInPort:
            inports.append(i.name)


        provenance_start = "#task = Task(taskId, dataflow_tag, taskName "+program.name+")\n" +\
                "#task_input = DataSet(dataflow_tag, [Element("+str(inports)+")])\n"+\
                "#task.add_dataset(task_input)\n"+\
                "#task.begin()"

        f.write(str("\n"+provenance_start+"\n"))
        source.write("")
        source.write(str("\n"+provenance_start+"\n"))

        for line in content:
            f.write(str(line))
        outports = []
        for i in program.hasOutPort:
            outports.append(i.name)

        provenance_end =    "#task_output = DataSet(dataflow_tag, [Element("+str(outports)+")])\n"+\
                            "#task.add_dataset(task_output)\n" +\
                            "#task.end()\n"

        source.write(str("\n"+provenance_end+"\n"))
        source.write(str("\n"+provenance_end+"\n"))

        f.close()
        source.close()

        program.hasRetrospectiveCall = [True]
        ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")