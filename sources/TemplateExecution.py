import os
from functions.ProvenanceCalls import *
from pathlib import Path

def createTemplate(ontoexpline, activity, implementer):
    # essa função pega a chamada do programa que está salva como url no programa instanciado na ontologia.
    print("|*** Creating command line to ",  activity, " running: ", implementer, "In: ", os.path.basename(__file__))

    templateExecution = []
    act_file = open("sources/activities/"+activity.name+".py", "w")
    # metadata = list(set(implementer.hasMetadata)) #remove duplicatas
    for program in implementer:
        for metadata in program.hasMetadata:
            if ontoexpline.Url in metadata.is_a:
                print(metadata)
                templateExecution = '\nos.system("cd NMFSt/code && python3 ' + str(metadata.name)

        for port in program.hasInPort:
            templateExecution = templateExecution + " " + str(port.name)

    templateExecution = templateExecution+ " "+program.name



    # print("|*** Creating command line to ", program.name ,". In: ", os.path.basename(__file__))
    # #buscando a atividade que é implementada pelo programa
    # # so pode ter 1 metadado url que é o arquivo py
    # activity = ontoexpline.search(executedBy=program)
    # print("activity in template execution: ",activity)
    #
    # template = ''
    # conf_param = []
    # for meta in implementer.hasMetadata:
        # if ontoexpline.Url in meta.is_a:
        #     # print("script => ",meta.name)
        #     file_source = Path(meta.name)
        #     template = template + str(meta.name)
        #     os.system('chmod +x ' + meta.name)
        #
        #     # f = open(activity[0].hasMetadata[0].name, "w")
        #     # f.write("python2 "+str(file_source))
        #     # f.close()



        # if ontoexpline.Configuration_Parameter in meta.is_a:
        #     print("|*** ConfigurationParameter: ",meta.name," in: ", os.path.basename(__file__))
        #     templateExecution = templateExecution+" "+meta.name+" "
        #
        #     if meta.name == "--act":
        #         print("******************meta", meta, implementer.implements)
        #         templateExecution = templateExecution + str(implementer.implements)

            # if meta.name == "-a":
            #     templateExecution = templateExecution + str(implementer.name)
            #
            # if meta.name == "-p":
            #     templateExecution = templateExecution + str(implementer.name)

            # for val in meta.value:
            #     templateExecution = templateExecution + val+" "
            #     conf_param.append(val)

    # print("metadado da atividade",activity.hasMetadata)
    # f = open(activity.hasMetadata.name, "w")
    # f.write('os.system("python2 '+str(template)+'")\n')
    # f.close()
    #
    templateExecution = templateExecution+ ' ")\n'
    act_file.write(templateExecution)
    act_file.close()

    inputPortList = ""
    programName = ""
    for p in implementer:
        programName=p.name
        print("======> ",p)
        for port in p.hasInPort:
            print("=====> inport", port)
            inputPortList = inputPortList +" " + port.name

    f = open("sources/wf.py", "a+")
    f.write('os.system("python3 activities/'+str(os.path.basename((activity.name)+".py ")+ inputPortList+ " "+programName+' " )\n'))
    f.close()
    # insertRetrospectiveCall(ontoexpline, program, activity.hasMetadata.name)

    # os.system(template)
