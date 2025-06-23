#!/usr/bin/python
# Author: Tom Dalton (tsd4@st-andrews.ac.uk)
# 5/6/2018
#
# This script reads in files in the format created by Tom Dalton
# ValiPop outputs population records in this form when config includes: output_record_format = TD

from crptr.crptr import Crptr
from crptr.synthetic_populations.corruptor_definitions.birth_corruptors import BirthCorruptors
from crptr.synthetic_populations.corruptor_definitions.death_corruptors import DeathCorruptors
from crptr.synthetic_populations.corruptor_definitions.marriage_corruptors import MarriageCorruptors
from . import utils
import sys
import csv

def birthCorruptor(inputFile, outputFile, logFile, lookupFilesDir, deterministic, seed, proportionOfRecordsToCorrupt,
                   maxModificationsPerAttribute, numberOfModificationsPerRecord, recordLevelProportion):
    so = sys.stdout
    logOutput = open(logFile, 'w')
    sys.stdout = logOutput

    dataset = list(csv.DictReader(open(inputFile)))

    # add crptr ids
    dataset = utils.addCryptIDs(dataset)

    dataset = utils.convertFromListOfDictsToDictOfLists(dataset)
    labels = utils.extractLabels(dataset)

    corruptor = BirthCorruptors(labels, lookupFilesDir)

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

        'child\'s forname(s)': corruptor.forenameCorruptionGrouping,

        'child\'s surname': corruptor.surnameCorruptionGrouping,

        'sex': [(0.8, corruptor.sexFlip),
                (0.05, corruptor.missingValue),
                (0.1, corruptor.unknownCharacter),
                (0.05, corruptor.keyboardShift)],

        'father\'s forename': corruptor.forenameCorruptionGrouping,
        'father\'s surname': corruptor.surnameCorruptionGrouping,
        'father\'s occupation': corruptor.occupationCorruptionGrouping,

        'mother\'s forename': corruptor.forenameCorruptionGrouping,
        'mother\'s maiden surname': corruptor.surnameCorruptionGrouping,
        'mother\'s occupation': corruptor.occupationCorruptionGrouping,

        'day of parents\' marriage': corruptor.splitDateCorruptionGrouping,
        'month of parents\' marriage': corruptor.splitDateCorruptionGrouping,
        'year of parents\' marriage': corruptor.splitDateCorruptionGrouping,

        'birth day': corruptor.splitDateCorruptionGrouping,
        'birth month': corruptor.splitDateCorruptionGrouping,
        'birth year': corruptor.splitDateCorruptionGrouping,

        'illegit': [(1.0, corruptor.missingValue)],

        'address': corruptor.addressCorruptionGrouping,
        'place of parent\'s marriage': corruptor.addressCorruptionGrouping

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

    sys.stdout = so
    logOutput.close()



def deathCorruptor(inputFile, outputFile, logFile, lookupFilesDir, deterministic, seed, proportionOfRecordsToCorrupt,
                   maxModificationsPerAttribute, numberOfModificationsPerRecord, recordLevelProportion):
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

    corruptor = DeathCorruptors(labels, lookupFilesDir)

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

        'forename(s) of deceased': corruptor.forenameCorruptionGrouping,

        'surname of deceased': corruptor.surnameCorruptionGrouping,

        'marital status': [(0.5, corruptor.marritalStatus),
                           (0.35, corruptor.missingValue),
                           (0.1, corruptor.unknownCharacter),
                           (0.05, corruptor.keyboardShift)],

        'occupation': corruptor.occupationCorruptionGrouping,

        'sex': [(0.8, corruptor.sexFlip),
                (0.05, corruptor.missingValue),
                (0.1, corruptor.unknownCharacter),
                (0.05, corruptor.keyboardShift)],

        'name of spouse': [(0.2, corruptor.generalCharacter),
                              (0.1, corruptor.keyboardShift),
                              (0.1, corruptor.unknownCharacter),
                              (0.25, corruptor.missingValue),
                              (0.35, corruptor.phoneticVariation)],

        'spouse\'s occ': corruptor.occupationCorruptionGrouping,

        'day': corruptor.splitDateCorruptionGrouping,
        'month': corruptor.splitDateCorruptionGrouping,
        'year': corruptor.splitDateCorruptionGrouping,

        'age at death': [(0.3, corruptor.keyboardShift),
                         (0.3, corruptor.unknownCharacter),
                         (0.4, corruptor.missingValue)],

        'father\'s forename': corruptor.forenameCorruptionGrouping,
        'father\'s surname': corruptor.surnameCorruptionGrouping,
        'if father deceased': corruptor.deceasedCorruptionGrouping,
        'father\'s occupation': corruptor.occupationCorruptionGrouping,

        'mother\'s forename': corruptor.forenameCorruptionGrouping,
        'mother\'s maiden surname': corruptor.surnameCorruptionGrouping,
        'if mother deceased': corruptor.deceasedCorruptionGrouping,
        'mother\'s occupation': corruptor.occupationCorruptionGrouping,

        'death code A': [(0.6, corruptor.generalCharacter),
                           (0.1, corruptor.keyboardShift),
                           (0.3, corruptor.missingValue)],

        'death code B': [(0.6, corruptor.generalCharacter),
                         (0.1, corruptor.keyboardShift),
                         (0.3, corruptor.missingValue)],

        'death code C': [(0.6, corruptor.generalCharacter),
                         (0.1, corruptor.keyboardShift),
                         (0.3, corruptor.missingValue)],

        'address': corruptor.addressCorruptionGrouping

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

    sys.stdout = so
    logOutput.close()


def marriageCorruptor(inputFile, outputFile, logFile, lookupFilesDir, deterministic, seed, proportionOfRecordsToCorrupt,
                   maxModificationsPerAttribute, numberOfModificationsPerRecord, recordLevelProportion):
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

    corruptor = MarriageCorruptors(labels, lookupFilesDir)

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

        'forename of groom': corruptor.forenameCorruptionGrouping,
        'surname of groom': corruptor.surnameCorruptionGrouping,
        'occupation of groom': corruptor.forenameCorruptionGrouping,
        'marital status of groom': [(0.5, corruptor.marritalStatus),
                           (0.35, corruptor.missingValue),
                           (0.1, corruptor.unknownCharacter),
                           (0.05, corruptor.keyboardShift)],

        'age of groom': [(0.3, corruptor.keyboardShift),
                         (0.3, corruptor.unknownCharacter),
                         (0.4, corruptor.missingValue)],

        'address of groom': corruptor.addressCorruptionGrouping,

        'forename of bride': corruptor.forenameCorruptionGrouping,
        'surname of bride': corruptor.surnameCorruptionGrouping,
        'occupation of bride': corruptor.forenameCorruptionGrouping,
        'marital status of bride': [(0.5, corruptor.marritalStatus),
                                    (0.35, corruptor.missingValue),
                                    (0.1, corruptor.unknownCharacter),
                                    (0.05, corruptor.keyboardShift)],

        'age of bride': [(0.3, corruptor.keyboardShift),
                         (0.3, corruptor.unknownCharacter),
                         (0.4, corruptor.missingValue)],

        'address of bride': corruptor.addressCorruptionGrouping,

        'day': corruptor.splitDateCorruptionGrouping,
        'month': corruptor.splitDateCorruptionGrouping,
        'year': corruptor.splitDateCorruptionGrouping,

        'place of marriage': corruptor.addressCorruptionGrouping,

        'groom\'s father\'s forename': corruptor.forenameCorruptionGrouping,
        'groom\'s father\'s surname': corruptor.surnameCorruptionGrouping,
        'groom\'s father\'s occupation': corruptor.occupationCorruptionGrouping,
        'if groom\'s father deceased': corruptor.deceasedCorruptionGrouping,

        'bride\'s father\'s forename': corruptor.forenameCorruptionGrouping,
        'bride\'s father\'s surname': corruptor.surnameCorruptionGrouping,
        'bride\'s father\'s occupation': corruptor.occupationCorruptionGrouping,
        'if bride\'s father deceased': corruptor.deceasedCorruptionGrouping,

        'groom\'s mother\'s forename': corruptor.forenameCorruptionGrouping,
        'groom\'s mother\'s maiden surname': corruptor.surnameCorruptionGrouping,
        'if groom\'s mother deceased': corruptor.deceasedCorruptionGrouping,

        'bride\'s mother\'s forename': corruptor.forenameCorruptionGrouping,
        'bride\'s mother\'s maiden surname': corruptor.surnameCorruptionGrouping,
        'if bride\'s mother deceased': corruptor.deceasedCorruptionGrouping

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

    sys.stdout = so
    logOutput.close()
