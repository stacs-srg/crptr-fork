from crptr.corrupt_values.base import CorruptValue
from crptr import base_functions


class CorruptAbbreviatedNameForms(CorruptValue):

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.num_of_char =  None
    self.name =            'Abbreviated Name Forms'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('num')):
        base_functions.check_is_integer('num_of_char', value)
        self.num_of_char = value
      else:
        base_kwargs[keyword] = value
    base_kwargs['position_function'] = dummy_position
    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    base_functions.check_is_integer('num_of_char',
                                              self.num_of_char)
  def corrupt_value(self, in_str):
    """Method which corrupts the given input string and returns the modified
       string by randomly selecting an edit operation and position in the
       string where to apply this edit.
    """

    if (len(in_str) == 0) or (len(in_str) < self.num_of_char):  # Empty string, no modification possible
      return in_str
    new_str = in_str[:self.num_of_char]
    return new_str