from crptr.corrupt_records.base import CorruptRecord


class CorruptDuplicateRecord(CorruptRecord):
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

    self.name =        'Missing record'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):
        base_kwargs[keyword] = value

    base_kwargs['position_function'] = dummy_position

    CorruptRecord.__init__(self, base_kwargs)  # Process base arguments

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_list):
    """Simply return the missing value string.
    """
    new_list = in_list[:]
    new_list[0]=('duplicate')
    return new_list

# =============================================================================