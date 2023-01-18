# Gold Digger
## Search files for gold

Gold Digger is a simple tool used to help quickly discover sensitive information in files recursively. Originally written to assist in rapidly searching files obtained during a penetration test.

## Installation

Gold Digger requires Python3.

```sh
virtualenv -p python3 .
source bin/activate
python dig.py --help
```

## Usage

```sh
usage: dig.py [-h] [-e EXCLUDE] [-g GOLD] -d DIRECTORY [-r RECURSIVE] [-l LOG]

optional arguments:
  -h, --help            show this help message and exit
  -e EXCLUDE, --exclude EXCLUDE
                        JSON file containing extension exclusions
  -g GOLD, --gold GOLD  JSON file containing the gold to search for
  -d DIRECTORY, --directory DIRECTORY
                        Directory to search for gold
  -r RECURSIVE, --recursive RECURSIVE
                        Search directory recursively?
  -l LOG, --log LOG     Log file to save output
```

## Example Usage
Gold Digger will recursively go through all folders and files in search of content matching items listed in the `gold.json` file. Additionally, you can leverage an exclusion file called `exclusions.json` for skipping files matching specific extensions. Provide the root folder as the `--directory` flag.

An example structure could be:


```sh
~/Engagements/CustomerName/data/randomfiles/
~/Engagements/CustomerName/data/randomfiles2/
~/Engagements/CustomerName/data/code/
```

You would provide the following command to parse all 3 account reports:

```sh
python dig.py --gold gold.json --exclude exclusions.json --directory ~/Engagements/CustomerName/data/ --log Customer_2022-123_gold.log
```

## Results
The tool will create a log file containg the scanning results. Due to the nature of using regular expressions, there may be numerous false positives. Despite this, the tool has been proven to increase productivity when processing thousands of files. 

## Shout-outs
Shout out to @d1vious for releasing git-wild-hunt https://github.com/d1vious/git-wild-hunt! Most of the regex in GoldDigger was used from this amazing project.
