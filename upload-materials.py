from docx import Document
from io import StringIO 
from pathlib import Path
from tqdm import tqdm
import argparse
import logging
import os
import sys
import traceback
import aws_utils


def main(input):
    files = []

    file_count = 0
    # we can either process a dir full of files or a single file
    if os.path.isdir(input):
        local_files = os.listdir(input)
        for file in local_files:
            files.append(os.path.join(input, file))
    elif os.path.isfile(input):
        files.append(input)

   
    for file in tqdm(files):
        if file.endswith('.pdf'):
            if file.endswith('backgroundmaterials.pdf'):
                public_url = aws_utils.upload_pdf(file, aws_utils.FileTypes.BRIEFING_BOOK)
                logging.info('uploaded briefing book ' + file)
                logging.info('public url: ' + public_url)
            elif file.endswith('interview.pdf'):
                public_url = aws_utils.upload_pdf(file, aws_utils.FileTypes.TRANSCRIPT)
                logging.info('uploaded interview ' + file)
                logging.info('public url: ' + public_url)
            else:
                logging.info('skipping ' + file)

        
    
    



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('POH')
    logger.info("Started")
    
    parser = argparse.ArgumentParser(description='Process arguments.', add_help=False)
    parser.add_argument("input",  nargs='?', help="location of file(s) to process.  can be a directory or a single .docx file")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help="call this function with no argument to process docx files in $HOME/poh")
    args = parser.parse_args()

    if args.input:
        input = args.input
    else:
        input = str(Path.home()) + '/poh'
    
    
    main(input)
    
    
    logger.info("Finished")