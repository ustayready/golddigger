import pathlib
import json
import re
import os
import argparse
import logging
import sys
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-e','--exclude', help='JSON file containing extension exclusions', default='binary.json')
parser.add_argument('-g','--gold', help='JSON file containing the gold to search for', default='gold.json')
parser.add_argument('-d','--directory', help='Directory to search for gold', required=True)
parser.add_argument('-r','--recursive', help='Search directory recursively?', default=True)
parser.add_argument('-l','--log', help='Log file to save output', default=None)
args = parser.parse_args()

version = '0.1'
now = datetime.now()
now_dt = now.strftime('%m%d%Y%H%M%S')
log_file = f'gold_{now_dt}.log'

if not args.log is None:
    log_file = args.log

logging.basicConfig(
        format = '%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level = logging.INFO,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
)

log = logging.getLogger()
log.setLevel(logging.INFO)
log.info(f'Gold Digger v{version}')
log.info(f'Saving results to: {log_file}')

def main(args):
    log.info(f'Searching: {args.directory}')

    gold = load_gold(args.gold)
    log.info(f'Searching for {len(gold)} nuggets...')

    exclusions = load_exclusions(args.exclude)
    log.info(f'Loaded {len(exclusions)} exclusions...')

    mine = load_files(args.directory, args.recursive, exclusions)
    log.info(f'Found {len(mine)} files...')

    nuggets = mine_gold(mine, gold)
    
def mine_gold(mine, gold):
    for check_file in mine:
        if os.path.isfile(check_file):
            file_data = load_file(check_file)
            for nugget in gold:
                matches = re.findall(gold[nugget], file_data)
                if matches:
                    log.info(f'Struck gold! {nugget} -> {check_file}')

def load_gold(gold):
    with open(gold, 'r') as fh:
        return json.load(fh)

def load_exclusions(exclusions):
    with open(exclusions, 'r') as fh:
        return [x.lower() for x in json.load(fh)]

def load_file(check_file):
    try:
        with open(check_file, 'r') as fh:
            return fh.read()
    except:
        return ''

def load_files(gold_mine, recursive, exclusions):
    good_files = []
    nuggets = [x for x in pathlib.Path(gold_mine).rglob('*')]
    for nugget in nuggets:
        if not any(
            exclude in os.path.basename(nugget) 
            for exclude in exclusions
        ):
            good_files.append(nugget)
    return good_files

if __name__ == '__main__':
    main(args)
