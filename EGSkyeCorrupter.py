#!/usr/bin/python
# Author: Tom Dalton (tsd4@st-andrews.ac.uk)
# 5/6/2018
#
# This script reads in files in the format provided by Eilidh Garrett for the Skye data
# ValiPop outputs population records in this form when config includes: output_record_format = EG_SKYE
# This script performs corruption based on a provided config file
# This script then outputs the corrupted records to new files ready to be used with linkage-java

inputFile = "/Users/tsd4/OneDrive/cs/PhD/code/population-model/src/main/resources/valipop/results/batch39-job36-sc500k/20180604-121800:537/records/birth_records.csv"
outputFile = "/Users/tsd4/OneDrive/cs/PhD/code/population-model/src/main/resources/valipop/results/batch39-job36-sc500k/20180604-121800:537/records/birth_10k_corrupted.csv"
deterministic = True
seed = 12345
proportionOfRecordsToModify = 0.1
maxModificationsPerAttribute = 2
numberOfModificationsPerRecord = 4

import Utils
import os
import EGCorruptorDefinitions
import crptr



tempFile = "temp.csv"

# handle commas
Utils.removeCommas(inputFile, tempFile)

# add crptr ids
Utils.addCryptIDs(tempFile, tempFile)

# read in source file
records = Utils.readInFile(tempFile)

labels = Utils.extractLabels(records)

corrupt = EGCorruptorDefinitions.Corruptors(labels)

Utils.setDeterminism(deterministic, seed)

# data corruption

recordLevelProportion = 0.25
attributeLevelProportion = 1 - recordLevelProportion
numberOfCorruptibleAttributes = 11
split = attributeLevelProportion / float(numberOfCorruptibleAttributes)

columnProbabilities = {'ID':0.0, 'family':0.0, 'marriage':0.0, 'Death':0.0, # GROUND TRUTH - DO NOT CORRUPT - ALL VALUES 0
                     'crptr-record': recordLevelProportion,
                     'child\'s forname(s)': split, 'child\'s surname': split, 'birth date': split, 'sex': split, # CHILD
                     'father\'s forename': split, 'father\'s surname': split, # FATHER
                     'mother\'s forename': split, 'mother\'s maiden surname':  split, # MOTHER
                     'day of parents\' marriage':  split/3.0,'month of parents\' marriage': split/3.0,'year of parents\' marriage': split/3.0, # MARRIAGE
                     'day of reg': split/3.0,'month of reg': split/3.0,'year of reg': split/3.0, 'illegit': split, # REGISTRATION

                     'notes1':0.0, 'marriageBaby':0.0, # OTHER POPULATED FIELDS

                     # UNPOPULATED FIELDS
                     'mother\'s occupation':0.0,
                     'father\'s occupation':0.0,
                     'address 1':0.0,'address 2':0.0,
                     'IOSBIRTH_Identifier':0.0,'corrected':0.0,'source':0.0,'line no':0.0,'RD Identifier':0.0,'IOS_RDIdentifier':0.0,'IOS_RSDIdentifier':0.0,'register identifier':0.0,'IOS_RegisterNumber':0.0,'IOS_Entry no':0.0,'IOS_RegisterYear':0.0,'sschild':0.0,'sxchild':0.0,'ssfather':0.0,'sxfather':0.0,'ssmother':0.0,'sxmother':0.0,'place of parent\'s marriage 1':0.0,'place of parent\'s marriage 2':0.0,'forename of informant':0.0,'surname of informant':0.0,'relationship of informant to child':0.0,'did inform sign?':0.0,'was inform present?':0.0,'notes2':0.0,'notes3':0.0,'repeats':0.0,'edits':0.0,'latepid':0.0,'latesch':0.0}

selectedCorruptors = {

                        'crptr-record':                [(0.0, corrupt.blankRecord),
                                                        (0.2, corrupt.dayMonthSwapMarriage),
                                                        (0.2, corrupt.dayMonthSwapRegistration),
                                                        (0.2, corrupt.childNameSwap),
                                                        (0.2, corrupt.fatherNameSwap),
                                                        (0.2, corrupt.motherNameSwap)],

                        'child\'s forname(s)':         corrupt.forenameCorruptionGrouping,

                        'child\'s surname':            corrupt.surnameCorruptionGrouping,

                        'birth date':                  [(0.95, corrupt.dateDDMMYYYY),
                                                        (0.05, corrupt.missingValue)],

                        'sex':                         [(0.8, corrupt.sexFlip),
                                                        (0.05, corrupt.missingValue),
                                                        (0.1, corrupt.unknownCharacter),
                                                        (0.05, corrupt.keyboardShift)],

                        'father\'s forename':          corrupt.forenameCorruptionGrouping,
                        'father\'s surname':           corrupt.surnameCorruptionGrouping,

                        'mother\'s forename':          corrupt.forenameCorruptionGrouping,
                        'mother\'s maiden surname':    corrupt.surnameCorruptionGrouping,

                        'day of parents\' marriage':   corrupt.splitDateCorruptionGrouping,
                        'month of parents\' marriage': corrupt.splitDateCorruptionGrouping,
                        'year of parents\' marriage':  corrupt.splitDateCorruptionGrouping,

                        'day of reg':                  corrupt.splitDateCorruptionGrouping,
                        'month of reg':                corrupt.splitDateCorruptionGrouping,
                        'year of reg':                 corrupt.splitDateCorruptionGrouping,

                        'illegit':                     [(1.0, corrupt.missingValue)]

                    }

numberOfRecords = len(records)
numberToModify = int(numberOfRecords * proportionOfRecordsToModify)
print numberToModify

crptrInstance = crptr.CorruptDataSet(number_of_org_records = numberOfRecords,
                                     number_of_mod_records = numberToModify,
                                     attribute_name_list = labels[1:],
                                     max_num_dup_per_rec = 1,
                                     num_dup_dist = 'uniform',
                                     max_num_mod_per_attr = maxModificationsPerAttribute,
                                     num_mod_per_rec = numberOfModificationsPerRecord,
                                     attr_mod_prob_dict = columnProbabilities,
                                     attr_mod_data_dict = selectedCorruptors
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



