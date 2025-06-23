from crptr.corrupt_records.corrupt_clear_record import CorruptClearRecord
import crptr.corrupt_value as corrupt_value  # Main classes to corrupt attribute values of records
import crptr.base_functions as base_functions  # Helper functions
import crptr.position_functions as position_functions


class Corruptor:
    def __init__(self, lookupFilesDir, encoding = 'UTF-8'):
        self.encoding = encoding
        self.lookupFilesDir = lookupFilesDir
        self.setup()

    def setup(self):
        # =====================================================================
        # Character level
        # =====================================================================
        self.generalCharacter = corrupt_value.CorruptValueEdit(
            position_function = position_functions.position_mod_normal,
            char_set_funct = base_functions.char_set_ascii,
            insert_prob = 0.2,
            delete_prob = 0.2,
            substitute_prob = 0.5,
            transpose_prob = 0.1
        )

        self.marritalStatus = corrupt_value.CorruptCategoricalDomain(
            categories_list=["R", "M", "W", "D", "B", "S"]
        )

        self.surnameMisspell = corrupt_value.CorruptCategoricalValue(
            lookup_file_name = self.lookupFilesDir + '/surname-misspell.csv',
            has_header_line = False,
            unicode_encoding = self.encoding
        )

        self.keyboardShift = corrupt_value.CorruptValueKeyboard(
            position_function = position_functions.position_mod_normal,
            row_prob = 0.4,
            col_prob = 0.6
        )

        self.unknownCharacter = corrupt_value.CorruptUnknownCharacter(
            position_function=position_functions.position_mod_uniform,
            unknown_char="?"
        )

        self.deceasedFlip = corrupt_value.CorruptCategoricalDomain(
            categories_list=["D", ""]
        )

        self.ocr = corrupt_value.CorruptValueOCR(
            lookup_file_name = self.lookupFilesDir + '/ocr-variations.csv',
            has_header_line=False,
            unicode_encoding=self.encoding,
            position_function=position_functions.position_mod_uniform
        )

        # =====================================================================
        # Attribute level
        # =====================================================================


        self.abbreviateToInitial = corrupt_value.CorruptAbbreviatedNameForms(
            num_of_char = 1
        )

        self.sexFlip = corrupt_value.CorruptCategoricalDomain(
            categories_list = ["m", "f"]
        )

        self.missingValue = corrupt_value.CorruptMissingValue(
            missing_val='missing'
        )

        self.dateDDMMYYYY = corrupt_value.CorruptDate(
            date_order = "yyyy-mm-dd",
            separator = "-",
            components_to_modify = ['day', 'month', 'year'],
            date_corruption_methods = ['add', 'decline', 'swap_digit','swap_comp', 'random', 'first','full_month','abbr_month']
        )

        self.phoneticVariation = corrupt_value.CorruptValuePhonetic(
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
