from crptr import base_functions
from crptr.corrupt_records.base import CorruptRecord


class CorruptSwapAttributes(CorruptRecord):
  """A corruptor method which simply sets an attribute value to a missing
     value.

     The additional argument (besides the base class argument
     'position_function') that has to be set when this attribute type is
     initialised are:

     missing_val  The string which designates a missing value. Default value
                  is the empty string ''.

     Note that the 'position_function' is not required by this corruptor
     method.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, attr_name_list, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.attr_name_list = attr_name_list

    self.attr1 = None
    self.attr2 = None
    self.name =        'Swap Attributes'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('attr1')):
        base_functions.check_is_string('attr1', value)
        self.attr1 = value
        if (value not in attr_name_list):
            raise Exception('Value of "%s" is not in dataset attributes. Check dataset correct attributes ' % str(value))


      elif (keyword.startswith('attr2')):
        base_functions.check_is_string('attr2', value)
        self.attr2 = value
        if (value not in attr_name_list):
            raise Exception('Value of "%s" is not in dataset attributes. Check dataset correct attributes ' % str(value))
      else:
        base_kwargs[keyword] = value

    base_kwargs['position_function'] = dummy_position

    CorruptRecord.__init__(self, base_kwargs)  # Process base arguments

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_list):
    """Simply return the missing value string.
    """
    attr1_idx = self.attr_name_list.index(self.attr1)
    attr2_idx = self.attr_name_list.index(self.attr2)
    attr1_val = in_list[attr1_idx]
    attr2_val = in_list[attr2_idx]
    new_list = in_list[:]
    new_list[attr1_idx] = attr2_val
    new_list[attr2_idx] = attr1_val

    return new_list

# =============================================================================
# =============================================================================
#swap_attr = CorruptSwapAttributes(\
#    attr1='FirstName',
#    attr2= 'LastName'
#)

#print swap_attr.__dict__
#print swap_attr.corrupt_value(test_list)
# =============================================================================
