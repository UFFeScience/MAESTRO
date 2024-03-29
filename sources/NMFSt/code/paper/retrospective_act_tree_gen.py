#constructor.pu retrospective call
task = Task(1, "NMFSt", "Act_tree_gen")
task_input = DataSet("iAct_tree_gen", [Element(INPUT_PATH, OUTPUT_FORMAT, program, path_in_fasta])])
task.add_dataset(task_input)
task.begin()


Phylo.write(tree, path_out_tree, OUTPUT_FORMAT)


task_output = DataSet("oAct_tree_gen", [Element([path_out_tree, path_out_aln])])
task.add_dataset(task_output)
task.end()


