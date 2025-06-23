import crptr.base_functions as base_functions


# ===============================================================================
# Classes for corrupting a value in a list of attributes (fields) of the data set
# ===============================================================================
#attr_name_list Need to be included in this model to allow index selection from records for record level corruptions

#attr_name_list = ['crptr-record','FirstName', 'LastName','Gender','DateofBirth','FatherFirstName','FatherLastName', 'FatherOccupation',	'MotherFirstName', 'MotherLastName', 'MotherOccupation']

class CorruptRecord:
  """Base class for the definition of corruptor that is applied on a single
     attribute (field) in the data set.

     This class and all of its derived classes provide methods that allow the
     definition of how values in a single attribute are corrupted (modified)
     and the parameters necessary for the corruption process.

     The following variables need to be set when a CorruptValue instance is
     initialised (with further parameters listed in the derived classes):

     position_function  A function that (somehow) determines the location
                        within a string value of where a modification
                        (corruption) is to be applied. The input of this
                        function is assumed to be a string and its return value
                        an integer number in the range of the length of the
                        given input string.
  """

  # ---------------------------------------------------------------------------
#AHMAD# in the initiation (__init__) arguments inserted are checked, valedated and procssed to be used
  def __init__(self, base_kwargs):
    """Constructor, set general attributes.
    """

    # General attributes for all attribute corruptors.
    #
    self.position_function = None

    # Process the keyword argument (all keywords specific to a certain data
    # generator type were processed in the derived class constructor)
    #
    for (keyword, value) in list(base_kwargs.items()):
#AHMAD#This is checking from calls in generate-data-english.py file
#AHMAD# 'position' realted to the inserted argument in the file config and same to others
      if (keyword.startswith('position')):
        base_functions.check_is_function_or_method('position_function', value)
        #AHMAD# setting position to the given value in the file
        #-----# in this case one of the functions (position_mod_normal or position_mod_uniform)
        self.position_function = value

      else:
        raise Exception('Illegal constructor argument keyword: "%s"' % \
              (str(keyword)))

    base_functions.check_is_function_or_method('position_function',
                                              self.position_function)

    # Check if the position function does return an integer value
    #
    pos = self.position_function('test')
    if ((not isinstance(pos, int)) or (pos < 0) or (pos > 3)):
      raise Exception('Position function returns an illegal value (either' + \
                       'not an integer or and integer out of range: %s' % \
                       (str(pos)))

  # ---------------------------------------------------------------------------

  def corrupt_value(self, list):
    """Method which corrupts the given input list of strings and returns the modified
       list.
       See implementations in derived classes for details.
    """

    raise Exception('Override abstract method in derived class')
