import re
from docx import Document

forbidden = ['Assisting' , 
             'assisting' , 
             'Audiotape' , 
             'audiotape', 
             'Transcription',
             'transcription',
             'Transcript',
             'copy',
             'editor'
             'Final_edit',
             'Final',
             'Notetaker',
             'Index'
             ]
k=1
def get_start_para(docx):    
    factors = []
    k=1
    for para in docx.paragraphs:
        
        k+=1
        line = para.text
        match = re.search(': ', line) 
        factor = 0

        if k > 40:
            factor +=1

        if match:
            factor +=1 # i.e. there is a colon

            proper_name = line[0:match.span()[0]].replace('inal edit', 'inal_edit')
            
            for forbidden_term in forbidden:
                if forbidden_term in proper_name:
                    factor -= 10
            
            toks = proper_name.split(' ')
            if len(toks) < 4:
                factor += 1 # i.e. the number of words looks like a name

            if len(toks) > 7:
                factor -= 10

            for tok in toks:
                if tok and tok[0].isupper():
                    factor +=1 # i.e. the tokens are capitalized like names
        #print(str(factor) + " " + line)
        factors.append(factor)
    return next(x for x, val in enumerate(factors) if val > 2) 


