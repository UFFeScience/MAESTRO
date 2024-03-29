from dfa_lib_python.dataflow import Dataflow
from dfa_lib_python.transformation import Transformation
from dfa_lib_python.attribute import Attribute
from dfa_lib_python.attribute_type import AttributeType
from dfa_lib_python.set import Set
from dfa_lib_python.set_type import SetType
from dfa_lib_python.task import Task
from dfa_lib_python.dataset import DataSet
from dfa_lib_python.element import Element
from dfa_lib_python.program import Program

df = Dataflow('NMFSt')

Act_tree_gen = Transformation('Act_tree_gen')
Act_tree_gen_input = Set('iAct_tree_gen', SetType.INPUT,
[ Attribute('att_input_dataset', AttributeType.TEXT), Attribute('att_tree_OUTPUT_FORMAT', AttributeType.TEXT), Attribute('program', AttributeType.TEXT), Attribute('file', AttributeType.TEXT)])

Act_tree_gen_output = Set('oAct_tree_gen', SetType.OUTPUT,
[Attribute('ATT_TREE_OUTPUT', AttributeType.TEXT), Attribute('ATT_ALN', AttributeType.TEXT)])

Act_tree_gen.set_sets([Act_tree_gen_input, Act_tree_gen_output])
df.add_transformation(Act_tree_gen)


Act_sub_tree = Transformation('Act_sub_tree')
Act_sub_tree_input = Set('iAct_sub_tree', SetType.INPUT,
[ Attribute('att_alignment', AttributeType.TEXT)])

Act_sub_tree_output = Set('oAct_sub_tree', SetType.OUTPUT,
[Attribute('att_tree', AttributeType.TEXT)])

Act_sub_tree.set_sets([Act_sub_tree_input, Act_sub_tree_output])
df.add_transformation(Act_sub_tree)

df.save()