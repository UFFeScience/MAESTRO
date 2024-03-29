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

os.system("python3 Provenance/prospectiveProvenance.py")
# parser = argparse.ArgumentParser(description='Descrição do script.')
# parser.add_argument('full_dataset_plasmodium', type=str, help='Descrição do argumento 1')
# parser.add_argument('nexus', type=str, help='Descrição do argumento 1')
# parser.add_argument('ClustalW', type=str, help='Descrição do argumento 1')
# args = parser.parse_args()
# full_dataset_plasmodium = args.full_dataset_plasmodium
# nexus = args.nexus
# ClustalW = args.ClustalW
#
#
# task = Task(1, "NMFSt","Act_tree_gen")
# task_input = DataSet("iAct_tree_gen", [Element([full_dataset_plasmodium, nexus, ClustalW])])
# task.add_dataset(task_input)
# task.begin()

os.system("cd NMFSt/code && python3 constructor2.py full_dataset_plasmodium nexus ClustalW ")

# task_output = DataSet("oAct_tree_gen", [Element(['PORT_TREE'])])
# task.add_dataset(task_output)
# task.save()
# task.end()

