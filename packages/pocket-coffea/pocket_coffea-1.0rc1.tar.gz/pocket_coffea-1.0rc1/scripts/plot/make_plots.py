import os
import sys
#import time
import argparse
import logging

import numpy as np

import matplotlib
matplotlib.use('Agg')

from coffea.util import load

from pocket_coffea.utils.configurator import Configurator
from pocket_coffea.utils import utils
from pocket_coffea.utils.plot_utils import PlotManager
from pocket_coffea.parameters.plotting import style_cfg

parser = argparse.ArgumentParser(description='Plot histograms from coffea file')
parser.add_argument('--cfg', default=os.getcwd() + "/config/test.json", help='Config file with parameters specific to the current run', required=False)
parser.add_argument("-o", "--outputdir", required=True, type=str, help="Output folder")
parser.add_argument("-i", "--inputfile", required=True, type=str, help="Input file")
parser.add_argument('-v', '--version', type=str, default=None, help='Version of output (e.g. `v01`, `v02`, etc.)')
parser.add_argument('-j', '--workers', type=int, default=8, help='Number of parallel workers to use for plotting')
#parser.add_argument('-o', '--only', type=str, default='', help='Filter histograms name with string', required=False)
parser.add_argument('-oc', '--only_cat', type=str, default=[''], nargs="+", help='Filter categories with string', required=False)
parser.add_argument('-os', '--only_syst', type=str, nargs="+", default='', help='Filter systematics with a list of strings', required=False)
parser.add_argument('-e', '--exclude', type=str, default=None, help='Exclude categories with string', required=False)
parser.add_argument('--split_systematics', action='store_true', help='Split systematic uncertainties in the ratio plot')
parser.add_argument('--partial_unc_band', action='store_true', help='Plot only the partial uncertainty band corresponding to the systematics specified as the argument `only_syst`')
parser.add_argument('--overwrite', action='store_true', help='Overwrite plots in output folder')
parser.add_argument('--log', action='store_true', help='Set y-axis scale to log')
parser.add_argument('--density', action='store_true', help='Set density parameter to have a normalized plot')
parser.add_argument('-d', '--data_key', type=str, default='DATA', help='Prefix for data samples', required=False)

args = parser.parse_args()

print("Loading the configuration file...")
if args.cfg[-3:] == ".py":
    # Load the script
    config_module =  utils.path_import(args.cfg)
    try:
        config = config_module.cfg
        logging.info(config)

    except AttributeError:
        print("The provided configuration module does not contain a `cfg` attribute of type Configurator. Please check your configuration!")
    if not isinstance(config, Configurator):
        raise("The configuration module attribute `cfg` is not of type Configurator. Please check yuor configuration!")

    #TODO improve the run options conig
    run_options = config_module.run_options
    
elif args.cfg[-4:] == ".pkl":
    config = cloudpickle.load(open(args.cfg,"rb"))
else:
    raise sys.exit("Please provide a .py/.pkl configuration file")

#print("Starting ", end='')
#print(time.ctime())
#start = time.time()

if os.path.isfile( args.inputfile ): accumulator = load(args.inputfile)
else: sys.exit(f"Input file '{args.inputfile}' does not exist")

if not args.overwrite:
    if os.path.exists(args.outputdir):
        raise Exception(f"The output folder '{args.outputdir}' already exists. Please choose another output folder or run with the option `--overwrite`.")

if not os.path.exists(args.outputdir):
    os.makedirs(args.outputdir)


plotter = PlotManager(
    variables=accumulator['variables'].keys(),
    hist_objs=accumulator['variables'],
    datasets_metadata=accumulator['datasets_metadata'],
    plot_dir=args.outputdir,
    style_cfg=style_cfg,
    only_cat=args.only_cat,
    data_key=args.data_key,
    workers=args.workers,
    log=args.log,
    density=args.density,
    save=True
)
plotter.plot_datamc_all(syst=True, spliteras=False)

"""
# Filter dictionary of histograms with `args.only`
accumulator['variables'] = { k : v for k,v in accumulator['variables'].items() if args.only in k }
if args.exclude:
    accumulator['variables'] = { k : v for k,v in accumulator['variables'].items() if not args.exclude in k }
HistsToPlot = list(accumulator['variables'].keys())

NtotHists = len(HistsToPlot)
NHistsToPlot = len([key for key in HistsToPlot if args.only in key])
print("# tot histograms = ", NtotHists)
print("# histograms to plot = ", NHistsToPlot)
print("Histograms to plot:", HistsToPlot)

# Parallelization of plotting
delimiters = np.linspace(0, NtotHists, args.workers + 1).astype(int)
chunks = [(delimiters[i], delimiters[i+1]) for i in range(len(delimiters[:-1]))]
pool = Pool()
# Parallel calls of make_plots on different subsets of histograms
pool.starmap(make_plots, chunks)
pool.close()

end = time.time()
runTime = round(end-start)
print("Finishing ", end='')
print(time.ctime())
print(f"Drawn {NHistsToPlot} plots in {runTime} s")
"""
