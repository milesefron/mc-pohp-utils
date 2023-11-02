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
            str = str + "BOLD" + run.text + "BOLD"
        else:
            str = str + run.text
    return str

def extract_speaker(para, file):
    name_test = handle_bf(para)
    
    
    # need to hack things in case the terminating colon on the name slug is NOT bolded
    if re.search('^BOLD[A-Za-z \\.]+BOLD: (?!BOLD)', name_test):
        print(file)
        print("FOUND NON-BOLDED COLON IN NAME SLUG.  You should open the docx file and edit the bolding in this line...")
        print(para.text)
        quit()


    if re.search('^BOLD.*:\s?BOLD', name_test):
        fields = re.split(':\s?BOLD', name_test)
        if not fields or len(fields) == 0:
            fields = name_test.split(':BOLD')
        if fields and len(fields) > 0:
            speaker = fields[0]
            speaker = re.sub('BOLD', '', speaker)
            speaker = re.sub('BOLD', '', speaker)
            return speaker    
    return None


def docx2html(doc, file):
    # create an empty HTML element
    html_element = etree.Element('html')

    # create the head element
    head_element = etree.SubElement(html_element, 'head')
    title_element = etree.SubElement(head_element, 'title')
    style_element = etree.SubElement(head_element, 'link')
    style_element.attrib['rel'] = 'stylesheet'
    style_element.attrib['href'] = 'style.css'
    title_element.text = 'Document Title'

    body_element = etree.SubElement(html_element, 'body')
    dl_element = etree.SubElement(body_element, 'dl')

    conversation = []
    context = []
    dd_elelment = None
    dt_element = None
    p_element = None

    # get the beginning of our interview proper
    first = interview_utils.get_start_para(doc)



    for para in doc.paragraphs[first:]:
        
        speaker = extract_speaker(para, file)
        text = handle_italics(para)

        print(speaker)
        print(text)

        # does it have a named speaker?
        if speaker:
            
            # separate the speaker info
            regex = '^' + speaker + ":"
            speech = re.sub(regex, '', text)

            dt_element = etree.SubElement(dl_element, 'dt')
            dt_element.text = speaker

            dd_element = etree.SubElement(dl_element, 'dd')
            p_element  = etree.SubElement(dd_element, 'p')
            p_element.text = speech
            

        # if not, simple--we just append to the context
        else:
            p_element  = etree.SubElement(dd_element, 'p')            
            p_element.text = text
            


    string_version = etree.tostring(html_element).decode("utf-8").replace('::ITALICS', '<i>').replace('ITALICS::', '</i>')
    string_version = re.sub('R?E?DACTEDTEXT', '<span class="redacted2">REDACTEDTEXT</span>', string_version)
    return string_version




        



