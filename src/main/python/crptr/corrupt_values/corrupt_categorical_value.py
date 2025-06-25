import random

from crptr import base_functions
from crptr.corrupt_values.base import CorruptValue


class CorruptCategoricalValue(CorruptValue):
  """Replace a categorical value with another categorical value from the same
     look-up file.

     This corruptor can be used to modify attribute values with known
     misspellings.

     The look-up file is a CSV file with two columns, the first is a
     categorical value that is expected to be in an attribute in an original
     record, and the second is a variation of this categorical value.

     It is possible for an 'original' categorical value (first column) to have
     several misspelling variations (second column). In such a case one
     misspelling will be randomly selected.

     The additional arguments (besides the base class argument
     'position_function') that have to be set when this attribute type is
     initialised are:

     lookup_file_name  Name of the file which contains the categorical values
                       and their misspellings.

     has_header_line   A flag, set to True or False, that has to be set
                       according to if the look-up file starts with a header
                       line or not.

     unicode_encoding  The Unicode encoding (a string name) of the file.

     Note that the 'position_function' is not required by this corruptor
     method.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.lookup_file_name = None
    self.has_header_line =  None
    self.unicode_encoding = None
    self.misspell_dict =    {}  # The dictionary to hold the misspellings
    self.name =             'Categorial value'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('look')):
        base_functions.check_is_non_empty_string('lookup_file_name', value)
        self.lookup_file_name = value

      elif (keyword.startswith('has')):
        base_functions.check_is_flag('has_header_line', value)
        self.has_header_line = value

      elif (keyword.startswith('unicode')):
        base_functions.check_is_non_empty_string('unicode_encoding', value)
        self.unicode_encoding = value

      else:
        base_kwargs[keyword] = value

    base_kwargs['position_function'] = dummy_position

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    base_functions.check_is_non_empty_string('lookup_file_name',
                                            self.lookup_file_name)
    base_functions.check_is_flag('has_header_line', self.has_header_line)
    base_functions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    # Load the misspelling lookup file - - - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data = \
                     base_functions.read_csv_file(self.lookup_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    # Process values from file and misspellings
    #
    for rec_list in lookup_file_data:
      if (len(rec_list) != 2):
        raise Exception('Illegal format in misspellings lookup file %s: %s' \
                         % (self.lookup_file_name, str(rec_list)))

      org_val =  rec_list[0].strip()
      if (org_val == ''):
        raise Exception('Empty original attribute value in lookup file %s' % \
                         (self.lookup_file_name))
      misspell_val = rec_list[1].strip()
      if (misspell_val == ''):
        raise Exception('Empty misspelled attribute value in lookup ' + \
                         'file %s' % (self.lookup_file_name))
      if (org_val == misspell_val):
        raise Exception('Misspelled value is the same as original value' + \
                         ' in lookup file %s' % (self.lookup_file_name))

      this_org_val_list = self.misspell_dict.get(org_val, [])
      this_org_val_list.append(misspell_val)
      self.misspell_dict[org_val] = this_org_val_list

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string and replaces it with a
       misspelling, if there is a known misspelling for the given original
       value.

       If there are several known misspellings for the given original value
       then one will be randomly selected.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    if (in_str not in self.misspell_dict):  # No misspelling for this value
      return in_str

    misspell_list = self.misspell_dict[in_str]

    return random.choice(misspell_list)