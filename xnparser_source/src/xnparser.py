import pip
import requests
import urllib.parse

from cermine import runCermine
from mla import runMLA 
from apa import runAPA
from ama import runAMA


class XNParser:
    """
    A class used to create a bibliographical reference parser
    
    ...

    Attributes
    ----------
    ref : str
        the raw bibliographical reference
    result : dict
        the result after parsing the reference containing all parsed fields
    style : str
        the citation style of the reference
    title : str
        the title of the reference
    author : str
        the author of the reference   
    journal : str
        the journal of the reference
    volume : str
        the volume of the reference
    issue : str
        the issue of the reference  
    year : str
        the year of the reference
    pages : str
        the pages of the reference

    Methods
    -------
    parseRef(ref) : str
        Parses the bibliographical reference
    getResult() : dict  
        Gets the result after parsing the reference containing all parsed fields
    getStyle() : str
        Gets the citation style of the reference
    getTitle() : str
        Gets the title of the reference
    getAuthor() : str
        Gets the author of the reference
    getJournal() : str
        Gets the journal of the reference
    getVolume() : str
        Gets the volume of the reference
    getIssue() : str
        Gets the issue of the reference
    getYear() : str
        Gets the year of the reference
    getPages() : str
        Gets the pages of the reference
    """

    def __init__(self):
        """
        Constructs an XNParser
        """
        self.__setup()

        self.ref = ""
        self.style = ""

        self.result = {}
        self.title = ""
        self.author = ""
        self.journal = ""
        self.volume = ""
        self.issue = ""
        self.year = ""
        self.pages = ""

        self.start = False


    ##### PUBLIC METHODS #####

    def parseRef(self, ref):
        """
        Parses the bibliographical reference

        Args:
            ref (str): the raw bibliographical reference
        """
        self.ref = ref
        self.__idStyle()

        styles = ["modern-language-association", "apa", "vancouver"]

        if (self.style in styles):
            self.__runRegEx()
        else:
            self.__runCermine()
        
        self.start = True


    def getResult(self):
        """
        Gets the result after parsing the reference containing all parsed fields

        Returns:
            dict: the result after parsing the reference containing all parsed fields or empty

        Raises:
            SystemError: if parseRef(ref) was not run first    
        """
        self.__isValid()
        return self.result


    def getStyle(self):
        """
        Gets the citation style of the reference

        Returns:
            str: the citation style of the reference or "none"

        Raises:
            SystemError: if parseRef(ref) was not run first     
        """
        self.__isValid()
        return self.style


    def getTitle(self):
        """
        Gets the title of the reference

        Returns:
            str: the title of the reference or "none"

        Raises:
            SystemError: if parseRef(ref) was not run first 
        """
        if (self.__isEmpty(self.title)):
            return "none"
        return self.title


    def getAuthor(self):
        """
        Gets the author of the reference

        Returns:
            str: the author of the reference or "none"

        Raises:
            SystemError: if parseRef(ref) was not run first     
        """
        self.__isValid()

        if (self.__isEmpty(self.author)):
            return "none"
        return self.author


    def getJournal(self):
        """
        Gets the journal of the reference

        Returns:
            str: the journal of the reference or "none"
        
        Raises:
            SystemError: if parseRef(ref) was not run first 
        """
        if (self.__isEmpty(self.journal)):
            return "none"
        return self.journal


    def getVolume(self):
        """
        Gets the volume of the reference

        Returns:
            str: the volume of the reference or "none"
        
        Raises:
            SystemError: if parseRef(ref) was not run first 
        """
        if (self.__isEmpty(self.volume)):
            return "none"
        return self.volume


    def getIssue(self):
        """
        Gets the issue of the reference

        Returns:
            str: the issue of the reference or "none"
        
        Raises:
            SystemError: if parseRef(ref) was not run first 
        """
        if (self.__isEmpty(self.issue)):
            return "none"
        return self.issue


    def getYear(self):
        """
        Gets the year of the reference

        Returns:
            str: the year of the reference or "none"
        
        Raises:
            SystemError: if parseRef(ref) was not run first 
        """
        if (self.__isEmpty(self.year)):
            return "none"
        return self.year


    def getPages(self):
        """
        Gets the pages of the reference

        Returns:
            str: the pages of the reference or "none"
        
        Raises:
            SystemError: if parseRef(ref) was not run first 
        """
        if (self.__isEmpty(self.issue)):
            return "none"
        return self.pages


    ##### PRIVATE METHODS #####

    def __setup(self):
        required = ['requests', 're', 'subprocess', 'urllib.parse']

        for req in required:
            try:
                return __import__(req)
            except ImportError:
                pip.main(['install', req])


    def __isValid(self):
        if not self.start:
            raise SystemError("run parseRef(ref) first")


    def __isEmpty(self, field):
        if field == "":
            return True
        return False


    def __idStyle(self):
        api = 'http://styleclass.labs.crossref.org/citationstyle/'
        query = urllib.parse.quote(self.ref)
        r = requests.get(api + query)
        
        self.style = r.json()['citation_style']


    def __runRegEx(self):
        res = {}

        if self.style == "modern-language-association":
            res = runMLA(self.ref)

        elif self.style == "apa":
            res = runAPA(self.ref)   

        elif self.style == "vancouver":
            res = runAMA(self.ref) 

        self.result = res
        self.title = res['title'] if 'title' in res else ""
        self.author = res['author'] if 'author' in res else ""
        self.volume = res['volume'] if 'volume' in res else ""
        self.issue = res['issue'] if 'issue' in res else ""
        self.year = res['year'] if 'year' in res else ""
        self.journal = res['journal'] if 'journal' in res else ""
        self.pages = res['pages'] if 'pages' in res else ""


    def __runCermine(self):
        res = runCermine(self.ref)

        self.result = res
        self.title = res['title'] if 'title' in res else ""
        self.author = res['author'] if 'author' in res else ""
        self.volume = res['volume'] if 'volume' in res else ""
        self.issue = res['issue'] if 'issue' in res else ""
        self.year = res['year'] if 'year' in res else ""
        self.journal = res['journal'] if 'journal' in res else ""
        self.pages = res['pages'] if 'pages' in res else ""
