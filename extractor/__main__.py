from pyquery import PyQuery as pq


def extract_saints(d, position):
    saints = []
    selector = f"div.article__text > ul:nth-child({position})> li > a"
    p = d(selector)
    for a in p:
        saints.append(a.text)
    return saints


def saints():
    d = pq(filename="data/święci.html")
    female_saints = extract_saints(d, 12)
    male_saints = extract_saints(d, 16)
    return female_saints, male_saints


def patrons():
    patrons = []
    d = pq(filename="data/patroni.html")
    p = d("table")
    return patrons


def merged(saints_data, patrons_data):
    merged = []
    return merged


def main():
    print("Starting...")

    print("Saints...")
    saints_data = saints()
    female_saints_data, male_saints_data = saints_data
    print(female_saints_data)
    print(male_saints_data)
    print()

    print("Patrons...")
    patrons_data = patrons()
    print(patrons_data)
    print()

    print("Merged...")
    merged_data = merged(saints_data, patrons_data)
    print(merged_data)
    print()

    print("Ending...")


main()
