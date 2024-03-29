# `MAESTRO`


`MAESTRO` (experi**M**ent m**A**nag**E**ment ba**S**ed on**T**ology and p**RO**venance) is an approach to support scientists in generating bioinformatic experiments workflow-based. The approach aims to create valid experiments adapted to capture data provenance considering optionalities and variabilities in the experiment. Three modules compose Maestro: an ontology named [OntoExpLine](https://sol.sbc.org.br/index.php/bresci/article/view/11179), a provenance tool named DfAnalyzer that capture and storage data provenance at runtime, and an API that enable scientists to specify and derive a workflow specification according to their necessities.


## `MAESTRO` architecture

### Module I: OntoExpLine Ontology

OntoExpLine is an ontology to represent algebraic experiment lines that aim to describe workflows specifications in abstract and concrete levels and add metadata and domain knowledge. According to this, OntoExpLine comprises four branches: Domain, Experiment Line (abstract workflow level), Workflow (concrete workflow level), and metadata, all described below.

#### Domain
The first one is named Domain. The Domain module is represented as an OntoExpLine branch and describes the domain operations used to create an experiment. In this module, we used [EDAM](https://edamontology.org/page#Viewing) ontology as an OntoExpLine sub-ontology. The domain branch provides operations performed in bioinformatic experiments (*e. g.*, sequence alignment, nucleic acid curvature calculation, clustering, DNA mapping, etc.), their relations with the knowledge field (*e. g.*, Biosciences, Chemistry, Physics), the type of data (*e. g.*, biodiversity data, ecological data, etc.), and data formats (*e. g.*, JSON, YALM, RDF, etc.).

Described in the following code is a concept that defines a domain operation named Sequence Alignment represented by  **operation_0292**. The concept description defines its subclasses, restrictions, and relationships with other domain elements.

    <!-- http://edamontology.org/operation_0292 -->
    <owl:Class rdf:about="http://edamontology.org/operation_0292">
        <rdfs:subClassOf rdf:resource="http://edamontology.org/operation_2403"/>
        <rdfs:subClassOf rdf:resource="http://edamontology.org/operation_2451"/>
        <rdfs:subClassOf rdf:resource="http://edamontology.org/operation_2928"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="http://edamontology.org/has_output"/>
                <owl:someValuesFrom rdf:resource="http://edamontology.org/data_0863"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <created_in>beta12orEarlier</created_in>
        <oboInOwl:comment>Includes methods that align sequence profiles (representing sequence alignments): ethods might perform one-to-one, one-to-many or many-to-many comparisons.  See also &apos;Sequence alignment comparison&apos;.</oboInOwl:comment>
        <oboInOwl:hasDefinition>Align (identify equivalent sites within) molecular sequences.</oboInOwl:hasDefinition>
        <oboInOwl:hasExactSynonym>Sequence alignment construction</oboInOwl:hasExactSynonym>
        <oboInOwl:hasExactSynonym>Sequence alignment generation</oboInOwl:hasExactSynonym>
        <oboInOwl:hasNarrowSynonym>Consensus-based sequence alignment</oboInOwl:hasNarrowSynonym>
        <oboInOwl:hasNarrowSynonym>Constrained sequence alignment</oboInOwl:hasNarrowSynonym>
        <oboInOwl:hasNarrowSynonym>Multiple sequence alignment (constrained)</oboInOwl:hasNarrowSynonym>
        <oboInOwl:hasNarrowSynonym>Sequence alignment (constrained)</oboInOwl:hasNarrowSynonym>
        <oboInOwl:inSubset rdf:resource="http://purl.obolibrary.org/obo/edam#edam"/>
        <oboInOwl:inSubset rdf:resource="http://purl.obolibrary.org/obo/edam#operations"/>
        <rdfs:comment>See also &quot;Read mapping&quot;</rdfs:comment>
        <rdfs:label>Sequence alignment</rdfs:label>
        <rdfs:seeAlso rdf:resource="https://en.wikipedia.org/wiki/Sequence_alignment"/>
    </owl:Class>

#### ExpLine
Expline is the second module. In this module, the experiment is specified as a set of activities in the abstract form, considering the domain operations provided by the first module. The scientist defines what the experiment will perform, not how the operations run. The experiment is defined as a set of domain activities that consume and generate datasets used on the flow. Considering the variabilities on the workflow structure, we used the [Experiment Line approach](https://link.springer.com/chapter/10.1007/978-3-642-02279-1_20) to describe three types of activities: mandatory (essential to the experiment), optional (activities which can be removed from the experiment), and variant (can be executed by different programs or scripts). 

#### ProvONE
To compose the third module, we used [ProvONE](http://jenkins-1.dataone.org/jenkins/view/Documentation%20Projects/job/ProvONE-Documentation-trunk/ws/provenance/ProvONE/v1/provone.html) as an OntoExpLine sub-ontology. Unlike the ExpLine module, the ProvONE branch defines concrete components: what programs or scripts implement the domain operations defined as expline activities, and what the implementer consumes/generates.

#### Metadata - DC
The last module is the OntoExpLine Metadata branch composed by [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/).  Metadata represents a category of data used to describe data and in workflow describe the experiment elements such as resources, services, dependencies, consumed/generated data, etc. In `MAESTRO`, we used the Dublin Core data model, composed of fifteen elements and characterized mainly because of the ease of use and adaptability to different description levels.

### Module II - Provenance Tool: DfAnalyzer
[DfAnalyzer](https://dl.acm.org/doi/abs/10.14778/3229863.3236265?casa_token=eqMi7Lvv5TwAAAAA:S2nFreuByjO0a7QNj_7oKrdmLdUj_KUmkSpLaFwxYyO6Qrntno-fpLOScyOURp563zMAAd4IQHRk) is a tool that aims to provide dataflow analysis to scientific applications. The architecture comprises five components: 
 **Provenance Data Extractor** (PDE): Based on HTTP requests, capture provenance and data from scientific codes or workflows based on Scientific Workflows Manage Systems. **Raw Data Extractor**: a binary component that accesses files and extracts data. **Raw Data Indexer**: a component that indexes raw data to reduce the volume of data. **DfViewer**: the component that provides a graphical dataflow visualization from the specification. Query interface: a component that provides SQL-based queries to query stored data.
 
#### Prospective Provenance
#### Retrospective Provenance

### Module III - `MAESTRO` API
`MAESTRO` API comprises two types of functions defined as specification and manipulation functions that aim to specify the experiment on the OntoExpLine structure. The first type (specification) seeks to define the experiment according to the Experiment Line approach (conceptual level), ProvONE (concrete level), Domain Operations executed in experience (EDAM), and add Metadata (DC). The second type (manipulation) enable run queries that make possible:

-   Get experiment line, EDAM, ProvONE, and metadata specification elements.
-   Verify instances types and compatibilities according to OntoExpLine classes and properties (e. g.: What program implements an experiment line activity? What data is generated by a program or abstract activity? What domain operations can a program run? etc.).
-   Convert an abstract specification to concrete workflow.
-   Verify variation points on workflow structure.
-   Add or remove optional points on the flow.

  

The functions are described below.
#### To define a domain operation (EDAM branch):
```
domainOperation(onto, "Operation Name")
```
In `MAESTRO` domain operations are concepts integrated from EDAM ontology that represent a Bioinformatic operation. domainOperation() is a **specification function** used to specify a domain operation defined on EDAM that will be attributed to associate abstract and concrete components defined on experiment line and ProveONE branches. This function use two parameters: the ontology load previously and the domain operation label represented on EDAM, and return a ontology object.

An usage example of domainOperation() function:

```
#to load the ontology
ontoexpline = get_ontology("ontologies/ontoexpline.owl").load()

#to define a domain operation present on EDAM ontology
op_validation = domainOperation(ontoexpline, "Sequencing_quality_control")
``` 

#### To define an attribute (Experiment Line branch):
```
createAttribute(ontoexpline, "Attribute name") 
```

An attribute is a Line of Experience concept representing an abstraction of concrete values that may (or may not) have the same structure. To explain the concept, let's consider two programs that aim to generate phylogenomic trees, program A and program B. Although the two programs generate the same result (phylogenomic tree), the output dataset generated by each one can be different. It means that given the same input performed by both programs, both outputs can be composed of distinct types of data, more or less information, or even different formats.

This way, an attribute represents an abstraction of values that can be structurally different (e. g., by information or data types) but represent equivalent results. createrAttribute() is a **specification function** and use two parameters: the ontology load previously and the attribute label, and return a ontology object.

An usage example of createAttribute() function:
```
#Creating an attribute on Experiment Line branch
sequence_input_att = createAttribute(ontoexpline, "Input_Validation") 
```

#### To define a relation (Experiment Line branch):
```
createRelation(ontoexpline, "Relation name")
```

As the attribute, a relation is an experiment line concept representing a collection of attributes. The relation concept is a dataset abstract version. createRelation() is a **specification function** and use two parameters: the ontology load previously and the relation label, and return a ontology object.

```
# Creating an input relation
input_validation = createRelation(ontoexpline, "Rel_Validation_In")  
```
#### To associate relation to attributes:
```
associateRelationAtt(relationObject, [attributes list])
```
After creating attributes and relation instances is needed to associate each other aiming with defining an abstract dataset. The function associateRelationAtt() is a **specification function** and uses a relation object and an attributes list as parameters.

An usage example of associateRelationAtt():

```
# Associating inputValidation (Relation) to a list of attributes
associateRelationAtt(inputValidation, [sequence_input_att])
```

<img src = "visualizations/png/rel_att.png" width="450">


#### To define concrete data instances (ProvONE branch):
```
createPort(ontoexpline, "Port name")
```
Port instances represent concrete data consumed and produced by programs and their execution parameters. createPort() is a **specification function** and uses the ontology and a string as parameters.

An usage example of createPort():
```
# Creating a port
input_sequence_port = createPort(ontoexpline, "ORTHOMCL1000")
```
#### To associate port to attribute:
```
associatePortAtt(Port, Attribute)
```
Although attribute and port instances represent data elements, it uses different levels. While attribute represents data at the abstract level, port represents the data object consumed/generated by programs/scripts. In Maestro's context, different programs can consume/generate the same attribute in different structures; given this, attributes need to be associated with ports explicitly to enable equivalences between attributes and ports. The function associatePortAtt() is a **specification function** and uses a port and attribute to create the relation.

An usage example of associatePortAtt():
```
associatePortAtt(sequence_input_att, input_sequence_port)
```

<img src = "visualizations/png/att_port.png" width="450">

#### To create a program (ProvONE branch)

```
createProgram(ontoexpline, "Program name", domain_operation, "directory")
```
ProvONE defines a program as a computational task that consumes and produces data. In Maestro's context, the function used to instantiate a program needs as parameters: the ontology, a string representing the program's name, a domain operation, and the program's directory. createProgram() is a **specification function**.

An usage example of createProgram():
```
remove_pipe = createProgram(ontoexpline, "Remove_Pipe", op_validation, "sources/remove_pipe.py")
```
#### To create an abstract activity (Experiment Line branch)
```
createActivity(ontoexpline, "Activity name", domain operation, [input_relation],  
                    [output_relation], Boolean, [programs], Boolean)
```
All the instances defined so far are dependencies to create abstract activities instances. Maestro uses the Experiment Line as the primary approach to derive experiments from a specification based on abstract activities. 

To create am abstract activity on Maestro, the function createActivity() uses the ontology, a string representing the name of the activity, a domain operation, a list of input relations, a list of output relations, a boolean value that represents the optionality on the flow, a list of implementers, and a boolean value to set if the activity is the first on the flow.  createActivity() is a **specification function**.

```
# creating an activity  
aa = createActivity(ontoexpline, "Validation_Activity", op_validation, [rel_input_validation],  
                    [rel_output_validation], False, [remove_pipe], True)
                    
```
