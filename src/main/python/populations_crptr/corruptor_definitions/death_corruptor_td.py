from crptr.corrupt_records.corrupt_swap_attributes import CorruptSwapAttributes
from crptr.synthetic_populations.corruptor_definitions.base import Corruptor


class DeathCorruptorTD(Corruptor):

    def __init__(self, labels, lookupFilesDir, encoding = 'UTF-8'):
        self.columnLabels = labels
        Corruptor.__init__(self, lookupFilesDir, encoding)


    def setup(self):

        Corruptor.setup(self)

        # =====================================================================
        # Attribute level
        # =====================================================================


        # =====================================================================
        # Record level
        # =====================================================================
        self.dayMonthSwapDeath = CorruptSwapAttributes(
            attr1='day',
            attr2='month',
            attr_name_list=self.columnLabels
        )

        self.deceasedNameSwap = CorruptSwapAttributes(
            attr1='forename(s) of deceased',
            attr2='surname of deceased',
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