programId=0
def incrementProgramId():
    global programId
    programId +=1
    print("===> id: ", programId)
    return programId

def createProgram(onto, name, operation, source, dataflow):
    program = onto.Program(name)
    program.is_a.append(operation)

    metadata_url = onto.Url(source)
    program.hasMetadata.append(metadata_url)
    programId = incrementProgramId()
    program.hasId = programId
    program.belongsTo = dataflow

    return program

def associateProgramPort(program, inPorts, outPorts):
    """[função utilizada para associar programas em portas]
        Arguments:
            ontoexpline {[ontology]} -- [ontologia utilizada pelo código, no caso: ontoexpline com provone, expline, metadata e edam]
            inports {[port list ]} -- [lista de portas de entrada]
            outports {[port list]} -- [lista de portas de saída]
        """
    if inPorts and outPorts:
        program.hasInPort = inPorts
        program.hasOutPort = outPorts
    else:
        print("|*** Relações não podem ser vazias!")
        return exit()

