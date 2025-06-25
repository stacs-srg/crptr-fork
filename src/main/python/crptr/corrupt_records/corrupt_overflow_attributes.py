from crptr import base_functions
from crptr.corrupt_records.base import CorruptRecord


class CorruptOverflowAttributes(CorruptRecord):
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
    self.overflow_level = None
    self.start_pos = None
    self.name =        'Overflow Attributes'

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
            raise Exception('Value of "%s" is not in dataset attributes. Check dataset correct attributes : %s' % str(value))

      elif (keyword.startswith('attr2')):
        base_functions.check_is_string('attr2', value)
        self.attr2 = value
        if (value not in attr_name_list):
            raise Exception('Value of "%s" is not in dataset attributes. Check dataset correct attributes : %s' % str(value))

      elif (keyword.startswith('overflow')):
        base_functions.check_is_normalised('overflow_level', value)
        self.overflow_level = value

      elif (keyword.startswith('start')):
        base_functions.check_start_position_of_overflow('start_pos', value)
        self.start_pos = value

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
    if self.start_pos == 'beginning':
        overflow_len = len(attr2_val) * self.overflow_level
        overflow_len = int(overflow_len)
        print(overflow_len)
        new_attr1_val = attr1_val + attr2_val[:overflow_len]
        print(new_attr1_val)
        new_attr2_val = attr2_val[overflow_len:]
        print(new_attr2_val)
        new_list[attr1_idx] = new_attr1_val
        new_list[attr2_idx] = new_attr2_val

    elif self.start_pos == 'ending':
        overflow_len = len(attr1_val) * self.overflow_level
        overflow_len = int(overflow_len)
        print(overflow_len)
        new_attr2_val = attr1_val[overflow_len:] + attr2_val
        print(new_attr2_val)
        new_attr1_val = attr1_val[:overflow_len]
        print(new_attr1_val)
        new_list[attr1_idx] = new_attr1_val
        new_list[attr2_idx] = new_attr2_val

    return new_list

# =============================================================================
# =============================================================================
'''
over_attr = CorruptOverflowAttributes(\
    attr1='FirstName',
    attr2= 'LastName',
    overflow_level = 0.5,
    start_pos = 'beginning'
)

print over_attr.__dict__
print over_attr.corrupt_value(test_list)
# =============================================================================
'''
