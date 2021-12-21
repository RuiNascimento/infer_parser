#!/usr/bin/env python3
'''
A simple script to automate the use of infer_experiment.py provided in the REsQC package.

Output of infer_experiment.py can be pipep into infer_parser or used as an argument.

Example usage:
infer_experiment -i aligment.sam -r reference.bed | ./infer_parser.py
or
./infer_parser.py infer_experiment_output.txt

Args:
    filename, output of infer_experiment, can be pipep via stdin alternativelly
    -i, --ignore_failed, ignore the failed to determine fraction
    -m, --max_failed, float fraction of maximum allowed for the failed to determine fraction. Default = 0.1
    -s, --simple, Simple output, for usage in scripts/pipelines.
'''


import sys
import os
import argparse


__author__ = "Rui Nascimento"
__copyright__ = "Copyright 2019, Rui Nascimento"
__credits__ = ["Rui Nascimento"]
__license__ = "MIT License"
__version__ = "1.0.1"
__maintainer__ = "Rui Nascimento"
__email__ = "rui_nascimento93@hotmail.com"
__status__ = "Development"

# Verbose management
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
def enablePrint():
    sys.stdout = sys.__stdout__

# Determine the type of experiment
def type_of_experiment(data):
    if 'SingleEnd' in data:
        print('Single End experiment')
        # return'singleend'
    elif 'PairEnd' in data:
        print('Pair End experiment')
        # return 'pairend'
    else:
        print('Could not determine type of experiment!')

# Parse the fractions
def get_info(data):
    failed = "Couldn't determine the failed fraction"
    first = "Couldn't determine the '++,--' fraction"
    second = "Couldn't determine the '+-,-+' fraction"
    for line in data.splitlines():
        if line.startswith('Fraction of reads failed to determine:'):
            failed = line.split(': ')[1]
        elif line.startswith('Fraction of reads explained by "++,--":'):
            first = line.split(': ')[1]
        elif line.startswith('Fraction of reads explained by "+-,-+":'):
            second = line.split(': ')[1]
        elif line.startswith('Fraction of reads explained by "1++,1--,2+-,2-+":'):
            first = line.split(': ')[1]
        elif line.startswith('Fraction of reads explained by "1+-,1-+,2++,2--":'):
            second = line.split(': ')[1]
    return (failed,first,second)

# Check if failed fraction is to big
def check_failed(info, max_failed=0.1):
    info = float(info[0])
    if info > max_failed:
        print('Failed fraction is more than '+'{:.2%}'.format(max_failed)+' of the data, please double check results')
        exit()
# Check strand to infer HTseq --stranded option to use
def check_strand(info):
    first, second =  float(info[1]), float(info[2])
    difference = abs(first-second)
    if difference > 0.02 and difference < 0.15:
        print('Please double check infer_experiment results!')
    if difference >= 0.15:
        if first > second:
            print("--stranded yes")
            if args.simple:
                enablePrint()
                print('yes')
        else:
            print('--stranded reverse')
            if args.simple:
                enablePrint()
                print('reverse')
    else:
        print("++,-- and +-,-+ factions too similiar, probabily unstranded")
        print("--stranded no")
        if args.simple:
            enablePrint()
            print('no')

# Arguments configuration
parser = argparse.ArgumentParser(prog='infer_parser.py', usage='%(prog)s [options]', description='A simple script to pipe the output of infer_experiment.py in order to determine the correct arguments for HTseq.')
parser.add_argument('-i', '--ignore_failed', action='store_false', help='Ignore fraction of failed to determine.')
parser.add_argument('-m', '--max_failed', action='store', type=float, metavar='', help='Maximum allowed for the failed to determine fraction. Example: -m 0.1')
parser.add_argument('-s', '--simple', action='store_true', help='Simple output, for usage in scripts/pipelines.')
parser.add_argument('filename', nargs='?')
args = parser.parse_args()


if __name__ == "__main__":
    if args.filename:
        data = open(args.filename).read()
    elif not sys.stdin.isatty():
        data = sys.stdin.read()
    else:
        parser.print_help()
        exit()
    if args.simple:
        blockPrint()
    type_of_experiment(data)
    info = get_info(data)
    if args.ignore_failed:
        if args.max_failed:
            check_failed(info,max_failed=args.max_failed)
        else:
            check_failed(info,max_failed=0.1)
    check_strand(info)
