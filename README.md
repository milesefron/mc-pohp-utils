# mc-pohp-utils
Utilities for manipulating collections of book-length interview documents.  For now the main bit of functionality is `app-docx2html.py`, which translates a docx-formatted interview into HTML.

# setup
```
git clone https://github.com/milesefron/mc-pohp-utils.git
pip install -r requirements.txt
```

# running
`$ python app-docx2html.py ./directory-full-of-docx-files`

or

`$ python app-docx2html.py path-to-docx-file.docx`

if no path is specified, the program looks for docx files in `$HOME/poh`.

# understanding
This program is intended for use by Miller Center POHP staff.  We often need to translate multiple long-form interview files from docx to html.  This only works because the interviews follow a highly structured format.  This software has been tested on over 100 interviews and works well on them.  But it is somewhat brittle and its output should be checked before publishing results, especially in these cases:
* Redactions. Be sure that all redactions seem to have been rendered properly.
* Name headings.  If interview personnell have unusually formatted names (e.g. with multiple titles or middle names), check closely that they appear correctly.
* Starting line.  Most interviews have frontmatter before the interview itself, which should be skipped by this program.  But that means the software needs to detect where the interview proper begins.  Again, this worked in our training examples, but a spot check is still a good idea.

