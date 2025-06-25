from crptr.corrupt_records.corrupt_clear_record import CorruptClearRecord
import crptr.base_functions as base_functions  # Helper functions
import crptr.position_functions as position_functions

from crptr.corrupt_values.corrupt_abbreviated_name_forms import CorruptAbbreviatedNameForms
from crptr.corrupt_values.corrupt_categorical_domain import CorruptCategoricalDomain
from crptr.corrupt_values.corrupt_categorical_value import CorruptCategoricalValue
from crptr.corrupt_values.corrupt_date import CorruptDate
from crptr.corrupt_values.corrupt_missing_value import CorruptMissingValue
from crptr.corrupt_values.corrupt_unknown_character import CorruptUnknownCharacter
from crptr.corrupt_values.corrupt_value_edit import CorruptValueEdit
from crptr.corrupt_values.corrupt_value_keyboard import CorruptValueKeyboard
from crptr.corrupt_values.corrupt_value_ocr import CorruptValueOCR
from crptr.corrupt_values.corrupt_value_phonetic import CorruptValuePhonetic

class Corruptor:
    def __init__(self, lookupFilesDir, encoding = 'UTF-8'):
        self.encoding = encoding
        self.lookupFilesDir = lookupFilesDir
        self.setup()

    def setup(self):
        # =====================================================================
        # Character level
        # =====================================================================
        self.generalCharacter = CorruptValueEdit(
            position_function = position_functions.position_mod_normal,
            char_set_funct = base_functions.char_set_ascii,
            insert_prob = 0.2,
            delete_prob = 0.2,
            substitute_prob = 0.5,
            transpose_prob = 0.1
        )

        self.marritalStatus = CorruptCategoricalDomain(
            categories_list=["R", "M", "W", "D", "B", "S"]
        )

        self.surnameMisspell = CorruptCategoricalValue(
            lookup_file_name = self.lookupFilesDir + '/surname-misspell.csv',
            has_header_line = False,
            unicode_encoding = self.encoding
        )

        self.keyboardShift = CorruptValueKeyboard(
            position_function = position_functions.position_mod_normal,
            row_prob = 0.4,
            col_prob = 0.6
        )

        self.unknownCharacter = CorruptUnknownCharacter(
            position_function=position_functions.position_mod_uniform,
            unknown_char="?"
        )

        self.deceasedFlip = CorruptCategoricalDomain(
            categories_list=["D", ""]
        )

        self.ocr = CorruptValueOCR(
            lookup_file_name = self.lookupFilesDir + '/ocr-variations.csv',
            has_header_line=False,
            unicode_encoding=self.encoding,
            position_function=position_functions.position_mod_uniform
        )

        # =====================================================================
        # Attribute level
        # =====================================================================


        self.abbreviateToInitial = CorruptAbbreviatedNameForms(
            num_of_char = 1
        )

        self.sexFlip = CorruptCategoricalDomain(
            categories_list = ["m", "f"]
        )

        self.missingValue = CorruptMissingValue(
            missing_val='missing'
        )

        self.dateDDMMYYYY = CorruptDate(
            date_order = "yyyy-mm-dd",
            separator = "-",
            components_to_modify = ['day', 'month', 'year'],
            date_corruption_methods = ['add', 'decline', 'swap_digit','swap_comp', 'random', 'first','full_month','abbr_month']
        )

        self.phoneticVariation = CorruptValuePhonetic(
            lookup_file_name = self.lookupFilesDir + '/phonetic-variations.csv',
            has_header_line = False,
            unicode_encoding = self.encoding
        )

        self.forenameCorruptionGrouping = [(0.2, self.generalCharacter),
                                           (0.1, self.keyboardShift),
                                           (0.1, self.unknownCharacter),
                                           (0.2, self.abbreviateToInitial),
                                           (0.05, self.missingValue),
                                           (0.35, self.phoneticVariation)]

        self.forenameCorruptionGroupingOCR = [(0.6, self.ocr),
                                           (0.05, self.missingValue),
                                           (0.35, self.phoneticVariation)]

        self.addressCorruptionGrouping = [(0.3, self.generalCharacter),
                                          (0.4, self.keyboardShift),
                                          (0.2, self.unknownCharacter),
                                          (0.1, self.missingValue)]

        self.addressCorruptionGroupingOCR = [(0.9, self.ocr),
                                          (0.1, self.missingValue)]

        self.occupationCorruptionGrouping = [(0.3, self.generalCharacter),
                                             (0.2, self.keyboardShift),
                                             (0.2, self.unknownCharacter),
                                             (0.3, self.missingValue)]

        self.occupationCorruptionGroupingOCR = [(0.7, self.ocr),
                                             (0.3, self.missingValue)]

        self.surnameCorruptionGrouping = [(0.2, self.generalCharacter),
                                          (0.1, self.keyboardShift),
                                          (0.1, self.unknownCharacter),
                                          (0.2, self.surnameMisspell),
                                          (0.05, self.missingValue),
                                          (0.35, self.phoneticVariation)]

        self.surnameCorruptionGroupingOCR = [(0.4, self.ocr),
                                          (0.2, self.surnameMisspell),
                                          (0.05, self.missingValue),
                                          (0.35, self.phoneticVariation)]

        self.splitDateCorruptionGrouping = [(0.7, self.keyboardShift),
                                       (0.2, self.generalCharacter),
                                       (0.1, self.missingValue)]

        self.splitDateCorruptionGroupingOCR = [(0.9, self.ocr),
                                            (0.1, self.missingValue)]

        self.deceasedCorruptionGrouping = [(0.5, self.deceasedFlip),
                                           (0.2, self.keyboardShift),
                                           (0.05, self.unknownCharacter),
                                           (0.25, self.missingValue)]

        self.deceasedCorruptionGroupingOCR = [(0.5, self.deceasedFlip),
                                           (0.5, self.ocr)]

        # =====================================================================
        # Record level
        # =====================================================================
        self.blankRecord = CorruptClearRecord(
            clear_val=' '
        )
