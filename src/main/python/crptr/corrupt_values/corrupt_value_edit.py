import random

from crptr import base_functions
from crptr.corrupt_values.base import CorruptValue


class CorruptValueEdit(CorruptValue):
  """A simple corruptor which applies one edit operation on the given value.

     Depending upon the content of the value (letters, digits or mixed), if the
     edit operation is an insert or substitution a character from the same set
     (letters, digits or both) is selected.

     The additional arguments (besides the base class argument
     'position_function') that has to be set when this attribute type is
     initialised are:

     char_set_funct   A function which determines the set of characters that
                      can be inserted or used of substitution
     insert_prob      These for values set the likelihood of which edit
     delete_prob      operation will be selected.
     substitute_prob  All four probability values must be between 0 and 1, and
     transpose_prob   the sum of these four values must be 1.0
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.char_set_funct =  None
    self.insert_prob =     None
    self.delete_prob =     None
    self.substitute_prob = None
    self.transpose_prob =  None
    self.name =            'Edit operation'

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('char')):
        base_functions.check_is_function_or_method('char_set_funct', value)
        self.char_set_funct = value

      elif (keyword.startswith('ins')):
        base_functions.check_is_normalised('insert_prob', value)
        self.insert_prob = value

      elif (keyword.startswith('del')):
        base_functions.check_is_normalised('delete_prob', value)
        self.delete_prob = value

      elif (keyword.startswith('sub')):
        base_functions.check_is_normalised('substitute_prob', value)
        self.substitute_prob = value

      elif (keyword.startswith('tran')):
        base_functions.check_is_normalised('transpose_prob', value)
        self.transpose_prob = value

      else:
        base_kwargs[keyword] = value

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    base_functions.check_is_function_or_method('char_set_funct',
                                              self.char_set_funct)
    base_functions.check_is_normalised('insert_prob',     self.insert_prob)
    base_functions.check_is_normalised('delete_prob',     self.delete_prob)
    base_functions.check_is_normalised('substitute_prob', self.substitute_prob)
    base_functions.check_is_normalised('transpose_prob',  self.transpose_prob)

    # Check if the character set function returns a string
    #
    test_str = self.char_set_funct('test')   # This might become a problem
    base_functions.check_is_string_or_unicode_string('test_str', test_str)

    if (abs((self.insert_prob + self.delete_prob + self.substitute_prob + \
         self.transpose_prob) - 1.0) > 0.0000001):
      raise Exception('The four edit probabilities do not sum to 1.0')

    # Calculate the probability ranges for the four edit operations
    #
    self.insert_range =     [0.0,self.insert_prob]
    self.delete_range =     [self.insert_range[1],
                             self.insert_range[1] + self.delete_prob]
    self.substitute_range = [self.delete_range[1],
                             self.delete_range[1] + self.substitute_prob]
    self.transpose_range =  [self.substitute_range[1],
                             self.substitute_range[1] + self.transpose_prob]
    assert self.transpose_range[1] == 1.0

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string and returns the modified
       string by randomly selecting an edit operation and position in the
       string where to apply this edit.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    # in_str = in_str.decode("UTF-8")

    # Randomly select an edit operation
    #
    r = random.random()

    if (r < self.insert_range[1]):
      edit_op = 'ins'
    elif ((r >= self.delete_range[0]) and (r < self.delete_range[1])):
      edit_op = 'del'
    elif ((r >= self.substitute_range[0]) and (r < self.substitute_range[1])):
      edit_op = 'sub'
    else:
      edit_op = 'tra'

    # Do some checks if only a valid edit operations was selected
    #
    if (edit_op == 'ins'):
      assert self.insert_prob > 0.0
    elif (edit_op == 'del'):
      assert self.delete_prob > 0.0
    elif (edit_op == 'sub'):
      assert self.substitute_prob > 0.0
    else:
      assert self.transpose_prob > 0.0

    # If the input string is empty only insert is possible
    #
    if ((len(in_str) == 0) and (edit_op != 'ins')):
      return in_str  # Return input string without modification

    # If the input string only has one character then transposition is not
    # possible
    #
    if ((len(in_str) == 1) and (edit_op == 'tra')):
      return in_str  # Return input string without modification

    # Position in string where to apply the modification
    #
    # For a transposition we cannot select the last position in the string
    # while for an insert we can specify the position after the last
    if (edit_op == 'tra'):
      len_in_str = in_str[:-1]
    elif (edit_op == 'ins'):
      len_in_str = in_str+'x'
    else:
      len_in_str = in_str
    mod_pos = self.position_function(len_in_str)

    # Get the set of possible characters that can be inserted or substituted
    #
    char_set = self.char_set_funct(in_str)

    if (char_set == ''):  # No possible value change
      return in_str

    if (edit_op == 'ins'):  # Insert a character
      ins_char = random.choice(char_set)
      new_str = in_str[:mod_pos] + ins_char + in_str[mod_pos:]

    elif (edit_op == 'del'):  # Delete a character
      new_str = in_str[:mod_pos] + in_str[mod_pos+1:]

    elif (edit_op == 'sub'):  # Substitute a character
      sub_char = random.choice(char_set)
      new_str = in_str[:mod_pos] + sub_char + in_str[mod_pos+1:]

    else:  # Transpose two characters
      char1 = in_str[mod_pos]
      char2 = in_str[mod_pos+1]
      new_str = in_str[:mod_pos]+char2+char1+in_str[mod_pos+2:]

    return new_str