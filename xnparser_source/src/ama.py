import re

ama_regex_author = r"(?P<num>[0-9\[\]]+\.?)?\s?(?P<author>(([\w.'-]+[ ]?){1,3}[,][ ])*([\w' -]+)\.(\s*[A-Z]\.)?)(?P<end>.*)"
ama_regex_end = r"(?P<front>.*)(?P<year>\d{4});(?P<volume>[0-9\w.? ]+)?(?P<issue>\([0-9-\w. ]+\))?:?(?P<page>[0-9-–P]*)."

def runAMA(ref) -> dict:
    result = {}

    # Using corresponding style parser
    end_result = re.search(ama_regex_end, ref)
    
    # Check if regex was able to parse the reference
    if end_result:
        parsed_fields = end_result.groupdict()
    else:
        parsed_fields = False
    
    # Matching
    if parsed_fields:
        ref_front = parsed_fields.get('front')
        # parse the front half
        front_half_result = re.search(ama_regex_author, ref_front)
        
        # AUTHOR, TITLE, AND JOURNAL
        author = ""
        title = ""
        journal = ""
        
        if front_half_result:
            author = front_half_result.group('author')
            title_journal = front_half_result.group('end').split('. ')      
            
            if len(title_journal) > 3:
                for i in range(len(title_journal) - 1):
                    if i != len(title_journal) - 2:
                        title = title + ". " + title_journal[i]
                    else:
                        journal = title_journal[i]
            elif len(title_journal) > 2:
                title = title_journal[0]
                journal = title_journal[1]
            else:
                title = title_journal[0]
        

        if title and '[' in title and ']' in title:     
            temp = re.search('\[(.+?)\]', title).group(1)
            if len(temp) > 10 or ' ' in temp:
                title = temp

        result['title'] = title
        result['journal'] = journal

        # Check authors
        # if ('et al' in author):
        #     a = author.split('et al')
        #     author = a[0]
        temp = []
        if ' and ' in author:
            temp = author.split(' and ')
            author = "".join(temp)
        if ' & ' in author:
            temp = author.split(' & ')
            author = "".join(temp)
        if ' Jr' in author:
            temp = author.split(' Jr')
            author = "".join(temp)
        if ' 2nd' in author:
            temp = author.split(' 2nd')
            author = "".join(temp)
        if ' 3rd' in author:
            temp = author.split(' 3rd')
            author = "".join(temp)
        if ' Sr' in author:
            temp = author.split(' Sr')
            author = "".join(temp)

        result['author'] = author


        # YEAR, VOLUME, AND ISSUE
        result['year'] = parsed_fields.get('year')
        result['volume'] = parsed_fields.get('volume')
        result['issue'] = parsed_fields.get('issue')


        # TODO: check this
        # PAGES
        page = parsed_fields.get('page')
        result['pages'] = page


    # APA result is a dict with these fields
    # result['title']
    # result['author']
    # result['journal']
    # result['volume']
    # result['issue']
    # result['year']
    # result['pages']

    return result