import csv
import itertools

import pyquery


def extract_saints(d, position):
    result = []

    selector = f"div.article__text > ul:nth-child({position})> li > a"
    p = d(selector)

    for node in p:
        result.append(node.text)
    return result


def saints():
    # https://parenting.pl/imiona-swietych-swiete-imiona-zenskie-i-meskie
    d = pyquery.PyQuery(filename="data/święci.html")
    female_saints = extract_saints(d, 12)
    male_saints = extract_saints(d, 16)
    return set(female_saints), set(male_saints)


def td(d, td_class):
    selector = f"body > div[align=center] > table > tbody > tr > td.{td_class}"
    p = d(selector)
    texts = []
    for node in p:
        texts.append(node.text)
    return texts


def process_names(names):
    first = True
    processed_names = []
    for name in names:
        if first:
            first = False
            continue
        processed_names.append(name)
    return processed_names


def process_patronages(patronages):
    first = True
    processed_patronages = []
    for patronage in patronages:
        if first:
            first = False
            continue
        processed_patronage = patronage.removeprefix("Patron ")
        processed_patronage = processed_patronage.removeprefix("Patronka ")
        processed_patronages.append(processed_patronage)
    return processed_patronages


def patrons():
    # https://patroni.waw.pl
    d = pyquery.PyQuery(filename="data/patroni.html")
    names = td(d, "a")
    patronages = td(d, "b")

    processed_names = process_names(names)
    processed_patronages = process_patronages(patronages)

    return list(zip(processed_names, processed_patronages))


def possible_patrons(patron_names, name):
    result = []
    for patron in patron_names:
        if name in patron:
            result.append(patron)
    return result


def merge(saints_data, patrons_data):
    name_to_patronage = {name: patronage for name, patronage in patrons_data}
    patron_names = [name for name, _ in patrons_data]
    result = []
    for name in saints_data:
        try:
            local_patrons = possible_patrons(patron_names, name)
            for local_patron in local_patrons:
                patronage = name_to_patronage[local_patron]
                result.append((local_patron, patronage))
        except KeyError as exception:
            missing = exception.args[0]
            print(f"Not found: {missing}.")
    return result


def merged(saints_data, patrons_data):
    female_saints_data, male_saints_data = saints_data
    female_merged = merge(female_saints_data, patrons_data)
    male_merged = merge(male_saints_data, patrons_data)
    return female_merged, male_merged


def main():
    print("Starting...")

    print("Saints...")
    saints_data = saints()
    female_saints_data, male_saints_data = saints_data
    print("Female...")
    print(female_saints_data)
    print("Male...")
    print(male_saints_data)
    print()

    print("Patrons...")
    patrons_data = patrons()
    print(patrons_data)
    print()

    print("Merged...")
    merged_data = merged(saints_data, patrons_data)
    print(merged_data)
    female_merged_data, male_merged_data = merged_data
    print()

    print("Saving...")
    with open("extracted.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        for name, patronage in itertools.chain(female_merged_data, male_merged_data):
            csv_writer.writerow((name, patronage))
    print()

    print("Ending...")


main()
