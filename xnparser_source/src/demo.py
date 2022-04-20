"""
    A demo file to demonstrate XNParser functionality
"""
from xnparser import XNParser


ref = "Hanna, K. (2007). Adsorption of aromatic carboxylate compounds on the surface of synthesized iron oxide-coated sands. Applied Geochemistry, 22(9), 2045-2053."

parser = XNParser()

parser.parseRef(ref)

print(parser.getResult())

# print(parser.getStyle())

# print(parser.getAuthor())

# print(parser.getTitle())

# print(parser.getJournal())

# print(parser.getVolume())

# print(parser.getIssue())

# print(parser.getYear())

# print(parser.getPages())
