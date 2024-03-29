#activity 01 specification
act_tree_gen = 	createActivity(ontoexpline, "Act_tree_gen", op_tree, [rel_input],[rel_output_tree_gen], False, [clustalw], True, dataflow)

#activity 02 specification
act_sub_trees = createActivity(ontoexpline, "Act_sub_tree", op_refinament, [rel_output_tree_gen], [rel_output_subtrees], False, [subtree_program], False, dataflow)

