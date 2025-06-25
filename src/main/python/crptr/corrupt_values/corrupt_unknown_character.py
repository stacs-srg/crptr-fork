from crptr import base_functions
from crptr.corrupt_values.base import CorruptValue


class CorruptUnknownCharacter(CorruptValue):

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.unknown_char =  None
    self.name =            'Unknown Character'

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('unknown')):
        base_functions.check_is_string('unknown_char', value)
        self.unknown_char = value

      else:
        base_kwargs[keyword] = value

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    base_functions.check_is_string('unknown_char',
                                              self.unknown_char)
  def corrupt_value(self, in_str):
    """Method which corrupts the given input string and returns the modified
       string by randomly selecting an edit operation and position in the
       string where to apply this edit.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str
    
    mod_pos = self.position_function(in_str)
    new_str = in_str[:mod_pos] + self.unknown_char + in_str[mod_pos + 1:]
    return new_str