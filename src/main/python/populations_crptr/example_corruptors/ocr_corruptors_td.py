#!/usr/bin/python
# Author: Tom Dalton (tsd4@st-andrews.ac.uk)
# 5/6/2018
#
# This script reads in files in the format created by Tom Dalton
# ValiPop outputs population records in this form when config includes: output_record_format = TD

from crptr.crptr import Crptr
from populations_crptr.corruptor_definitions.birth_corruptor_td import BirthCorruptorTD
from populations_crptr.corruptor_definitions.death_corruptor_td import DeathCorruptorTD
from populations_crptr.corruptor_definitions.marriage_corruptor_td import MarriageCorruptorTD
from populations_crptr import utils
import csv
import sys

def birthCorruptor(inputFile, outputFile, logFile, lookupFilesDir, deterministic, seed, proportionOfRecordsToCorrupt,
                   maxModificationsPerAttribute, numberOfModificationsPerRecord, recordLevelProportion):
    
    # Set stdout to logfile
    so = sys.stdout
    logOutput = open(logFile, 'w')
    sys.stdout = logOutput

    dataset = list(csv.DictReader(open(inputFile)))

    # add crptr ids
    dataset = utils.addCryptIDs(dataset)

    dataset = utils.convertFromListOfDictsToDictOfLists(dataset)
    labels = utils.extractLabels(dataset)

    corruptor = BirthCorruptorTD(labels, lookupFilesDir)

    utils.setDeterminism(deterministic, seed)

    # data corruption
    numberOfCorruptibleAttributes = 14

    attributeLevelProportion = 1 - recordLevelProportion
    split = attributeLevelProportion / float(numberOfCorruptibleAttributes)

    columnProbabilities = {

        # GROUND TRUTH - DO NOT CORRUPT - ALL VALUES 0
        'ID': 0.0, 'family': 0.0, 'Death': 0.0, 'CHILD_IDENTITY': 0.0,
        'MOTHER_IDENTITY': 0.0, 'FATHER_IDENTITY': 0.0,
        'DEATH_RECORD_IDENTITY': 0.0, 'PARENT_MARRIAGE_RECORD_IDENTITY': 0.0,
        'FATHER_BIRTH_RECORD_IDENTITY': 0.0, 'MOTHER_BIRTH_RECORD_IDENTITY': 0.0,
        'MARRIAGE_RECORD_IDENTITY1': 0.0, 'MARRIAGE_RECORD_IDENTITY2': 0.0,
        'MARRIAGE_RECORD_IDENTITY3': 0.0, 'MARRIAGE_RECORD_IDENTITY4': 0.0,
        'MARRIAGE_RECORD_IDENTITY5': 0.0,

        'crptr-record': recordLevelProportion,

        # CHILD
        'child\'s forname(s)': split, 'child\'s surname': split,
        'birth day': split / 3.0, 'birth month': split / 3.0, 'birth year': split / 3.0,
        'address': split, 'sex': split,

        # FATHER
        'father\'s forename': split, 'father\'s surname': split,
        'father\'s occupation': split,

        # MOTHER
        'mother\'s forename': split, 'mother\'s maiden surname': split,
        'mother\'s occupation': split,

        # MARRIAGE
        'day of parents\' marriage': split / 3.0,
        'month of parents\' marriage': split / 3.0,
        'year of parents\' marriage': split / 3.0,

        'place of parent\'s marriage': split, 'illegit': split

    }

    selectedCorruptors = {

        'crptr-record': [(0.0, corruptor.blankRecord),
                         (0.3, corruptor.dayMonthSwapMarriage),
                         (0.3, corruptor.childNameSwap),
                         (0.2, corruptor.fatherNameSwap),
                         (0.2, corruptor.motherNameSwap)],

        'child\'s forname(s)': corruptor.forenameCorruptionGroupingOCR,

        'child\'s surname': corruptor.surnameCorruptionGroupingOCR,

        'sex': [(0.8, corruptor.sexFlip),
                (0.05, corruptor.missingValue),
                (0.1, corruptor.unknownCharacter),
                (0.05, corruptor.ocr)],

        'father\'s forename': corruptor.forenameCorruptionGroupingOCR,
        'father\'s surname': corruptor.surnameCorruptionGroupingOCR,
        'father\'s occupation': corruptor.occupationCorruptionGroupingOCR,

        'mother\'s forename': corruptor.forenameCorruptionGroupingOCR,
        'mother\'s maiden surname': corruptor.surnameCorruptionGroupingOCR,
        'mother\'s occupation': corruptor.occupationCorruptionGroupingOCR,

        'day of parents\' marriage': corruptor.splitDateCorruptionGroupingOCR,
        'month of parents\' marriage': corruptor.splitDateCorruptionGroupingOCR,
        'year of parents\' marriage': corruptor.splitDateCorruptionGroupingOCR,

        'birth day': corruptor.splitDateCorruptionGroupingOCR,
        'birth month': corruptor.splitDateCorruptionGroupingOCR,
        'birth year': corruptor.splitDateCorruptionGroupingOCR,

        'illegit': [(1.0, corruptor.missingValue)],

        'address': corruptor.addressCorruptionGroupingOCR,
        'place of parent\'s marriage': corruptor.addressCorruptionGroupingOCR

    }

    numberOfRecords = len(dataset)
    numberToModify = int(numberOfRecords * proportionOfRecordsToCorrupt)
    print("Records to be corrupted: " + str(numberToModify))

    crptrInstance = Crptr(number_of_org_records=numberOfRecords,
                                         number_of_mod_records=numberToModify,
                                         attribute_name_list=labels,
                                         max_num_dup_per_rec=1,
                                         num_dup_dist='uniform',
                                         max_num_mod_per_attr=maxModificationsPerAttribute,
                                         num_mod_per_rec=numberOfModificationsPerRecord,
                                         attr_mod_prob_dict=columnProbabilities,
                                         attr_mod_data_dict=selectedCorruptors
                                         )

    records = crptrInstance.corrupt_records(dataset)
    # end of data corruption

    # remove original versions for corrupter records
    utils.removeOrigonalRecordsForWhichDuplicateExists(records, labels)

    # remove crptr ids
    utils.removeCryptIDs(records, labels)

    # Output corrupted data
    utils.outputDictToCSV(labels, records, outputFile)

    # Reset stdout
    sys.stdout = so
    logOutput.close()




def deathCorruptor(inputFile, outputFile, logFile, lookupFilesDir, deterministic, seed, proportionOfRecordsToCorrupt,
                   maxModificationsPerAttribute, numberOfModificationsPerRecord, recordLevelProportion):
    
    # Set stdout to logfile
    so = sys.stdout
    logOutput = open(logFile, 'w')
    sys.stdout = logOutput

    # records = Utils.readInFile(inputFile)

    records = list(csv.DictReader(open(inputFile)))

    # handle commas
    # records = Utils.removeCommas(records)

    # add crptr ids
    records = utils.addCryptIDs(records)

    records = utils.convertFromListOfDictsToDictOfLists(records)
    labels = utils.extractLabels(records)

    corruptor = DeathCorruptorTD(labels, lookupFilesDir)

    utils.setDeterminism(deterministic, seed)

    # data corruption
    numberOfCorruptibleAttributes = 19

    attributeLevelProportion = 1 - recordLevelProportion
    split = attributeLevelProportion / float(numberOfCorruptibleAttributes)

    columnProbabilities = {
        # GROUND TRUTH - DO NOT CORRUPT - ALL VALUES 0
        'ID': 0.0, 'Birth': 0.0, 'mar': 0.0,
        'DECEASED_IDENTITY': 0.0,
        'MOTHER_IDENTITY': 0.0, 'FATHER_IDENTITY': 0.0,
        'SPOUSE_IDENTITY': 0.0, 'BIRTH_RECORD_IDENTITY': 0.0,
        'PARENT_MARRIAGE_RECORD_IDENTITY': 0.0,
        'FATHER_BIRTH_RECORD_IDENTITY': 0.0, 'MOTHER_BIRTH_RECORD_IDENTITY': 0.0,
        'SPOUSE_MARRIAGE_RECORD_IDENTITY': 0.0, 'SPOUSE_BIRTH_RECORD_IDENTITY': 0.0,

        'crptr-record': recordLevelProportion,

        'forename(s) of deceased': split, 'surname of deceased': split,
        'occupation': split, 'marital status': split, 'sex': split,

        'name of spouse': split, 'spouse\'s occ': split,

        'day': split / 3.0, 'month': split / 3.0, 'year': split / 3.0,

        'address': split,

        'age at death': split,

        'father\'s forename': split, 'father\'s surname': split,
        'father\'s occupation': split, 'if father deceased': split,

        'mother\'s forename': split, 'mother\'s maiden surname': split,
        'mother\'s occupation': split, 'if mother deceased': split,

        'death code A': split / 3.0, 'death code B': split / 3.0, 'death code C': split / 3.0

    }

    selectedCorruptors = {

        'crptr-record': [(0.0, corruptor.blankRecord),
                         (0.3, corruptor.dayMonthSwapDeath),
                         (0.3, corruptor.deceasedNameSwap),
                         (0.2, corruptor.fatherNameSwap),
                         (0.2, corruptor.motherNameSwap)],

        'forename(s) of deceased': corruptor.forenameCorruptionGroupingOCR,

        'surname of deceased': corruptor.surnameCorruptionGroupingOCR,

        'marital status': [(0.5, corruptor.marritalStatus),
                           (0.35, corruptor.missingValue),
                           (0.1, corruptor.unknownCharacter),
                           (0.05, corruptor.ocr)],

        'occupation': corruptor.occupationCorruptionGroupingOCR,

        'sex': [(0.8, corruptor.sexFlip),
                (0.05, corruptor.missingValue),
                (0.1, corruptor.unknownCharacter),
                (0.05, corruptor.ocr)],

        'name of spouse': [(0.3, corruptor.ocr),
                              (0.1, corruptor.unknownCharacter),
                              (0.25, corruptor.missingValue),
                              (0.35, corruptor.phoneticVariation)],

        'spouse\'s occ': corruptor.occupationCorruptionGroupingOCR,

        'day': corruptor.splitDateCorruptionGroupingOCR,
        'month': corruptor.splitDateCorruptionGroupingOCR,
        'year': corruptor.splitDateCorruptionGroupingOCR,

        'age at death': [(0.3, corruptor.ocr),
                         (0.3, corruptor.unknownCharacter),
                         (0.4, corruptor.missingValue)],

        'father\'s forename': corruptor.forenameCorruptionGroupingOCR,
        'father\'s surname': corruptor.surnameCorruptionGroupingOCR,
        'if father deceased': corruptor.deceasedCorruptionGroupingOCR,
        'father\'s occupation': corruptor.occupationCorruptionGroupingOCR,

        'mother\'s forename': corruptor.forenameCorruptionGroupingOCR,
        'mother\'s maiden surname': corruptor.surnameCorruptionGroupingOCR,
        'if mother deceased': corruptor.deceasedCorruptionGroupingOCR,
        'mother\'s occupation': corruptor.occupationCorruptionGroupingOCR,

        'death code A': [(0.7, corruptor.ocr),
                           (0.3, corruptor.missingValue)],

        'death code B': [(0.7, corruptor.ocr),
                         (0.3, corruptor.missingValue)],

        'death code C': [(0.7, corruptor.ocr),
                         (0.3, corruptor.missingValue)],

        'address': corruptor.addressCorruptionGroupingOCR

    }

    numberOfRecords = len(records)
    numberToModify = int(numberOfRecords * proportionOfRecordsToCorrupt)
    print("Records to be corrupted: " + str(numberToModify))

    crptrInstance = Crptr(number_of_org_records=numberOfRecords,
                                         number_of_mod_records=numberToModify,
                                         attribute_name_list=labels,
                                         max_num_dup_per_rec=1,
                                         num_dup_dist='uniform',
                                         max_num_mod_per_attr=maxModificationsPerAttribute,
                                         num_mod_per_rec=numberOfModificationsPerRecord,
                                         attr_mod_prob_dict=columnProbabilities,
                                         attr_mod_data_dict=selectedCorruptors
                                         )

    records = crptrInstance.corrupt_records(records)
    # end of data corruption

    # remove original versions for corrupter records
    utils.removeOrigonalRecordsForWhichDuplicateExists(records, labels)

    # remove crptr ids
    utils.removeCryptIDs(records, labels)

    # Output corrupted data
    utils.outputDictToCSV(labels, records, outputFile)




def marriageCorruptor(inputFile, outputFile, logFile, lookupFilesDir, deterministic, seed, proportionOfRecordsToCorrupt,
                   maxModificationsPerAttribute, numberOfModificationsPerRecord, recordLevelProportion):
    
    # Set stdout to logfile
    so = sys.stdout
    logOutput = open(logFile, 'w')
    sys.stdout = logOutput

    # records = Utils.readInFile(inputFile)

    records = list(csv.DictReader(open(inputFile)))

    # handle commas
    # records = Utils.removeCommas(records)

    # add crptr ids
    records = utils.addCryptIDs(records)

    records = utils.convertFromListOfDictsToDictOfLists(records)
    labels = utils.extractLabels(records)

    corruptor = MarriageCorruptorTD(labels, lookupFilesDir)

    utils.setDeterminism(deterministic, seed)

    # data corruption
    numberOfCorruptibleAttributes = 28

    attributeLevelProportion = 1 - recordLevelProportion
    split = attributeLevelProportion / float(numberOfCorruptibleAttributes)

    columnProbabilities = {
        # GROUND TRUTH - DO NOT CORRUPT - ALL VALUES 0
        'ID': 0.0,
        'gdeath': 0.0, 'bdeath': 0.0,
        'GROOM_IDENTITY': 0.0, 'BRIDE_IDENTITY': 0.0,
        'GROOM_MOTHER_IDENTITY': 0.0, 'GROOM_FATHER_IDENTITY': 0.0,
        'BRIDE_MOTHER_IDENTITY': 0.0, 'BRIDE_FATHER_IDENTITY': 0.0,
        'GROOM_BIRTH_RECORD_IDENTITY': 0.0, 'BRIDE_BIRTH_RECORD_IDENTITY': 0.0,
        'GROOM_FATHER_BIRTH_RECORD_IDENTITY': 0.0, 'GROOM_MOTHER_BIRTH_RECORD_IDENTITY': 0.0,
        'BRIDE_FATHER_BIRTH_RECORD_IDENTITY': 0.0, 'BRIDE_MOTHER_BIRTH_RECORD_IDENTITY': 0.0,

        'crptr-record': recordLevelProportion,

        'day': split / 3.0, 'month': split / 3.0, 'year': split / 3.0,
        'place of marriage': split,

        'forename of groom': split, 'surname of groom': split,
        'occupation of groom': split, 'marital status of groom': split,
        'age of groom': split, 'address of groom': split,

        'forename of bride': split, 'surname of bride': split,
        'occupation of bride': split, 'marital status of bride': split,
        'age of bride': split, 'address of bride': split,

        'groom\'s father\'s forename': split, 'groom\'s father\'s surname': split,
        'groom\'s father\'s occupation': split, 'if groom\'s father deceased': split,

        'groom\'s mother\'s forename': split, 'groom\'s mother\'s maiden surname': split,
        'if groom\'s mother deceased': split,

        'bride\'s father\'s forename': split, 'bride\'s father\'s surname': split,
        'bride\'s father\'s occupation': split, 'if bride\'s father deceased': split,

        'bride\'s mother\'s forename': split, 'bride\'s mother\'s maiden surname': split,
        'if bride\'s mother deceased': split
    }

    selectedCorruptors = {

        'crptr-record': [(0.0, corruptor.blankRecord),
                         (0.1, corruptor.dayMonthSwapDeath),
                         (0.15, corruptor.groomNameSwap),
                         (0.15, corruptor.brideNameSwap),
                         (0.15, corruptor.brideMotherNameSwap),
                         (0.15, corruptor.brideFatherNameSwap),
                         (0.15, corruptor.groomMotherNameSwap),
                         (0.15, corruptor.groomFatherNameSwap)],

        'forename of groom': corruptor.forenameCorruptionGroupingOCR,
        'surname of groom': corruptor.surnameCorruptionGroupingOCR,
        'occupation of groom': corruptor.forenameCorruptionGroupingOCR,

        'marital status of groom': [(0.5, corruptor.marritalStatus),
                           (0.1, corruptor.unknownCharacter),
                           (0.4, corruptor.ocr)],

        'age of groom': [(0.7, corruptor.ocr),
                         (0.3, corruptor.unknownCharacter)],

        'address of groom': corruptor.addressCorruptionGroupingOCR,

        'forename of bride': corruptor.forenameCorruptionGroupingOCR,
        'surname of bride': corruptor.surnameCorruptionGroupingOCR,
        'occupation of bride': corruptor.forenameCorruptionGroupingOCR,

        'marital status of bride': [(0.5, corruptor.marritalStatus),
                                    (0.35, corruptor.missingValue),
                                    (0.1, corruptor.unknownCharacter),
                                    (0.05, corruptor.ocr)],

        'age of bride': [(0.7, corruptor.keyboardShift),
                         (0.3, corruptor.unknownCharacter)],

        'address of bride': corruptor.addressCorruptionGroupingOCR,

        'day': corruptor.splitDateCorruptionGroupingOCR,
        'month': corruptor.splitDateCorruptionGroupingOCR,
        'year': corruptor.splitDateCorruptionGroupingOCR,

        'place of marriage': corruptor.addressCorruptionGroupingOCR,

        'groom\'s father\'s forename': corruptor.forenameCorruptionGroupingOCR,
        'groom\'s father\'s surname': corruptor.surnameCorruptionGroupingOCR,
        'groom\'s father\'s occupation': corruptor.occupationCorruptionGroupingOCR,
        'if groom\'s father deceased': corruptor.deceasedCorruptionGroupingOCR,

        'bride\'s father\'s forename': corruptor.forenameCorruptionGroupingOCR,
        'bride\'s father\'s surname': corruptor.surnameCorruptionGroupingOCR,
        'bride\'s father\'s occupation': corruptor.occupationCorruptionGroupingOCR,
        'if bride\'s father deceased': corruptor.deceasedCorruptionGroupingOCR,

        'groom\'s mother\'s forename': corruptor.forenameCorruptionGroupingOCR,
        'groom\'s mother\'s maiden surname': corruptor.surnameCorruptionGroupingOCR,
        'if groom\'s mother deceased': corruptor.deceasedCorruptionGroupingOCR,

        'bride\'s mother\'s forename': corruptor.forenameCorruptionGroupingOCR,
        'bride\'s mother\'s maiden surname': corruptor.surnameCorruptionGroupingOCR,
        'if bride\'s mother deceased': corruptor.deceasedCorruptionGroupingOCR

    }

    numberOfRecords = len(records)
    numberToModify = int(numberOfRecords * proportionOfRecordsToCorrupt)
    print("Records to be corrupted: " + str(numberToModify))

    crptrInstance = Crptr(number_of_org_records=numberOfRecords,
                                         number_of_mod_records=numberToModify,
                                         attribute_name_list=labels,
                                         max_num_dup_per_rec=1,
                                         num_dup_dist='uniform',
                                         max_num_mod_per_attr=maxModificationsPerAttribute,
                                         num_mod_per_rec=numberOfModificationsPerRecord,
                                         attr_mod_prob_dict=columnProbabilities,
                                         attr_mod_data_dict=selectedCorruptors
                                         )

    records = crptrInstance.corrupt_records(records)
    # end of data corruption

    # remove original versions for corrupter records
    utils.removeOrigonalRecordsForWhichDuplicateExists(records, labels)

    # remove crptr ids
    utils.removeCryptIDs(records, labels)

    # Output corrupted data
    utils.outputDictToCSV(labels, records, outputFile)


