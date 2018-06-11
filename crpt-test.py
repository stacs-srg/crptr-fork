# Code adapted by: Tom Dalton - tsd4@st-andrews.ac.uk
# Forked from: Ahmad Alsediqi
# Based on code by:  Peter Christen and Dinusha Vatsalan, January-March 2012
#
# generate-data-english.py - Python module to generate synthetic data based on
#                            English look-up and error tables.
#
# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

# Import the necessary other modules of the data generator
#
import random

import basefunctions  # Helper functions
import corruptrecord # Main classes to corrupt whole records
import corruptvalue # Main classes to corrupt attribute values of records
import crptr
import positionfunctions
from EG_SKYE_Corruptor import Utils

# read in source file

inputFile = "input-files/birth-30.csv"
outputFile = "output-files/birth-30-out.csv"
tempFile = "temp.csv"

# handle commas
Utils.removeCommas(inputFile, tempFile)

# add crptr ids
Utils.addCryptIDs(tempFile, tempFile)

# read in source file
rec_dict = Utils.readInFile(tempFile)

random.seed(42)

# Valid encoding strings are listed here:
# http://docs.python.org/library/codecs.html#standard-encodings
unicode_encoding_used = 'utf_8'

# The name of the record identifier attribute (unique value for each record).
rec_id_attr_name = 'rec-id' # TD: change this to whatever our ID field is called
header_list = [rec_id_attr_name]+rec_dict[rec_id_attr_name]
del rec_dict["rec-id"] # TD: and this too


# separate CSV output file
output_file_name = 'output-files/birth-30-out.csv'

# Set how many original and how many duplicate records are to be generated.
num_org_rec = len(rec_dict)
num_dup_rec = int(num_org_rec * 0.1)

# Set the maximum number of duplicate records can be generated per original
# record.
#
max_duplicate_per_record = 1

# Set the probability distribution used to create the duplicate records for one
# original record (possible values are: 'uniform', 'poisson', 'zipf').
#
num_duplicates_distribution = 'poisson'

# Set the maximum number of modification that can be applied to a single
# attribute (field).
#
max_modification_per_attr = 1

# Set the number of modification that are to be applied to a record.
#
num_modification_per_record = 1

# Check if the given the unicode encoding selected is valid.
#
basefunctions.check_unicode_encoding_exists(unicode_encoding_used)


# -----------------------------------------------------------------------------
# Define the attributes to be generated for this data set, and the data set
# itself.
#
attr_name_list = ['crptr-record',
                  'FirstName', 'LastName','Gender','DateofBirth',
                  'FatherFirstName','FatherLastName', 'FatherOccupation',
                  'MotherFirstName', 'MotherLastName', 'MotherOccupation']

# -----------------------------------------------------------------------------
# Define how the generated records are to be corrupted (using methods from
# the corruptor.py module).

# For a value edit corruptor, the sum or the four probabilities given must
# be 1.0.
#
edit_corruptor = corruptvalue.CorruptValueEdit(
    position_function = positionfunctions.position_mod_normal,
    char_set_funct = basefunctions.char_set_ascii,
    insert_prob = 0.5,
    delete_prob = 0.5,
    substitute_prob = 0.0,
    transpose_prob = 0.0
)

edit_corruptor2 = corruptvalue.CorruptValueEdit(
    position_function = positionfunctions.position_mod_normal,
    char_set_funct = basefunctions.char_set_ascii,
    insert_prob = 0.25,
    delete_prob = 0.25,
    substitute_prob = 0.25,
    transpose_prob = 0.25
)

surname_misspell_corruptor = corruptvalue.CorruptCategoricalValue(
    lookup_file_name = 'lookup-files/surname-misspell.csv',
    has_header_line = False,
    unicode_encoding = unicode_encoding_used
)

ocr_corruptor = corruptvalue.CorruptValueOCR(
    position_function = positionfunctions.position_mod_normal,
    lookup_file_name = 'lookup-files/ocr-variations.csv',
    has_header_line = False,
    unicode_encoding = unicode_encoding_used
)

keyboard_corruptor = corruptvalue.CorruptValueKeyboard(
    position_function = positionfunctions.position_mod_normal,
    row_prob = 0.5,
    col_prob = 0.5
)

phonetic_corruptor = corruptvalue.CorruptValuePhonetic(
    lookup_file_name = 'lookup-files/phonetic-variations.csv',
    has_header_line = False,
    unicode_encoding = unicode_encoding_used
)

missing_val_corruptor = corruptvalue.CorruptMissingValue()

missing_val_corruptor_missing = corruptvalue.CorruptMissingValue(
    missing_val='missing'
)

given_name_missing_val_corruptor = corruptvalue.CorruptMissingValue(
    missing_value='unknown'
)

# =====================================================================
# Attribute level
# =====================================================================
given_name_unknown_char = corruptvalue.CorruptUnknownCharacter(
    position_function=positionfunctions.position_mod_uniform,
    unknown_char="?"
)

last_name_abbr = corruptvalue.CorruptAbbreviatedNameForms(
    num_of_char = 1
)

gender_categorical_domain = corruptvalue.CorruptCategoricalDomain(
    categories_list = ["M", "F"]
)

date = corruptvalue.CorruptDate(
    date_order = "dd-mm-yyyy",
    separator = "-",
    components_to_modify = ['day', 'month', 'year'],
    date_corruption_methods = ['add', 'decline', 'swap_digit','swap_comp', 'random', 'first','full_month','abbr_month']
)

# =====================================================================
# Record level
# =====================================================================
clear_rec = corruptrecord.CorruptClearRecord(
    clear_val=' '
)

swap_attr = corruptrecord.CorruptSwapAttributes(
    attr1='FirstName',
    attr2= 'LastName',
    attr_name_list=attr_name_list
)

over_attr = corruptrecord.CorruptOverflowAttributes(
    attr1='FirstName',
    attr2= 'LastName',
    overflow_level = 0.5,
    start_pos = 'beginning',
    attr_name_list=attr_name_list
)

missing_rec = corruptrecord.CorruptMissingRecord()

duplicate_rec = corruptrecord.CorruptDuplicateRecord()



# Define the probability distribution of how likely an attribute will be
# selected for a modification.
# Each of the given probability values must be between 0 and 1, and the sum of
# them must be 1.0.
# If a probability is set to 0 for a certain attribute, then no modification
# will be applied on this attribute.
#

attr_mod_prob_dictionary = {'crptr-record':0.0,
                            'FirstName': 0.0, 'LastName':0.0, 'Gender': 0.0,'DateofBirth': 0.0,
                            'FatherFirstName': 0.0,'FatherLastName': 0.0, 'FatherOccupation': 0.0,
                            'MotherFirstName': 0.0, 'MotherLastName': 0.0, 'MotherOccupation':1.0}


# Define the actual corruption (modification) methods that will be applied on
# the different attributes.
# For each attribute, the sum of probabilities given must sum to 1.0.
#
attr_mod_data_dictionary = {'LastName':[(0.2, edit_corruptor2),
                                        (0.4, given_name_unknown_char),
                                        (0.4, last_name_abbr),
                                        (0.0, phonetic_corruptor),
                                        (0.0, keyboard_corruptor)],
                            'FirstName':[(0.0, edit_corruptor2),
                                         (0.0, given_name_unknown_char),
                                         (0.0, last_name_abbr),
                                         (1.0, phonetic_corruptor),
                                         (0.0, keyboard_corruptor)],
                            'Gender':[(1.0, gender_categorical_domain)],
                            'DateofBirth':[(1.0, date)],
                            'MotherOccupation':[(1.0, edit_corruptor)],
                            'crptr-record':[(0.0,swap_attr),
                                            (0.0,over_attr),
                                            (0.0,clear_rec),
                                            (1.0,missing_rec),
                                            (0.0,duplicate_rec)]

                            }

# Nothing to change here - set-up the data set corruption object
#
test_data_corruptor = crptr.CorruptDataSet(number_of_org_records = num_org_rec,
                                           number_of_mod_records = num_dup_rec,
                                           attribute_name_list = attr_name_list,
                                           max_num_dup_per_rec = max_duplicate_per_record,
                                           num_dup_dist = num_duplicates_distribution,
                                           max_num_mod_per_attr = max_modification_per_attr,
                                           num_mod_per_rec = num_modification_per_record,
                                           attr_mod_prob_dict = attr_mod_prob_dictionary,
                                           attr_mod_data_dict = attr_mod_data_dictionary
                                           )

# =============================================================================
# No need to change anything below here

# Start the data generation process
#

assert len(rec_dict) == num_org_rec  # Check the number of generated records

# Corrupt (modify) the original records into duplicate records
#


rec_dict = test_data_corruptor.corrupt_records(rec_dict)
print rec_dict
for i in rec_dict.iteritems():
    print i
print len(rec_dict)
assert len(rec_dict) == num_org_rec+num_dup_rec # Check total number of records

# Inject any CSV Here (rec_dict is the dataset handler)
# Records must have the same IDs format [rec-000-org]

rec_id_list = rec_dict.keys()
rec_id_list.sort()

# Convert record dictionary into a list, with record identifier added
#
rec_list = []

for rec_id in rec_id_list:
    this_rec_list = [rec_id]+rec_dict[rec_id]
    rec_list.append(this_rec_list)
    #print this_rec_list

# header_list = [rec_id_attr_name]+rec_dict[rec_id_attr_name]
print header_list
basefunctions.write_csv_file(output_file_name, unicode_encoding_used, header_list, rec_list)

# Write generate data into a file
#
#test_data_corruptor.write()

# End.
# =============================================================================
