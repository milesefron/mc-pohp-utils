# mc-pohp-utils
Utility for manipulating collections of book-length interview documents.  For now the main bit of functionality is `app-docx2html.py`, which translates a docx-formatted interview into HTML.

# setup
```
git clone https://github.com/milesefron/mc-pohp-utils.git
pip install -r requirements.txt
```

# running
This program looks for .docx files (assuming that these will be in the format of Miller Center POHP interviews).  It will translate each .docx file it finds into a corresponding .html file, in the same directory as the .docx file.

There are three ways to run this program.

First, with no arguments like so:
`$ python app-docx2html.py`
In this case, the program will look for .docx files in $HOME/poh.  NB it doesn't do a full directory walk; just a shallow listing of files.

The second method is to supply a different directory:
`$ python app-docx2html.py ./directory-full-of-docx-files`

Lastly, you can point the program at a single .docx file:
`$ python app-docx2html.py path-to-docx-file.docx`

When the program is given a directory, it will ignore any files that don't have a .docx file extension.  If there are Word documents that aren't bona fide POHP interviews, the results will be unpredictable and probably not useful.

There is also a `-v` aka `--verbose` flag.  This only has an effect if there is trouble during the parsing or processing of documents.  In that case, any stacktraces will be shown.

# understanding
This program is intended for use by Miller Center POHP staff.  We often need to translate multiple long-form interview files from docx to html.  This only works because the interviews follow a highly structured format.  This software has been tested on over 100 interviews and works well on them.  But it is somewhat brittle and its output should be checked before publishing results, especially in these cases:
* Redactions. Be sure that all redactions seem to have been rendered properly.
* Name headings.  If interview personnell have unusually formatted names (e.g. with multiple titles or middle names), check closely that they appear correctly.
* Starting line.  Most interviews have frontmatter before the interview itself, which should be skipped by this program.  But that means the software needs to detect where the interview proper begins.  Again, this worked in our training examples, but a spot check is still a good idea.

If you need to alter the way the program handles interviews, you'll want to edit one of two files in this repo:
* `docx2html.py`, which is where the heavy lifting happens
* `interview_utils.py` which contains some basic helper code.

# troubleshooting
One thing to be aware of: this program tries to figure out who is speaking by looking for names with this logic:
* at the beginning of a line
* is it bolded?
* does it follow a name-ish regex?
* does it end with a colon?
That allows us to identify Thomas Jefferson as the speaker when a line starts like so (using HTML as a proxy for Word): 

```
<p><b>Thomas Jefferson:</b> Hi, I am the president.</p>
```

This works in almost all cases.  However, every now and then you'll see something like this instead:

```
<p><b>Thomas Jefferson</b>: Hi, I am the president.</p>
```

i.e. the colon is OUTSIDE of the boldface.  We originally tried to resolve these automatically, but found that there were unpredictable edge cases that made this too risky.  As such, you may see the program bomb out with an error like this:

```
/Users/foo/poh/zzz_donezo/Wexler_Anne.docx
FOUND NON-BOLDED COLON IN NAME SLUG.  You should open the docx file and edit the bolding in this line...
Chanin: Oh yes. A fourth type of meeting included very large sessions in the East Room with the President speaking on a particular issue. At the deputy level this required you to watch the logistics. We had an excellent bunch of people to handle this area on our staff. As you know the mesh of logistics with politics happens very quickly.
```

This means that you should go edit the docx file `/Users/foo/poh/zzz_donezo/Wexler_Anne.docx`, looking for the shown line, and bringing the colon inside the boldface.

These should be rarities, but now you've been warned.