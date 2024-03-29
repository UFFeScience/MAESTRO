import argparse
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

parser = argparse.ArgumentParser(description='Descrição do script.')
parser.add_argument('PORT_TREE', type=str, help='Descrição do argumento 1')
parser.add_argument('SubTree_Program', type=str, help='Descrição do argumento 1')
args = parser.parse_args()
PORT_TREE = args.PORT_TREE
SubTree_Program = args.SubTree_Program


task = Task(2, "NMFSt","Act_sub_tree")
task_input = DataSet("iAct_sub_tree", [Element([PORT_TREE, SubTree_Program])])
task.add_dataset(task_input)
task.begin()

os.system("cd NMFSt/code && python3 sources/NMFSt/code/sub_find.py PORT_TREE SubTree_Program ")

task_output = DataSet("oAct_sub_tree", [Element(['PORT_SUBTREES'])])
task.add_dataset(task_output)
task.save()
task.end()

