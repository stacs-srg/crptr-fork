#!/usr/bin/python
# Author: Tom Dalton (tsd4@st-andrews.ac.uk)
# 5/6/2018
#
# This script reads in files in the format provided by Eilidh Garrett for the Skye data
# ValiPop outputs population records in this form when config includes: output_record_format = EG_SKYE
# This script performs corruption based on a provided config file
# This script then outputs the corrupted records to new files ready to be used with linkage-java

import os

import EGCorruptorDefinitions
import Utils
import crptr
import sys


def birthCorruptor(inputFile, outputFile, logFile, lookupFilesDir, deterministic, seed, proportionOfRecordsToCorrupt,
                   maxModificationsPerAttribute, numberOfModificationsPerRecord, recordLevelProportion):
    so = sys.stdout
    logOutput = open(logFile, 'w')
    sys.stdout = logOutput

    tempFile = "temp.csv"

    # handle commas
    Utils.removeCommas(inputFile, tempFile)

    # add crptr ids
    Utils.addCryptIDs(tempFile, tempFile)

    # read in source file
    records = Utils.readInFile(tempFile)

    labels = Utils.extractLabels(records)

    corruptor = EGCorruptorDefinitions.BirthCorruptors(labels, lookupFilesDir)

    Utils.setDeterminism(deterministic, seed)

    # data corruption
    numberOfCorruptibleAttributes = 11

    attributeLevelProportion = 1 - recordLevelProportion
    split = attributeLevelProportion / float(numberOfCorruptibleAttributes)

    columnProbabilities = {
        # GROUND TRUTH - DO NOT CORRUPT - ALL VALUES 0
        'ID': 0.0, 'family': 0.0, 'marriage': 0.0, 'Death': 0.0,
        'crptr-record': recordLevelProportion,
        # CHILD
        'child\'s forname(s)': split, 'child\'s surname': split, 'birth date': split, 'sex': split,
        # FATHER
        'father\'s forename': split, 'father\'s surname': split,
        # MOTHER
        'mother\'s forename': split, 'mother\'s maiden surname': split,
        # MARRIAGE
        'day of parents\' marriage': split / 3.0, 'month of parents\' marriage': split / 3.0,
        'year of parents\' marriage': split / 3.0,
        # REGISTRATION
        'day of reg': split / 3.0, 'month of reg': split / 3.0, 'year of reg': split / 3.0,
        'illegit': split,

        # OTHER POPULATED FIELDS
        'notes1': 0.0, 'marriageBaby': 0.0,

        # UNPOPULATED FIELDS
        'mother\'s occupation': 0.0,
        'father\'s occupation': 0.0,
        'address 1': 0.0, 'address 2': 0.0,
        'IOSBIRTH_Identifier': 0.0, 'corrected': 0.0, 'source': 0.0, 'line no': 0.0,
        'RD Identifier': 0.0, 'IOS_RDIdentifier': 0.0, 'IOS_RSDIdentifier': 0.0,
        'register identifier': 0.0, 'IOS_RegisterNumber': 0.0, 'IOS_Entry no': 0.0,
        'IOS_RegisterYear': 0.0, 'sschild': 0.0, 'sxchild': 0.0, 'ssfather': 0.0, 'sxfather': 0.0,
        'ssmother': 0.0, 'sxmother': 0.0, 'place of parent\'s marriage 1': 0.0,
        'place of parent\'s marriage 2': 0.0, 'forename of informant': 0.0,
        'surname of informant': 0.0, 'relationship of informant to child': 0.0,
        'did inform sign?': 0.0, 'was inform present?': 0.0, 'notes2': 0.0, 'notes3': 0.0,
        'repeats': 0.0, 'edits': 0.0, 'latepid': 0.0, 'latesch': 0.0

    }

    selectedCorruptors = {

        'crptr-record': [(0.0, corruptor.blankRecord),
                         (0.2, corruptor.dayMonthSwapMarriage),
                         (0.2, corruptor.dayMonthSwapRegistration),
                         (0.2, corruptor.childNameSwap),
                         (0.2, corruptor.fatherNameSwap),
                         (0.2, corruptor.motherNameSwap)],

        'child\'s forname(s)': corruptor.forenameCorruptionGrouping,

        'child\'s surname': corruptor.surnameCorruptionGrouping,

        'birth date': [(0.95, corruptor.dateDDMMYYYY),
                       (0.05, corruptor.missingValue)],

        'sex': [(0.8, corruptor.sexFlip),
                (0.05, corruptor.missingValue),
                (0.1, corruptor.unknownCharacter),
                (0.05, corruptor.keyboardShift)],

        'father\'s forename': corruptor.forenameCorruptionGrouping,
        'father\'s surname': corruptor.surnameCorruptionGrouping,

        'mother\'s forename': corruptor.forenameCorruptionGrouping,
        'mother\'s maiden surname': corruptor.surnameCorruptionGrouping,

        'day of parents\' marriage': corruptor.splitDateCorruptionGrouping,
        'month of parents\' marriage': corruptor.splitDateCorruptionGrouping,
        'year of parents\' marriage': corruptor.splitDateCorruptionGrouping,

        'day of reg': corruptor.splitDateCorruptionGrouping,
        'month of reg': corruptor.splitDateCorruptionGrouping,
        'year of reg': corruptor.splitDateCorruptionGrouping,

        'illegit': [(1.0, corruptor.missingValue)]

    }

    numberOfRecords = len(records)
    numberToModify = int(numberOfRecords * proportionOfRecordsToCorrupt)
    print "Records to be corrupted: " + str(numberToModify)

    crptrInstance = crptr.CorruptDataSet(number_of_org_records=numberOfRecords,
                                         number_of_mod_records=numberToModify,
                                         attribute_name_list=labels[1:],
                                         max_num_dup_per_rec=1,
                                         num_dup_dist='uniform',
                                         max_num_mod_per_attr=maxModificationsPerAttribute,
                                         num_mod_per_rec=numberOfModificationsPerRecord,
                                         attr_mod_prob_dict=columnProbabilities,
                                         attr_mod_data_dict=selectedCorruptors
                                         )

    records = crptrInstance.corrupt_records(records)
    # end of data corruption

    # Output corrupted data to temp file before cleanup
    Utils.outputDictToCSV(labels, records, tempFile)

    # remove original versions for corrupter records
    Utils.removeOrigonalRecordsForWhichDuplicateExists(tempFile, tempFile)

    # remove crptr ids
    Utils.removeCryptIDs(tempFile, outputFile)

    # clean up temp file
    os.remove(tempFile)

    sys.stdout = so
    logOutput.close()


def deathCorruptor(inputFile, outputFile, logFile, lookupFilesDir, deterministic, seed, proportionOfRecordsToCorrupt,
                   maxModificationsPerAttribute, numberOfModificationsPerRecord, recordLevelProportion):
    so = sys.stdout
    logOutput = open(logFile, 'w')
    sys.stdout = logOutput

    tempFile = "temp.csv"

    # handle commas
    Utils.removeCommas(inputFile, tempFile)

    # add crptr ids
    Utils.addCryptIDs(tempFile, tempFile)

    # read in source file
    records = Utils.readInFile(tempFile)

    labels = Utils.extractLabels(records)

    corruptor = EGCorruptorDefinitions.DeathCorruptors(labels, lookupFilesDir)

    Utils.setDeterminism(deterministic, seed)

    # data corruption
    numberOfCorruptibleAttributes = 15

    attributeLevelProportion = 1 - recordLevelProportion
    split = attributeLevelProportion / float(numberOfCorruptibleAttributes)

    columnProbabilities = {
        # GROUND TRUTH - DO NOT CORRUPT - ALL VALUES 0
        'ID': 0.0, 'Birth': 0.0, 'mar': 0.0,

        'crptr-record': recordLevelProportion,

        # DECEASED
        'forename(s) of deceased': split, 'surname of deceased': split,
        'marital status': split, 'sex': split, 'name of spouse(s)': split,
        'day': split / 3.0, 'month': split / 3.0, 'year': split / 3.0, 'age at death': split,
        'cause of death': split,

        # PARENTS
        'father\'s forename': split, 'father\'s surname': split, 'if father deceased': split,
        'mother\'s forename': split, 'mother\'s maiden surname': split, 'if mother deceased': split,

        # REGISTRATION
        'day of reg': split / 3.0, 'month of reg': split / 3.0, 'year of reg': split / 3.0,

        # OTHER POPULATED FIELDS
        'death date': 0.0, 'agey': 0.0, 'notes1': 0.0,

        # UNPOPULATED FIELDS
        'spouse\'s occ': 0.0, 'occupation': 0.0,
        'father\'s occupation': 0.0, 'mother\'s occupation': 0.0,
        'address 1': 0.0, 'address 2': 0.0,

        'IOSidentifier': 0.0, 'corrected': 0.0, 'source': 0.0, 'input1': 0.0, 'identifier': 0.0,
        'IOS_Rdindentifier': 0.0, 'IOS_RSDindentifier': 0.0, 'register identifier': 0.0,
        'IOS_Regisdentifier': 0.0, 'entry number': 0.0, 'IOS_yearofregistration': 0.0, 'ssdec': 0.0,
        'sxdec': 0.0, 'ssfather': 0.0, 'sxfather': 0.0, 'ssmother': 0.0, 'sxmother': 0.0,
        'spousesn': 0.0, 'spousexn': 0.0, 'infxn': 0.0, 'infsn': 0.0, 'length of last illness': 0.0,
        'medically certified': 0.0, 'doctor\'s name': 0.0, 'forename of informant': 0.0,
        'surname of informant': 0.0, 'relationship of informant to deceased': 0.0,
        'did inform sign?': 0.0, 'was inform pres?': 0.0, 'notes2': 0.0, 'notes3': 0.0,
        'repeats': 0.0, 'edits': 0.0, 'earlypid': 0.0, 'earlysch': 0.0

    }

    selectedCorruptors = {

        'crptr-record': [(0.0, corruptor.blankRecord),
                         (0.2, corruptor.dayMonthSwapDeath),
                         (0.2, corruptor.dayMonthSwapRegistration),
                         (0.2, corruptor.deceasedNameSwap),
                         (0.2, corruptor.fatherNameSwap),
                         (0.2, corruptor.motherNameSwap)],

        'forename(s) of deceased': corruptor.forenameCorruptionGrouping,

        'surname of deceased': corruptor.surnameCorruptionGrouping,

        'marital status': [(0.5, corruptor.marritalStatus),
                           (0.35, corruptor.missingValue),
                           (0.1, corruptor.unknownCharacter),
                           (0.05, corruptor.keyboardShift)],

        'sex': [(0.8, corruptor.sexFlip),
                (0.05, corruptor.missingValue),
                (0.1, corruptor.unknownCharacter),
                (0.05, corruptor.keyboardShift)],

        'name of spouse(s)': [(0.2, corruptor.generalCharacter),
                              (0.1, corruptor.keyboardShift),
                              (0.1, corruptor.unknownCharacter),
                              (0.25, corruptor.missingValue),
                              (0.35, corruptor.phoneticVariation)],

        'day': corruptor.splitDateCorruptionGrouping,
        'month': corruptor.splitDateCorruptionGrouping,
        'year': corruptor.splitDateCorruptionGrouping,

        'age at death': [(0.3, corruptor.keyboardShift),
                         (0.3, corruptor.unknownCharacter),
                         (0.4, corruptor.missingValue)],

        'father\'s forename': corruptor.forenameCorruptionGrouping,
        'father\'s surname': corruptor.surnameCorruptionGrouping,
        'if father deceased': corruptor.deceasedCorruptionGrouping,

        'mother\'s forename': corruptor.forenameCorruptionGrouping,
        'mother\'s maiden surname': corruptor.surnameCorruptionGrouping,
        'if mother deceased': corruptor.deceasedCorruptionGrouping,

        'cause of death': [(0.2, corruptor.generalCharacter),
                           (0.1, corruptor.keyboardShift),
                           (0.1, corruptor.unknownCharacter),
                           (0.25, corruptor.missingValue)],

        'day of reg': corruptor.splitDateCorruptionGrouping,
        'month of reg': corruptor.splitDateCorruptionGrouping,
        'year of reg': corruptor.splitDateCorruptionGrouping

    }

    numberOfRecords = len(records)
    numberToModify = int(numberOfRecords * proportionOfRecordsToCorrupt)
    print "Records to be corrupted: " + str(numberToModify)

    crptrInstance = crptr.CorruptDataSet(number_of_org_records=numberOfRecords,
                                         number_of_mod_records=numberToModify,
                                         attribute_name_list=labels[1:],
                                         max_num_dup_per_rec=1,
                                         num_dup_dist='uniform',
                                         max_num_mod_per_attr=maxModificationsPerAttribute,
                                         num_mod_per_rec=numberOfModificationsPerRecord,
                                         attr_mod_prob_dict=columnProbabilities,
                                         attr_mod_data_dict=selectedCorruptors
                                         )

    records = crptrInstance.corrupt_records(records)
    # end of data corruption

    # Output corrupted data to temp file before cleanup
    Utils.outputDictToCSV(labels, records, tempFile)

    # remove original versions for corrupter records
    Utils.removeOrigonalRecordsForWhichDuplicateExists(tempFile, tempFile)

    # remove crptr ids
    Utils.removeCryptIDs(tempFile, outputFile)

    # clean up temp file
    os.remove(tempFile)

    sys.stdout = so
    logOutput.close()
