
import random

from crptr import base_functions
from crptr.corrupt_values.base import CorruptValue


class CorruptValueKeyboard(CorruptValue):
  """Use a keyboard layout to simulate typing errors. They keyboard is
     hard-coded into this method, but can be changed easily for different
     keyboard layout.

     A character from the original input string will be randomly chosen using
     the position function, and then a character from either the same row or
     column in the keyboard will be selected.

     The additional arguments (besides the base class argument
     'position_function') that have to be set when this attribute type is
     initialised are:

     row_prob  The probability that a neighbouring character in the same row
               is selected.

     col_prob  The probability that a neighbouring character in the same
               column is selected.

     The sum of row_prob and col_prob must be 1.0.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.row_prob = None
    self.col_prob = None
    self.name =     'Keybord value'

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('row')):
        base_functions.check_is_normalised('row_prob', value)
        self.row_prob = value

      elif (keyword.startswith('col')):
        base_functions.check_is_normalised('col_prob', value)
        self.col_prob = value

      else:
        base_kwargs[keyword] = value

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    base_functions.check_is_normalised('row_prob', self.row_prob)
    base_functions.check_is_normalised('col_prob', self.col_prob)

    if (abs((self.row_prob + self.col_prob) - 1.0) > 0.0000001):
      raise Exception('Sum of row and column probablities does not sum ' + \
                       'to 1.0')

    # Keyboard substitutions gives two dictionaries with the neigbouring keys
    # for all leters both for rows and columns (based on ideas implemented by
    # Mauricio A. Hernandez in his dbgen).
    # This following data structures assume a QWERTY keyboard layout
    #
    self.rows = {'a':'s',  'b':'vn', 'c':'xv', 'd':'sf', 'e':'wr', 'f':'dg',
                 'g':'fh', 'h':'gj', 'i':'uo', 'j':'hk', 'k':'jl', 'l':'k',
                 'm':'n',  'n':'bm', 'o':'ip', 'p':'o',  'q':'w',  'r':'et',
                 's':'ad', 't':'ry', 'u':'yi', 'v':'cb', 'w':'qe', 'x':'zc',
                 'y':'tu', 'z':'x',
                 '1':'2',  '2':'13', '3':'24', '4':'35', '5':'46', '6':'57',
                 '7':'68', '8':'79', '9':'80', '0':'9'}

    self.cols = {'a':'qzw', 'b':'gh',  'c':'df', 'd':'erc','e':'ds34',
                 'f':'rvc', 'g':'tbv', 'h':'ybn', 'i':'k89',  'j':'umn',
                 'k':'im', 'l':'o', 'm':'jk',  'n':'hj',  'o':'l90', 'p':'0',
                 'q':'a12', 'r':'f45', 's':'wxz', 't':'g56',  'u':'j78',
                 'v':'fg', 'w':'s23',  'x':'sd', 'y':'h67',  'z':'as',
                 '1':'q',  '2':'qw', '3':'we', '4':'er', '5':'rt',  '6':'ty',
                 '7':'yu', '8':'ui', '9':'io', '0':'op'}

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string by replacing a single
       character with a neighbouring character given the defined keyboard
       layout at a position randomly selected by the position function.
    """

    #in_str = in_str.decode("UTF-8")

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    max_try = 10  # Maximum number of tries to find a keyboard modification at
                  # a randomly selected position

    done_key_mod = False  # A flag, set to true once a modification is done
    try_num =      0

    mod_str = in_str[:]  # Make a copy of the string which will be modified

    while ((done_key_mod == False) and (try_num < max_try)):

      mod_pos =  self.position_function(mod_str)
      mod_char = mod_str[mod_pos]

      r = random.random()  # Create a random number between 0 and 1

      if (r <= self.row_prob):  # See if there is a row modification
        if (mod_char in self.rows):
          key_mod_chars = self.rows[mod_char]
          done_key_mod =  True

      else:  # See if there is a column modification
        if (mod_char in self.cols):
          key_mod_chars = self.cols[mod_char]
          done_key_mod =  True

      if (done_key_mod == False):
        try_num += 1

    # If a modification is possible do it
    #
    if (done_key_mod == True):

      # Randomly select one of the possible characters
      #
      new_char = random.choice(key_mod_chars)

      mod_str = mod_str[:mod_pos] + new_char + mod_str[mod_pos+1:]

    assert len(mod_str) == len(in_str)

    return mod_str