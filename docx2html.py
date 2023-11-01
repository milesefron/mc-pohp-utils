from docx import Document
from lxml import etree
import re
import interview_utils



def handle_italics(para):
    str = ""
    for run in para.runs:
        if run.italic:
            str = str + "::ITALICS " + run.text + " ITALICS::"
        else:
            str = str + run.text
    
    return str



def handle_redactions(para):
    str = ""
    for run in para.runs:
        if re.search('REDACTEDTEXT', run.text):
            str = str + " " + re.sub('REDACTEDTEXT', '::REDACTED REDACTEDTEXT REDACTED::', run.text)
        else:
            str = str + " " + run.text
    return str



def docx2html(doc):
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
        

        text = para.text

        

        text = handle_italics(para)


        # does it have a named speaker?
        match = re.search('^[A-Za-z]+ ?[A-Za-z]*:', text)
        if match:
            
            # separate the speaker info
            speaker = match.string[match.span()[0]:match.span()[1]-1]
            speech = match.string[match.span()[1]+1:]

            dt_element = etree.SubElement(dl_element, 'dt')
            dt_element.text = speaker

            dd_element = etree.SubElement(dl_element, 'dd')
            p_element  = etree.SubElement(dd_element, 'p')
            
            
            
                
            # handle any redactions
            p_element.text = speech
            

        # if not, simple--we just append to the context
        else:
            p_element  = etree.SubElement(dd_element, 'p')

            # handle any redactions
            
            p_element.text = text
            


    string_version = etree.tostring(html_element).decode("utf-8").replace('::ITALICS', '<i>').replace('ITALICS::', '</i>')
    string_version = re.sub('R?EDACTEDTEXT', '<span class="redacted2">REDACTEDTEXT</span>', string_version)
    return string_version




        



