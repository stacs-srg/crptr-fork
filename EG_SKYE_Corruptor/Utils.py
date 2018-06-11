import csv
import basefunctions
import random
import time

def readInFile(inputFile):
    recordsDict = {}
    with open(inputFile, "r") as f:
        dataset = csv.reader(f, delimiter=",")

        for row in dataset:
            if not row[0] in recordsDict:
                recordsDict[row[0]] = []

            for value in row[1:]:
                recordsDict[row[0]].append(value)

    return recordsDict


def extractLabels(data, idColumnLabel = "rec-id"):
    print data[idColumnLabel]
    labels = [idColumnLabel] + data[idColumnLabel]
    del data[idColumnLabel]

    return labels

def removeCommas(inputFile, outputFile):

    dataset_file = csv.DictReader(open(inputFile))
    dataset = list(dataset_file)

    for d in dataset:
        for key, value in d.iteritems():
            if "," in d[key]:
                d[key] = d[key].replace(",", "-")
                print d[key]

    fieldnames = dataset[0].keys()
    csvfile = open(outputFile, 'wb')
    csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
    csvwriter.writerow(dict((fn, fn) for fn in fieldnames))

    for r in dataset:
        csvwriter.writerow(r)
    csvfile.close()

    print "Removed commas in strings"

    return outputFile

def addCryptIDs(inputFile, outputFile):

    dataset_file = csv.DictReader(open(inputFile))
    dataset = list(dataset_file)
    count = 0

    for r in dataset:
        r["rec-id"] = "rec-" + str(count) + "-org"
        count += 1
        r["crptr-record"] = "original"

    fieldnames = dataset[0].keys()
    csvfile = open(outputFile, 'wb')
    csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
    csvwriter.writerow(dict((fn, fn) for fn in fieldnames))

    for r in dataset:
        csvwriter.writerow(r)

    csvfile.close()

    print "Added Crptr IDs"

def removeCryptIDs(inputFile, outputFile):

    dataset_file = csv.DictReader(open(inputFile))
    dataset = list(dataset_file)
    dataset_len = str(len(dataset))

    for i in dataset:
        if None in i:
            print i

    for r in dataset:
        del r['rec-id']
        del r['crptr-record']

    fieldnames = dataset[0].keys()
    csvfile = open(outputFile, 'wb')
    csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
    csvwriter.writerow(dict((fn, fn) for fn in fieldnames))

    for r in dataset:
        csvwriter.writerow(r)

    csvfile.close()

    print "Removed Crptr IDs"

def removeOrigonalRecordsForWhichDuplicateExists(inputFile, outputFile):

    dataset_file = csv.DictReader(open(inputFile))
    dataset = list(dataset_file)
    dataset_len = str(len(dataset))
    for i in dataset:
        if None in i:
            print i

    for r in dataset:
        if "dup" in r['rec-id']:
            rec, recid, dup, dupid = r['rec-id'].split('-')
            org_of_dup = rec + "-" + recid + "-org"

            for r2 in dataset:
                if org_of_dup == r2['rec-id']:
                    dataset.remove(r2)

    fieldnames = dataset[0].keys()
    csvfile = open(outputFile, 'wb')
    csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
    csvwriter.writerow(dict((fn, fn) for fn in fieldnames))

    for r in dataset:
        csvwriter.writerow(r)

    csvfile.close()

    print "Removed origonals of corrupted records"


def outputDictToCSV(labels, dict, outputFile, encoding = 'utf_8'):

    rec_id_list = dict.keys()
    rec_id_list.sort()
    rec_list = []

    for rec_id in rec_id_list:
        this_rec_list = [rec_id] + dict[rec_id]
        rec_list.append(this_rec_list)
        # print this_rec_list

    basefunctions.write_csv_file(outputFile, encoding, labels, rec_list)

def setDeterminism(deterministic, seed = None):
    if deterministic:
        random.seed(seed)
    else:
        seed = time.time()
        random.seed(seed)

    print "Used seed: " + str(seed)
