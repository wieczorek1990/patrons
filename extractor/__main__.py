from pyquery import PyQuery as pq
from lxml import etree

parser = etree.HTMLParser()

def saints():
    saints = []
    tree = etree.parse("data/święci.html", parser)
    return saints


def patrons():
    patrons = []
    tree = etree.parse("data/patroni.html", parser)
    return patrons


def merged(saints_data, patrons_data):
    merged = []
    return merged


def main():
    print("Starting...")
    print("Saints...")
    saints_data = saints()
    print("Patrons...")
    patrons_data = patrons()
    print("Merged...")
    merged_data = merged(saints_data, patrons_data)
    print(merged_data)
    print("Ending...")


main()
