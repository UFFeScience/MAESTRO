import configparser, os
from time import *
from pathlib import Path
from extractConfigParam import *
from time import *
import subprocess


path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "conf.ini")

cfg = configparser.ConfigParser()
cfg.read(config_path)

validation_input = cfg.get('VALIDATION', 'in_file')
validation_output = cfg.get('VALIDATION', 'out_file')
alignment_input = cfg.get('ALIGNMENT', 'in_file')
alignment_output = cfg.get('ALIGNMENT', 'out_file')
modelgenerator_input = cfg.get('MODELGENERATOR', 'in_file')
modelgenerator_gamma = cfg.get('MODELGENERATOR', 'gamma')
converter_input = cfg.get('CONVERTER', 'in_file')

tree_generator = cfg.get('TREEGENERATOR', 'in_file')
fileEvolutiveModel = cfg.get('TREEGENERATOR', 'evolutiveModel')
nruns = cfg.get('TREEGENERATOR', 'nruns')
nchains = cfg.get('TREEGENERATOR', 'nchains')
burnin = cfg.get('TREEGENERATOR', 'burnin')
printfreq = cfg.get('TREEGENERATOR', 'printfreq')
ngen = cfg.get('TREEGENERATOR', 'ngen')
rates_mrbayes = cfg.get('TREEGENERATOR', 'rates_mrbayes')

print("++++++++++++++")


# os.system('python3 remove_pipe.py -f ' + validation_input)
# os.system('python3 mafft.py -f '+ alignment_input)
# os.system('python3 model_generator.py -f '+ modelgenerator_input)
# os.system('python3 read_seq.py -f '+ converter_input)
# os.system('python3 mrbayes.py -f ' + tree_generator +' -f '+ fileEvolutiveModel +' -nr '+ nruns +' -nc ' +nchains+' -brn '+burnin+' -prt '+printfreq+' -ng '+ngen+' -rt '+rates_mrbayes)

# os.system("python3 mrbayes.py -f=in_file -f=evolutiveModel -nr=nruns -nc=nchains -brn=burnin -prt=printfreq -ng=ngen -rt=rates_mrbayes")
# os.system("python remove_pipe.py -f=File1023")
# os.system("python mafft.py -f=Validation_output")
# os.system("python muscle.py -in=ORTHOMCL1 -out=ARQUIVO_SAIDA")
# os.system("python model_generator.py -f=file1024")
# os.system("python read_seq.py -f=file1024")
# os.system("python mrbayes.py -f=fileConvertedAlignment -f=fileEvolutiveModel -nr=nruns  -nc=nchains  -brn=burnin  -prt=printfreq  -ng=ngen  -rt=rates_mrbayes")
print(alignment_input, alignment_output)
os.system("python programs/remove_pipe.py -f="+validation_input)
os.system("python programs/mafft.py -INFILE="+str(alignment_input)+" -OUTFILE="+str(alignment_output))
os.system("python programs/model_generator.py -f="+alignment_output+" -gamma="+modelgenerator_gamma)
