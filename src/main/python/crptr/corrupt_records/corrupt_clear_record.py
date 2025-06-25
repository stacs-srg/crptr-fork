from crptr import base_functions
from crptr.corrupt_records.base import CorruptRecord


class CorruptClearRecord(CorruptRecord):
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

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.clear_val = ' '
    self.name =        'Clear record'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('clear')):
        base_functions.check_is_string('clear_val', value)
        self.clear_val = value

      else:
        base_kwargs[keyword] = value

    base_kwargs['position_function'] = dummy_position

    CorruptRecord.__init__(self, base_kwargs)  # Process base arguments

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_list):
    """Simply return the missing value string.
    """
    new_list = in_list[:]
    for idx in range (len(new_list)):
        new_list[idx] = self.clear_val
    return new_list

# =============================================================================
#clear_rec = CorruptClearRecord(\
#       clear_val=' ')

#print clear_rec.__dict__
#print clear_rec.corrupt_value(test_list)
# =============================================================================
