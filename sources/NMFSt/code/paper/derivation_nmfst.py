# abstract workflow definition, validation and instantiation
absWf = [act_tree_generation, act_sub_trees_generation]
abs_wf= createExperimentLine(ontoexpline, "NMFSt", absWf)
dervation = isValid(ontoexpline, abs_wf, [], True)
injectProvenanceCalls(ontoexpline, derivation, [])



