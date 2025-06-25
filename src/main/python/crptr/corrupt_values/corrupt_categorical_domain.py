
import random

from crptr.corrupt_values.base import CorruptValue
from crptr import base_functions


class CorruptCategoricalDomain(CorruptValue):

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.categories_list =  None
    self.name =            'Categorical Domain'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('categories')):
        base_functions.check_is_list('categories_list', value)
        self.categories_list = value
      else:
        base_kwargs[keyword] = value
    base_kwargs['position_function'] = dummy_position

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    base_functions.check_is_list('categories_list',
                                              self.categories_list)
  def corrupt_value(self, in_str):
    """Method which corrupts the given input string and returns the modified
       string by randomly selecting an edit operation and position in the
       string where to apply this edit.
    """
    if in_str not in self.categories_list:
      return in_str
    #cat_list = self.categories_list
    if in_str in self.categories_list:
      new_str = in_str
      while new_str == in_str:
        new_str = random.choice(self.categories_list)
      return new_str