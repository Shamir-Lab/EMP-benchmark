import json
import os

# import matplotlib as mpl
# font = {'size'   : 22}
# mpl.rc('font', **font)
# mpl.rc('xtick', labelsize=30)    # fontsize of the tick labels
# mpl.rc('ytick', labelsize=30)
# mpl.rc('axes', labelsize=22)
# mpl.rc('legend', fontsize=20)

ALGOS_ACRONYM={"jactivemodules_greedy":"jAM_greedy",
               "jactivemodules_sa": "jAM_SA",
               "DOMINO": "DOMINO",
               "DOMINO2": "DOMINO",
               "netbox": "NetBox",
               "keypathwayminer_INES_GREEDY": "KPM",
               "hotnet2": "HotNet2",
               "bionet": "Bionet",
               "netbox3": "NetBox",
               "DOMINO3": "DOMINO",
               "netbox2_string" : "NetBox",
               "DOMINO4": "DOMINO" 
               }

ALGOS_NAMES=list(set(ALGOS_ACRONYM.values()))
ALGOS=ALGOS_ACRONYM.keys() # sorted(ALGOS_ACRONYM.keys())
# COLORDICT = {a: sns.color_palette("bright", n_colors=len(ALGOS_NAMES))[ALGOS_NAMES.index(ALGOS_ACRONYM[a])] for a in ALGOS_ACRONYM}
# PATCHES = [Line2D([0], [0], marker='o', color='gray', label=ALGOS_ACRONYM[a], markersize=12, markerfacecolor=c, alpha=0.7) for a, c in COLORDICT.iteritems()]

DATASETS_ACRONYM={"Breast_Cancer.G50":"BC",
                  "Crohns_Disease.G50":"CD",
                  "Schizophrenia.G50":"SCZ",
                  "Triglycerides.G50":"TRI",
                  "Type_2_Diabetes.G50":"T2D",
                  "Coronary_Artery_Disease.G50":"CAD",
                  "Bone_Mineral_Density.G50":"BMD",
                  "Height1.G50":"Height",
                  "Alzheimer.G50":"ALZ",
                  "Age_Related_Macular_Degeneration.G50":"AMD",
                  "Atrial_Fibrillation.G50":"AF",

                  "TNFa_2":"TNFa",
                  "HC12":"HC",
                  "ROR_1":"ROR",
                  "SHERA":"SHERA",
                  "SHEZH_1":"SHEZH",
                  "ERS_1":"ERS",
                  "IEM":"IEM",
                  "APO":"APO",
                  "CBX":"CBX",
                  "IFT":"IFT",}


dir_path = os.path.dirname(os.path.realpath(__file__))
PATH_TO_CONF = "config/conf.json"
config_json = json.load(open(os.path.join(dir_path, PATH_TO_CONF)))

BASE_PROFILE= config_json['BASE_PROFILE']
DATASETS_DIR= os.path.join(BASE_PROFILE, "datasets")
NETWORKS_DIR = os.path.join(BASE_PROFILE, "networks")
TEMPLATES_DIR = os.path.join(BASE_PROFILE, "templates")
DICTIONARIES_DIR = os.path.join(BASE_PROFILE, "dictionaries")
OUTPUT_GLOBAL_DIR = os.path.join(BASE_PROFILE, "report")
GO_DIR = os.path.join(BASE_PROFILE, "go")
CACHE_GLOBAL_DIR = os.path.join(BASE_PROFILE, "cache_global")
TRUE_SOLUTIONS_DIR = os.path.join(BASE_PROFILE, "true_solutions")
ROBUSTNESS_SOLUTIONS_DIR= os.path.join(BASE_PROFILE, "robustness_solutions")
LIST_DIR = os.path.join(BASE_PROFILE, "list")
REPOS_DIR = os.path.join(BASE_PROFILE, "repos")
RAW_DIR = os.path.join(BASE_PROFILE, "raw")


ENSEMBL_TO_GENE_SYMBOLS = "ensembl2gene_symbol.txt"
ENSEMBL_TO_ENTREZ = "ensembl2entrez.txt"

GO_OBO_URL = 'http://purl.obolibrary.org/obo/go/go-basic.obo'
GO_ASSOCIATION_GENE2GEO_URL = 'https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz'
GO_FILE_NAME = 'go_bp.obo' #'go-basic.obo'
GO_ASSOCIATION_FILE_NAME = "gene2go"
