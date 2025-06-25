from crptr.corrupt_records.corrupt_swap_attributes import CorruptSwapAttributes
from populations_crptr.corruptor_definitions.base import Corruptor

class BirthCorruptorTD(Corruptor):

    def __init__(self, labels, lookupFilesDir, encoding = 'UTF-8'):
        self.columnLabels = labels
        Corruptor.__init__(self, lookupFilesDir, encoding)

    def setup(self):

        Corruptor.setup(self)

        # =====================================================================
        # Record level
        # =====================================================================
        self.dayMonthSwapMarriage = CorruptSwapAttributes(
            attr1='day of parents\' marriage',
            attr2='month of parents\' marriage',
            attr_name_list=self.columnLabels
        )

        self.childNameSwap = CorruptSwapAttributes(
            attr1='child\'s forname(s)',
            attr2='child\'s surname',
            attr_name_list=self.columnLabels
        )

        self.fatherNameSwap = CorruptSwapAttributes(
            attr1='father\'s forename',
            attr2='father\'s surname',
            attr_name_list=self.columnLabels
        )

        self.motherNameSwap = CorruptSwapAttributes(
            attr1='mother\'s forename',
            attr2='mother\'s maiden surname',
            attr_name_list=self.columnLabels
        )