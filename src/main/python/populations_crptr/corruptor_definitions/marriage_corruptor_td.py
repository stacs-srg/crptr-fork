from crptr.corrupt_records.corrupt_swap_attributes import CorruptSwapAttributes
from crptr.synthetic_populations.corruptor_definitions.base import Corruptor


class MarriageCorruptorTD(Corruptor):

    def __init__(self, labels, lookupFilesDir, encoding = 'UTF-8'):
        self.columnLabels = labels
        Corruptor.__init__(self, lookupFilesDir, encoding)


    def setup(self):

        Corruptor.setup(self)

        self.dayMonthSwapDeath = CorruptSwapAttributes(
            attr1='day',
            attr2='month',
            attr_name_list=self.columnLabels
        )

        self.groomNameSwap = CorruptSwapAttributes(
            attr1='forename of groom',
            attr2='surname of groom',
            attr_name_list=self.columnLabels
        )

        self.brideNameSwap = CorruptSwapAttributes(
            attr1='forename of bride',
            attr2='surname of bride',
            attr_name_list=self.columnLabels
        )

        self.groomFatherNameSwap = CorruptSwapAttributes(
            attr1='groom\'s father\'s forename',
            attr2='groom\'s father\'s surname',
            attr_name_list=self.columnLabels
        )

        self.groomMotherNameSwap = CorruptSwapAttributes(
            attr1='groom\'s mother\'s forename',
            attr2='groom\'s mother\'s maiden surname',
            attr_name_list=self.columnLabels
        )

        self.brideFatherNameSwap = CorruptSwapAttributes(
            attr1='bride\'s father\'s forename',
            attr2='bride\'s father\'s surname',
            attr_name_list=self.columnLabels
        )

        self.brideMotherNameSwap = CorruptSwapAttributes(
            attr1='bride\'s mother\'s forename',
            attr2='bride\'s mother\'s maiden surname',
            attr_name_list=self.columnLabels
        )

