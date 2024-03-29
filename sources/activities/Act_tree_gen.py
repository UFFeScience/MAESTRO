import owlready2
from owlready2 import *
import subprocess
import time
import os, sys, re, shutil as sh, optparse, time, datetime, threading
import sys, random, string, psutil, subprocess, json
import getopt
from optparse import OptionParser
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

os.system("python sources/Provenance/prospectiveProvenance.py")

task = Task(1, "NMFSt", "TaskClustalW")
task_input = DataSet("iAct_tree_gen", [Element(['../data/full_dataset_plasmodium', 'nexus'])])
task.add_dataset(task_input)
task.begin()

os.system("python2 ontoexpline.sources/NMFSt/code/Constructor.py --inport= ../data/full_dataset_plasmodium --inport= nexus --program ClustalW ")

task_output = DataSet("oAct_tree_gen", [Element(['PORT_TREE'])])
task.add_dataset(task_output)
task.save()
task.end()

