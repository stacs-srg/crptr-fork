import random

from crptr import base_functions
from crptr.corrupt_values.base import CorruptValue


class CorruptValueOCR(CorruptValue):
  """Simulate OCR errors using a list of similar pairs of characters or strings
     that will be applied on the original string values.

     These pairs of characters will be loaded from a look-up file which is a
     CSV file with two columns, the first is a single character or character
     sequence, and the second column is also a single character or character
     sequence. It is assumed that the second value is an OCR modification of
     the first value, and the other way round. For example:

       5,S
       5,s
       2,Z
       2,z
       1,|
       6,G

     It is possible for an 'original' string value (first column) to have
     several variations (second column). In such a case one variation will be
     randomly selected during the value corruption (modification) process.

     The additional arguments (besides the base class argument
     'position_function') that have to be set when this attribute type is
     initialised are:

     lookup_file_name  Name of the file which contains the OCR character
                       variations.

     has_header_line   A flag, set to True or False, that has to be set
                       according to if the look-up file starts with a header
                       line or not.

     unicode_encoding  The Unicode encoding (a string name) of the file.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.lookup_file_name = None
    self.has_header_line =  None
    self.unicode_encoding = None
    self.ocr_val_dict =     {}  # The dictionary to hold the OCR variations
    self.name =             'OCR value'

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

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    base_functions.check_is_non_empty_string('lookup_file_name',
                                            self.lookup_file_name)
    base_functions.check_is_flag('has_header_line', self.has_header_line)
    base_functions.check_is_non_empty_string('unicode_encoding',
                                            self.unicode_encoding)

    # Load the OCR variations lookup file - - - - - - - - - - - - - - - - - - -
    #
    header_list, lookup_file_data = \
                     base_functions.read_csv_file(self.lookup_file_name,
                                                 self.unicode_encoding,
                                                 self.has_header_line)

    # Process values from file and their frequencies
    #
    for rec_list in lookup_file_data:
      if (len(rec_list) != 2):
        raise Exception('Illegal format in OCR variations lookup file ' + \
                         '%s: %s' % (self.lookup_file_name, str(rec_list)))
      org_val = rec_list[0].strip()
      var_val = rec_list[1].strip()

      if (org_val == ''):
        raise Exception('Empty original OCR value in lookup file %s' % \
                         (self.lookup_file_name))
      if (var_val == ''):
        raise Exception('Empty OCR variation value in lookup file %s' % \
                         (self.lookup_file_name))
      if (org_val == var_val):
        raise Exception('OCR variation is the same as original value in ' + \
                         'lookup file %s' % (self.lookup_file_name))

      # Now insert the OCR original value and variation twice (with original
      # and variation both as key and value), i.e. swapped
      #
      this_org_val_list = self.ocr_val_dict.get(org_val, [])
      this_org_val_list.append(var_val)
      self.ocr_val_dict[org_val] = this_org_val_list

      this_org_val_list = self.ocr_val_dict.get(var_val, [])
      this_org_val_list.append(org_val)
      self.ocr_val_dict[var_val] = this_org_val_list

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string by replacing a single
       character or a sequence of characters with an OCR variation at a
       position randomly selected by the position function.

       If there are several OCR variations then one will be randomly chosen.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    max_try = 10  # Maximum number of tries to find an OCR modification at a
                  # randomly selected position

    done_ocr_mod = False  # A flag, set to True once a modification is done
    try_num =      0

    mod_str = in_str[:]  # Make a copy of the string which will be modified

    while ((done_ocr_mod == False) and (try_num < max_try)):

      mod_pos = self.position_function(mod_str)

      # Try one to three characters at selected position
      #
      ocr_org_char_set = set([mod_str[mod_pos], mod_str[mod_pos:mod_pos+2], \
                              mod_str[mod_pos:mod_pos+3]])

      mod_options = []  # List of possible modifications that can be applied

      for ocr_org_char in ocr_org_char_set:
        if ocr_org_char in self.ocr_val_dict:
          ocr_var_list = self.ocr_val_dict[ocr_org_char]
          for mod_val in ocr_var_list:
            mod_options.append([ocr_org_char,len(ocr_org_char),mod_val])

      if (mod_options != []):  # Modifications are possible

        # Randomly select one of the possible modifications that can be applied
        #
        mod_to_apply = random.choice(mod_options)
        assert mod_to_apply[0] in list(self.ocr_val_dict.keys())
        assert mod_to_apply[2] in list(self.ocr_val_dict.keys())

        mod_str = in_str[:mod_pos] + mod_to_apply[2] + \
                  in_str[mod_pos+mod_to_apply[1]:]

        done_ocr_mod = True

      else:
        try_num += 1

    return mod_str