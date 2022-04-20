import re

mla_regex = r"(?P<num>[0-9\[\]]+\.?)?\s?(?P<authors>[\w\,\.\s]+.)[\s]?[\"\“](?P<title>[\w –\'\-\s\:.,\-\(\)]+[.]?)[\"\”]\s?(?P<publication>[\w\-\s\:\,\-\(\)]+)[,]?[\s]?(?P<volume>(vol.)?\s?[\w0-9.,\(\)]+)\s?(?P<year>[\(]\d{4}[\)])[\:\,]?(?P<index>(pp.)?\s[0-9–\-.,]+)"

def runMLA(ref) -> dict:
    result = {}
    
    # TITLE
    title = ""
    if '[' in ref and ']' in ref and ('“' in ref or '"' in ref):
        if ('“' in ref and (ref.index(']') < ref.index('”')
        or ref.index('[') - ref.index('”') > 2)):
            title = re.search('“(.+?)”', ref).group(1) 
        else:
            title = re.search('\[(.+?)\]', ref).group(1)
    elif '“' in ref:
        title = re.search('“(.+?)”', ref).group(1) 

    else:
        title = ""

    result['title'] = title


    # AUTHOR
    a = []
    if ('"' in ref):
        a = ref.split('"')
    if ('et al' in ref):
        a = ref.split('et al')
    else:
        a = ref.split('“')
    author = a[0]
    temp = []
    if ' and ' in author:
        temp = author.split(' and ')
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


    # VOLUME, YEAR, ISSUE
    volume = ""
    issue = ""
    year = ""
    r = re.search('((vol. )(?P<vol>[0-9]+)\s?[,]?)(?P<issue>[\w0-9\-. ]+)[,]?\s?([\(]?(?P<year>\d{4})[\)]?[\:\,]?)', ref)
    if r:
        volume = r.group('vol')
        issue = r.group('issue')
    if 'vol.' not in ref:
        issue = re.search('(\s?(?P<issue>[\w0-9\-. ]+)[,]?\s?([\(]?(?P<year>\d{4})[\)]?[\:\,]+))', ref).group('issue')

    ## Volume and issue
    if 'vol.' in ref:
        # print(ref)
        v = re.search('((vol.)\s?[0-9]+[, ])', ref)
        if v:
            volume = v.group(1)
            volume = volume.strip(',')
            volume = volume.strip('vol.')
            volume = volume.strip()
            v = re.search('((vol.)\s?[0-9]+[, ][A-Za-z]+\s)', ref)
        if v:
            volume = v.group(1)
            volume = volume.strip('vol.')
            volume = volume.strip()

    result['volume'] = volume
    result['issue'] = issue


    ## Year
    y = re.search('([\(](?P<year>\d{4})[\)][\:\,]+)', ref)
    multipleY = re.search('([\(]?(\d{4})[\)]?)(.+?)([\(](?P<year>\d{4})[\)][\:\,]+)', ref)
    if y and (not multipleY):
        year = y.group('year').strip()
    elif multipleY:
        year = multipleY.group('year').strip()

    result['year'] = year


    # PUBLICATION
    pub = ''
    re_title_pub_vol = '[\"\“](?P<title>[\w –\'\-\s\:.,\-\(\)]+[.]?)[\"\”]\s?(?P<publication>[\w\-\'\s\:\,\-\(\)]+)[,]?[\s]?(?P<volume>(vol.)\s?[\w0-9.,\(\)]+)\s?'
    r_title_pub_vol = re.search(re_title_pub_vol, ref)
    re_pub_one = '(.\”)\s(?P<publication>[\w., ]+)\s(vol.)\s*'
    r_pub_one = re.search(re_pub_one, ref)
    re_pub_two = '(.\”)\s(?P<publication>[\w.:\-\;\' ]+)\s[(vol.)(,)]\s*'
    r_pub_two = re.search(re_pub_two, ref)
    if r_title_pub_vol:
        pub = r_title_pub_vol.group('publication').strip(',')
        pub = pub.strip()
    elif r_pub_one:
        pub = r_pub_one.group('publication').strip()   
    elif r_pub_two:
        pub = r_pub_two.group('publication').strip()

    # Check if the journal name is between '].' and 'vol.'
    r_foreign_pub = re.search('(].)\s(?P<publication>[\w\'\-\:\. ]+)\s[(vol.),]\s*', ref)
    if r_foreign_pub: 
        pub = r_foreign_pub.group('publication').strip()

    result['journal'] = pub

    
    # PAGES
    page = ""
    re_page_one = '(?P<year>[\(]?\d{4}[\)]?)[\:\,]?\s(?P<page>(pp.)?\s?[\w\0-9]+)(.)[\n]\s*'
    re_page_two = '(?P<year>[\(]?\d{4}[\)]?)[\:\,]?\s(?P<page>(pp.)?\s?[0-9A-Z\–\-\, ]+)(.)\s*'
    r_page_one = re.search(re_page_one, ref)
    r_page_two = re.search(re_page_two, ref)
    if r_page_one:
        page = r_page_one.group('page')
        page.strip()
    elif r_page_two:
        page = r_page_two.group('page')
        page.strip()

    result['pages'] = page

    # MLA result is a dict with these fields
    # result['title']
    # result['author']
    # result['journal']
    # result['volume']
    # result['issue']
    # result['year']
    # result['pages']

    return result
