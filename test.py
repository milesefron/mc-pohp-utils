from docx import Document
from lxml import etree
import re
import interview_utils



def handle_italics(para):
    str = ""
    for run in para.runs:
        if run.italic:
            str = str + "::ITALICS" + run.text + "ITALICS::"
        else:
            str = str + run.text
    return str

def handle_bf(para):
    str = ""
    for run in para.runs:
        if run.bold:
            str = str + "::BOLD" + run.text + "BOLD::"
        else:
            str = str + run.text
    return str

def extract_speaker(para):
    name_test = handle_bf(para)
    if re.search('^::BOLD.*:\s?BOLD::', name_test):
        fields = name_test.split(': BOLD::')
        if not fields or len(fields) == 0:
            fields = name_test.split(':BOLD::')
        if fields and len(fields) > 0:
            speaker = fields[0]
            speaker = re.sub('::BOLD', '', speaker)
            speaker = re.sub('BOLD::', '', speaker)
            return speaker
    return None


def docx2html(doc):
    
    # get the beginning of our interview proper
    first = interview_utils.get_start_para(doc)

    print(first)
    quit()

    for para in doc.paragraphs[first:]:
        
        speaker = extract_speaker(para)
        text = handle_italics(para)

        if speaker:
            regex = speaker + ':'
            text = re.sub(regex, '', text).strip()
        
        print(f'{speaker}: {text[0:min(len(text), 50)]}')
            


file = '/Users/mefron/poh/test.docx'
doc = Document(file)
docx2html(doc)




        



