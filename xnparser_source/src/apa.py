import re

apa_regex_noissue = r"(?P<num>[\[\]0-9]+\.?)?\s?(?P<authors>(( and )?( & )?([\w]+)[,]?((\s*[\-]?[A-Z][. ]){1,2})[, ]?\s?(Jr )?)+)( et al. )?[\(]?(?P<year>(\d{4}))[\)]?[.]?[ ]?(?P<title>[A-Z][\w:.,;–\+\-\/\(\) ]+[.])(?P<publication>[\w. ]+)[.,]*\s(?P<volume>[\w0-9\(\)]+)[,]\s?(?P<index>[\w0-9\–]+)\s*"
apa_regex_withissue = r"(?P<num>[\[\]0-9]+\.?)?\s?(?P<authors>(( and )?( & )?([\w]+)[,]?((\s*[\-]?[A-Z][. ]){1,2})[, ]?\s?(Jr )?)+)( et al. )?[\(]?(?P<year>(\d{4}))[\)]?[.]?[ ]?(?P<title>[A-Z][\w:.,;–\+\-\/\(\) ]+[.])(?P<publication>[\w. ]+)[.,]*\s(?P<volume>[\w0-9]+)[\(](?P<issue>[0-9]+)[\)][,]\s?(?P<index>[0-9\–\-]+)\s*"
apa_regex_justtext = r"(?P<authors>(.+?))[\(](?P<year>(\d{4}))[\)][.]?[ ]?(?P<title>[A-Za-z0-9][\w\:.,?;\%\/\–\-\'\"\+\(\)\[\] ]+[.])\s?(?P<publication>[\w\'\-\;:,. ]+)[,]\s[\(]?[0-9][\)]?\s*"
apa_regex_nontext = r"[., ]+(?P<volume>[\0-9]+)([\(](?P<issue>[0-9]{1,2})[\)])?[,]\s?(?P<page>([0-9]+[A-Z]?[a-z]?)[\–\-]?([0-9]+[A-Z]?[a-z]?))\s*"

def runAPA(ref) -> dict:
    result = {}

    author = ''
    year = ''
    title = ''
    volume = ''
    issue = ''
    pub = ''
    page = ''

    # apa regex contains text matching
    result_justtext = re.search(apa_regex_justtext, ref)
    # apa regex for nontext matching
    result_nontext = re.search(apa_regex_nontext, ref)

    # Match just text part
    if result_justtext:
        author = result_justtext.group('authors')
        year = result_justtext.group('year')
        title = result_justtext.group('title')
        pub = result_justtext.group('publication')
    # Match the nontext part: volume, issue
    if result_nontext:
        volume = result_nontext.group('volume')
        issue = result_nontext.group('issue')
        page = result_nontext.group('page')

        
    # AUTHOR
    a_re = re.search('(?P<authors>(.+?))[\(](?P<year>(\d{4}))[\)][.]?[ ]?(.+?)\s*', ref)
    if a_re:
        author = a_re.group('authors')
    a = []
    if ('et al' in author):
        a = author.split('et al')
        author = a[0]
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


    # TITLE
    if '[' in ref and ']' in ref:     
        temp = re.search('\[(.+?)\]', ref).group(1) 
        if len(temp) > 10 or ' ' in temp:
            title = temp

    result['title'] = title


    # YEAR
    # Based on the current ground truth, year is wrapped with () but mla style does not require ()
    # Currently set the () a prerequisite for year field
    y = re.search('([\(](?P<year>\d{4})[\)])', ref)
    # Check if the raw ref contains multiple years 
    # e.g. (1946) vol. 101,3 (1976): 88-90. doi:10.1055/s-0028-1104041
    multipleY = re.search('([\(](?P<year>\d{4})[\)])(.+?)([\(]?(\d{4})[\)]?)', ref)
    if y and (not multipleY):
        year = y.group('year').strip()
    elif multipleY:
        year = multipleY.group('year').strip()

    result['year'] = year


    # VOLUME AND ISSUE
    # Check if the issue brackect wrapped both numbers and texts:
    # e.g. Leighton, F., Coloma, L., & Koenig, C. (1975). Structure, composition,
    # physical properties, and turnover of proliferated peroxisomes. 
    # A study of the trophic effects of Su-13437 on rat liver. The Journal of cell biology, 
    # 67(2PT.1), 281–309. https://doi.org/10.1083/jcb.67.2.281
    if ')' in volume and '(' not in volume:
        vi_re = re.search('(?P<volume>[0-9]+)?[\(](?P<issue>([0-9]+\s?[A-Za-z\-\.]+\s?[0-9]+){1,6})[\)]', ref)
        if vi_re:
            issue = vi_re.group('issue')
            volume = vi_re.group('volume')
    elif volume == '':
        vi_re = re.search('(?P<volume>[0-9]+)[\(](?P<issue>[\w\-]+)[\)]', ref)
        i_re = re.search('(?P<volume>[0-9]+)?[\(](?P<issue>[\w\-]{1,3})[\)]', ref)
        # If contains both volume and issue
        if vi_re:
            issue = vi_re.group('issue')
            volume = vi_re.group('volume')
        # If contains no volume
        elif i_re:
            issue = i_re.group('issue')
            if volume == issue:
                volume = ''
    # Filter the cases when volume and issue were originally identified as volume
    # by the apa_regex_nontext 
    # e.g. 36(1)
    else:
        vi_re = re.search('(?P<volume>[0-9]+)[\(](?P<issue>[\w\-]+)[\)]', volume)
        i_re = re.search('(?P<volume>[0-9]+)?[\(](?P<issue>[\w\-]{1,3})[\)]', volume)
        # If contains both volume and issue
        if vi_re:
            issue = vi_re.group('issue')
            volume = vi_re.group('volume')
        # If contains no volume
        elif i_re:
            issue = i_re.group('issue')
            volume = ''

    result['volume'] = volume
    result['issue'] = issue
    
    
    # PUBLICATION
    re_pub_one = '[\(](?P<year>(\d{4}))[\)][.]?[ ]?(?P<title>[A-Za-z0-9][\w\:.,?;\%\/\–\-\'\"\+\(\)\[\] ]+[.])\s?(?P<publication>[\w.:\-\;\' ]+)[,]\s([0-9])\s*'
    r_pub_one = re.search(re_pub_one, ref)
    # re_pub_two = '(.\”)\s(?P<publication>[\w.:\-\;\' ]+)\s[(vol.)(,)]\s*'
    # r_pub_two = re.search(re_pub_two, ref)
    if r_pub_one:
        pub = r_pub_one.group('publication').strip()   
    # elif r_pub_two:
    #     pub = r_pub_two.group('publication').strip()

    # Check if the journal name is between '].' and number
    r_foreign_pub = re.search('(].)\s?(?P<publication>[\w\'\-\;:,. ]+)[,]\s[\(]?[0-9][\)]?\s*', ref)
    if r_foreign_pub: 
        pub = r_foreign_pub.group('publication').strip()

    result['journal'] = pub

    
    # PAGES
    # truth: 1281-6	original/parsed: 1281–1286
    if('–' in page):
        r_parsedpage = re.search('(?P<one>[0-9]+)[\-\–](?P<two>[0-9]+)s*', page)
        if r_parsedpage:
            parsed_first_page = r_parsedpage.group('one')
            parsed_second_page = r_parsedpage.group('two')
            page = parsed_first_page + '-' + parsed_second_page

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
