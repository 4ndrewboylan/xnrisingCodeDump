from subprocess import PIPE, run
import re
from pathlib import Path

def runCermine(ref) -> dict:
    path = str(Path(__file__).parent.absolute())
    command = ['java', '-cp', path + '/../libs/cermine.jar', 'pl.edu.icm.cermine.bibref.CRFBibReferenceParser', '-reference', ref]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    
    resList = result.stdout.split('\n')
    resList = resList[1:len(resList)-2]
    resList = [line[1:-1].split(' = ') for line in resList]
    resList = [[line[0], line[1][1:-1]] for line in resList]

    resDict = {line[0]:line[1] for line in resList}    
    
    # JOURNAL
    if 'journal' in resDict:
        
        # If lingering quotes from a title
        if '”' in resDict['journal']:
            resList = resDict['journal'].split('”')
            resDict['journal'] = resList[-1]
        # If lingering comma from title
        if ',' in resDict['journal']:
            resList = resDict['journal'].split(',')
            resDict['journal'] = resList[-1]
        # If string ends with "vol"
        if resDict['journal'].endswith("vol"):
            resDict['journal'] = resDict['journal'][:-3]
    else:
        resDict['journal'] = ""
        

    # ISSUE 
    if 'number' in resDict:
        try:
            # If multiple issues returned, use the first
            resDict['number'] = resDict['number'].split(',')[0]
            resDict['issue'] = resDict['number']
            del resDict['number']
            
        except:
            pass
    else:
        resDict['number'] = ""

    # VOLUME
    if 'volume' in resDict:
        try:
            # If multiple volumes returned, use the first
            resDict['volume'] = resDict['volume'].split(',')[0]
        except:
            pass
    else:
        resDict['volume'] = ""

    # PAGE
    if 'pages' in resDict:
        try:
            # If multiple pages, use the first one
            pageList = resDict['pages'].split(',')
            if len(pageList) > 1:
                resDict['pages'] = pageList[0]
            resDict['pages'] = resDict['pages'].replace("--", "-")
        except:
            pass
    else:
        resDict['pages'] = ""

    # TITLE
    if 'title' in resDict:
        try:
            # Find string between brackets. If there is one, that's the title
            s = resDict['title']
            result = re.findall('\[.*?\]', s)
            if result:
                resDict['title'] = result[0]
            # Correct for lingering quotes
            if resDict['title'][0] == '“':
                resDict['title'] = resDict['title'][1:]
            if '”' in resDict['title']:
                resList = resDict['title'].split('”')
                if len(resList) > 1:
                    if resList[0] == "":
                        resDict['title'] = resList[1].lstrip()
                    else:
                        resDict['title'] = resList[0]
            # Correct for lingering bracket
            if "[" in resDict['title']:
                resList = resDict['title'].split('[')
                resDict['title'] = resList[0].strip()
        except:
            pass
    else:
        resDict['title'] = ""

    # AUTHOR(S)
    if 'author' in resDict:
        try:
            # Correct for lingering quotes
            if "“" in resDict['author']:
                resDict['author'] = resDict['author'].replace("“", "")
                resDict['author'] = resDict['author'].strip()
            if "\"" in resDict['author']:
                resDict['author'] = resDict['author'].replace("\"", "")
                resDict['author'] = resDict['author'].strip()
                
        except:
            pass
    else:
        resDict['author'] = ""

    # YEAR
    if 'year' in resDict:
        try:
            # If multiple years, use the latest one
            if ',' in resDict['year']:
                resList = resDict['year'].split(',')
                resList = [int(''.join(filter(str.isdigit, x))) for x in resList]
                resDict['year'] = max(resList)
        except:
            pass
    else:
        resDict['year'] = ""
        
    # CERMINE resDict is a dict with these fields
    # resDict['title']
    # resDict['author']
    # resDict['journal']
    # resDict['volume']
    # resDict['issue']
    # resDict['year']
    # resDict['pages']
    
    return resDict
