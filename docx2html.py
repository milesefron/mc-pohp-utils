from docx import Document
from io import StringIO 
from lxml import etree
from pathlib import Path
from tqdm import tqdm
import argparse
import logging
import os
import sys
import traceback

import interview_transform


def main(input, verbose):
    files = []

    file_count = 0
    # we can either process a dir full of files or a single file
    if os.path.isdir(input):
        local_files = os.listdir(input)
        for file in local_files:
            files.append(os.path.join(input, file))
    elif os.path.isfile(input):
        files.append(input)

    processed = []
    skipped = []  
    created = [] 
    for file in tqdm(files):
        if '.docx' not in file:
            skipped.append(file)
            continue

        try:
            doc = Document(file)
            html = interview_transform.docx2html(doc, file)

            out_file = file.replace('.docx', '.html')
            parser = etree.XMLParser(remove_blank_text=True)
            tree   = etree.parse(StringIO(html), parser)
            tree.write(out_file, pretty_print=True)
            created.append(out_file)
            processed.append(file)
        except Exception:
            if verbose:
                traceback.print_exc()
            logger.error('could not open/process docx file ' + file)
            skipped.append(file)
    
    for file in processed:
        logger.info('processed: ' + file)
    for file in skipped:
        logger.info('skipped: ' + file)

    return created


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('POH')
    logger.info("Started")
    
    parser = argparse.ArgumentParser(description='Process arguments.', add_help=False)
    parser.add_argument("input",  nargs='?', help="location of file(s) to process.  can be a directory or a single .docx file")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help="call this function with no argument to process docx files in $HOME/poh")
    parser.add_argument('-v', '--verbose', default=False, action="store_true", help="Print out extra information")
    args = parser.parse_args()

    if args.input:
        input = args.input
    else:
        input = str(Path.home()) + '/poh'
    
    verbose = False
    if args.verbose:
        verbose = True
    
    processed = main(input, verbose)
    
    if len(processed) == 0:
        logger.warning("We processed ZERO files.  This program needs .docx files as input to work properly.")
        logger.warning("Try re-running like so: python app-docx2html.py -i /path/to/file.docx")
        logger.warning("...or python app-docx2html.py /path/to/directory/with/docx_files_in_it/")
    else:
        for file in processed:
            logger.info('created: ' + file)
    logger.info("Finished")