# -----------------------------------------------------------------------------
# Import necessary modules

import math
import random

import crptr.base_functions as base_functions

class Crptr:
  """Main Crptr class which provides methods to corrupt the records in a given
     dataset. The following arguments need to be set when a Crptr instance is
     initialised:

     number_of_mod_records  The number of modified (corrupted) records that are
                            to be generated. This will correspond to the number
                            of 'duplicate' records that are generated.

     number_of_org_records  The number of records in the original dataset.

     attribute_name_list    The list of attributes (fields) in the dataset.

     max_num_dup_per_rec    The maximum number of modified (corrupted) records
                            that can be generated for a single original record.

     num_dup_dist           The probability distribution used to create 
                            duplicate records for a record (possible
                            distributions are: 'uniform', 'poisson', 'zipf').

     max_num_mod_per_attr   The maximum number of modifications to apply to a
                            single attribute.

     num_mod_per_rec        The number of modifications that are to be applied
                            to a record.

     attr_mod_prob_dict     This dictionary contains probabilities that
                            determine how likely an attribute is selected for
                            random modification (corruption).

                            Keys are attribute names and values are probability
                            values, which must sum to 1.0.

                            Not all attributes need to be listed in this
                            dictionary, only the ones onto which modifications
                            are to be applied.

                            An example of such a dictionary is given below.

     attr_mod_data_dict     A dictionary which, for each attribute that is to be
                            modified, contains a list of pairs of probabilities
                            and corruptor objects (i.e. classes from the
                            'corrupt_values' package).

                            For each attribute listed, the sum of probabilities
                            given in its list must sum to 1.0.
                            
                            An example of such a dictionary is given below.

     Example for 'attr_mod_prob_dict':

     attr_mod_prob_dict = {'surname':0.4, 'address':0.6}

     In this example, the surname attribute will be selected for modification
     with a 40% likelihood and the address attribute with a 60% likelihood.

     Example for 'attr_mod_data_dict':

     attr_mod_data_dict = {'surname':[(0.25,corrupt_ocr), (0.50:corrupt_edit),
                                      (0.25:corrupt_keyboard)],
                           'address':[(0.50:corrupt_ocr), (0.20:missing_value),
                                      (0.25:corrupt_keyboard)]}

     In this example, if the 'surname' is selected for modification, with a
     25% likelihood an OCR modification will be applied, with 50% likelihood a
     character edit modification will be applied, and with 25% likelihood a
     keyboard typing error modification will be applied.
     If the 'address' attribute is selected, then with 50% likelihood an OCR
     modification will be applied, with 20% likelihood a value will be set to
     a missing value, and with 25% likelihood a keyboard typing error
     modification will be applied.
  """

  # ---------------------------------------------------------------------------

  def __init__(self, **kwargs):
    """Constructor, set attributes.
    """

    self.number_of_mod_records = None
    self.number_of_org_records = None
    self.attribute_name_list =   None
    self.max_num_dup_per_rec =   None
    self.num_dup_dist =          None
    self.num_mod_per_rec =       None
    self.max_num_mod_per_attr =  None
    self.attr_mod_prob_dict =    None
    self.attr_mod_data_dict =    None

    # Process the keyword arguments
    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('number_of_m')):
        base_functions.check_is_integer('number_of_mod_records', value)
        base_functions.check_is_positive('number_of_mod_records', value)
        self.number_of_mod_records = value

      elif (keyword.startswith('number_of_o')):
        base_functions.check_is_integer('number_of_org_records', value)
        base_functions.check_is_positive('number_of_org_records', value)
        self.number_of_org_records = value

      elif (keyword.startswith('attribute')):
        base_functions.check_is_list('attribute_name_list', value)
        self.attribute_name_list = value

      elif (keyword.startswith('max_num_dup')):
        base_functions.check_is_integer('max_num_dup_per_rec', value)
        base_functions.check_is_positive('max_num_dup_per_rec', value)
        self.max_num_dup_per_rec = value

      elif (keyword.startswith('num_dup_')):
        if (value not in ['uniform', 'poisson', 'zipf']):
          raise Exception('Illegal value given for "num_dup_dist": %s' % \
                           (str(value)))
        self.num_dup_dist = value

      elif (keyword.startswith('num_mod_per_r')):
        base_functions.check_is_integer('num_mod_per_rec', value)
        base_functions.check_is_positive('num_mod_per_rec', value)
        self.num_mod_per_rec = value

      elif (keyword.startswith('max_num_mod_per_a')):
        base_functions.check_is_integer('max_num_mod_per_attr', value)
        base_functions.check_is_positive('max_num_mod_per_attr', value)
        self.max_num_mod_per_attr = value

      elif (keyword.startswith('attr_mod_p')):
        base_functions.check_is_dictionary('attr_mod_prob_dict', value)
        self.attr_mod_prob_dict = value

      elif (keyword.startswith('attr_mod_d')):
        base_functions.check_is_dictionary('attr_mod_data_dict', value)
        self.attr_mod_data_dict = value

      else:
        raise Exception('Illegal constructor argument keyword: "%s"' % (str(keyword)))

    # Check if the necessary variables have been set
    base_functions.check_is_integer('number_of_mod_records', self.number_of_mod_records)
    base_functions.check_is_positive('number_of_mod_records', self.number_of_mod_records)
    base_functions.check_is_integer('number_of_org_records', self.number_of_org_records)
    base_functions.check_is_positive('number_of_org_records', self.number_of_org_records)
    base_functions.check_is_list('attribute_name_list', self.attribute_name_list)
    base_functions.check_is_integer('max_num_dup_per_rec', self.max_num_dup_per_rec)
    base_functions.check_is_positive('max_num_dup_per_rec', self.max_num_dup_per_rec)
    base_functions.check_is_string('num_dup_dist', self.num_dup_dist)
    base_functions.check_is_integer('num_mod_per_rec', self.num_mod_per_rec)
    base_functions.check_is_positive('num_mod_per_rec', self.num_mod_per_rec)
    base_functions.check_is_integer('max_num_mod_per_attr', self.max_num_mod_per_attr)
    base_functions.check_is_positive('max_num_mod_per_attr', self.max_num_mod_per_attr)

    if self.max_num_mod_per_attr > self.num_mod_per_rec :
      raise Exception('Number of modifications per record must be larger' +
                      ' than maximum number of modifications per attribute')

    base_functions.check_is_dictionary('attr_mod_prob_dict', self.attr_mod_prob_dict)
    base_functions.check_is_dictionary('attr_mod_data_dict', self.attr_mod_data_dict)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Check if it is possible to generate the desired number of modified
    # (duplicate) corrupted records
    if self.number_of_mod_records > self.number_of_org_records * self.max_num_dup_per_rec :
      raise Exception('Desired number of duplicates cannot be generated ' +
                      'with given number of original records and maximum' +
                      ' number of duplicates per original record')

    # Check if there are enough attributes given for modifications - - - - - -
    if (len(self.attr_mod_prob_dict) < self.num_mod_per_rec):
      raise Exception('Not enough attribute modifications given to obtain' +
                      ' the desired number of modifications per record')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Create a distribution for the number of duplicates for an original record
    num_dup = 1
    prob_sum = 0.0
    self.prob_dist_list = [(num_dup, prob_sum)]

    if self.num_dup_dist == 'uniform' :
      uniform_val = 1.0 / float(self.max_num_dup_per_rec)

      for i in range(self.max_num_dup_per_rec-1):
        num_dup += 1
        self.prob_dist_list.append((num_dup,
                                    uniform_val+self.prob_dist_list[-1][1]))

    elif self.num_dup_dist == 'poisson' :

      def fac(n):  # Factorial of an integer number (recursive calculation)
        if (n > 1.0):
          return n*fac(n - 1.0)
        else:
          return 1.0

      poisson_num = []   # A list of poisson numbers
      poisson_sum = 0.0  # The sum of all poisson number

      # The mean (lambda) for the poisson numbers
      mean = 1.0 + (float(self.number_of_mod_records) / float(self.number_of_org_records))

      for i in range(self.max_num_dup_per_rec):
        poisson_num.append((math.exp(-mean) * (mean ** i)) / fac(i))
        poisson_sum += poisson_num[-1]

      for i in range(self.max_num_dup_per_rec):  # Scale so they sum up to 1.0
        poisson_num[i] = poisson_num[i] / poisson_sum

      for i in range(self.max_num_dup_per_rec-1):
        num_dup += 1
        self.prob_dist_list.append((num_dup,
                                    poisson_num[i]+self.prob_dist_list[-1][1]))

    elif self.num_dup_dist == 'zipf' :
      zipf_theta = 0.5

      denom = 0.0
      for i in range(self.number_of_org_records):
        denom += (1.0 / (i+1) ** (1.0 - zipf_theta))

      zipf_c = 1.0 / denom
      zipf_num = []  # A list of Zipf numbers
      zipf_sum = 0.0  # The sum of all Zipf number

      for i in range(self.max_num_dup_per_rec):
        zipf_num.append(zipf_c / ((i+1) ** (1.0 - zipf_theta)))
        zipf_sum += zipf_num[-1]

      for i in range(self.max_num_dup_per_rec):  # Scale so they sum up to 1.0
        zipf_num[i] = zipf_num[i] / zipf_sum

      for i in range(self.max_num_dup_per_rec-1):
        num_dup += 1
        self.prob_dist_list.append((num_dup,
                                    zipf_num[i]+self.prob_dist_list[-1][1]))

    print('Probability distribution for number of duplicates per record:')
    print(self.prob_dist_list)

    # Check probability list for attributes and dictionary for attributes - - -
    # if they sum to 1.0
    #
    attr_prob_sum = sum(self.attr_mod_prob_dict.values())
    if (abs(attr_prob_sum - 1.0) > 0.0000001):
      raise Exception('Attribute modification probabilities do not sum ' + \
                       'to 1.0: %f' % (attr_prob_sum))
    for attr_name in self.attr_mod_prob_dict:
      assert self.attr_mod_prob_dict[attr_name] >= 0.0, \
             'Negative probability given in "attr_mod_prob_dict"'
      if attr_name not in self.attribute_name_list:
        raise Exception('Attribute name "%s" in "attr_mod_prob_dict" not ' % \
                         (attr_name) + 'listed in "attribute_name_list"')

    # Check details of attribute modification data dictionary
    #
    for (attr_name, attr_mod_data_list) in list(self.attr_mod_data_dict.items()):
      if attr_name not in self.attribute_name_list:
        raise Exception('Attribute name "%s" in "attr_mod_data_dict" not ' % \
                         (attr_name) + 'listed in "attribute_name_list"')
      base_functions.check_is_list('attr_mod_data_dict entry',
                                  attr_mod_data_list)
      prob_sum = 0.0
      for list_elem in attr_mod_data_list:
        base_functions.check_is_tuple('attr_mod_data_dict list element',
                                     list_elem)
        assert len(list_elem) == 2, 'attr_mod_data_dict list element does ' + \
                                    'not consist of two elements'
        base_functions.check_is_normalised('attr_mod_data_dict list probability',
                                          list_elem[0])
        prob_sum += list_elem[0]
      if (abs(prob_sum - 1.0) > 0.0000001):
        raise Exception('Probability sum is no 1.0 for attribute "%s"' % \
                         (attr_name))

    # Generate a list with attribute probabilities summed for easy selection
    #
    self.attr_mod_prob_list = []
    prob_sum = 0
    for (attr_name, attr_prob) in list(self.attr_mod_prob_dict.items()):
      prob_sum += attr_prob
      self.attr_mod_prob_list.append([prob_sum, attr_name])
    #print self.attr_mod_prob_list

  # ---------------------------------------------------------------------------

  def corrupt_records(self, rec_dict):
    """Method to corrupt modify the records in the given record dictionary
       according to the settings of the data set corruptor.
    """

    # Check if number of records given is what is expected
    #
    assert self.number_of_org_records == len(rec_dict), \
           'Illegal number of records to modify given'

    # First generate for each original record the number of duplicates that are
    # to be generated for it.
    #
    dup_rec_num_dict = {}  # Keys are the record identifiers of the original
                           # records, value their number of duplicates
    total_num_dups = 0     # Total number of duplicates generated

    org_rec_id_list = list(rec_dict.keys())
    random.shuffle(org_rec_id_list)

    org_rec_i = 0  # Loop counter over which record to assign duplicates to

    while ((org_rec_i < self.number_of_org_records) and \
           (total_num_dups < self.number_of_mod_records)):

      # Randomly choose how many duplicates to create for this original record
      #
      r = random.random()  # Random number between 0.0 and 1.0
      ind = -1
      while (self.prob_dist_list[ind][1] > r):
        ind -= 1
      num_dups = self.prob_dist_list[ind][0]

      assert (num_dups > 0) and (num_dups <= self.max_num_dup_per_rec)

      # Check if there are still 'enough' duplicates to generate
      #
      if (num_dups <= (self.number_of_mod_records-total_num_dups)):

        # Select next record for which to generate duplicates
        #
        org_rec_id = org_rec_id_list[org_rec_i]
        org_rec_i += 1
        dup_rec_num_dict[org_rec_id] = num_dups
        total_num_dups += num_dups

    assert total_num_dups == sum(dup_rec_num_dict.values())

    # Deal with the case where every original record has a number of duplicates
    # but not enough duplicates are generated in total
    #
    org_rec_id_list = list(rec_dict.keys())
    random.shuffle(org_rec_id_list)

    while (total_num_dups < self.number_of_mod_records):
      org_rec_id = random.choice(org_rec_id_list)

      # If possible, increase number of duplicates for this record by 1
      #
      if (dup_rec_num_dict[org_rec_id] < self.max_num_dup_per_rec):
        dup_rec_num_dict[org_rec_id] = dup_rec_num_dict[org_rec_id]+1
        total_num_dups += 1

    assert sum(dup_rec_num_dict.values()) == self.number_of_mod_records

    # Generate a histogram of number of duplicates per record
    #
    dup_histo = {}
    for (org_rec_id_to_mod, num_dups) in dup_rec_num_dict.items():
      dup_count = dup_histo.get(num_dups, 0) + 1
      dup_histo[num_dups] = dup_count
    print('Distribution of number of original records with certain number ' + \
          'of duplicates:')
    dup_histo_keys = list(dup_histo.keys())
    dup_histo_keys.sort()
    for num_dups in dup_histo_keys:
      print(' Number of records with %d duplicates: %d' % \
            (num_dups, dup_histo[num_dups]))
    print()

    num_dup_rec_created = 0  # Count how many duplicate records have been
                             # generated


    # Main loop over all original records for which to generate duplicates - -
    #
    for (org_rec_id_to_mod, num_dups) in dup_rec_num_dict.items():
      assert (num_dups > 0) and (num_dups <= self.max_num_dup_per_rec)
      self.process_records(num_dup_rec_created, num_dups, org_rec_id_to_mod, rec_dict)


    return rec_dict

  def process_records(self, num_dup_rec_created, num_dups, org_rec_id_to_mod, rec_dict):
    print()
    print('Generating %d modified (duplicate) records for record "%s"' % \
          (num_dups, org_rec_id_to_mod))
    rec_to_mod_list = rec_dict[org_rec_id_to_mod]
    d = 0  # Loop counter for duplicates for this record
    this_dup_rec_list = []  # A list of all duplicates for this record
    # Loop to create duplicate records - - - - - - - - - - - - - - - - - - - -
    while (d < num_dups):

      # Create a duplicate of the original record
      #
      dup_rec_list = rec_to_mod_list[:]  # Make copy of original record

      org_rec_num = org_rec_id_to_mod.split('-')[1]
      dup_rec_id = 'rec-%s-dup-%d' % (org_rec_num, d)
      print('  Generate identifier for duplicate record based on "%s": %s' \
            % (org_rec_id_to_mod, dup_rec_id))

      # Count the number of modifications in this record (counted as the
      # number of modified attributes)
      #
      num_mod_in_record = 0

      # Set the attribute modification counters to zero for all attributes
      # that can be modified
      #
      attr_mod_count_dict = {}
      for attr_name in list(self.attr_mod_prob_dict.keys()):
        attr_mod_count_dict[attr_name] = 0

      # Abort generating modifications after a larger number of tries to
      # prevent an endless loop
      max_num_tries = self.num_mod_per_rec * 10
      num_tries = 0

      # Now apply desired number of modifications to this record
      while ((num_mod_in_record < self.num_mod_per_rec) and
             (num_tries < max_num_tries)):

        # Randomly modify an attribute value
        r = random.random()  # Random value between 0.0 and 1.0
        i = 0
        while (self.attr_mod_prob_list[i][0] < r):
          i += 1
        mod_attr_name = self.attr_mod_prob_list[i][1]

        if (attr_mod_count_dict[mod_attr_name] < self.max_num_mod_per_attr):
          mod_attr_name_index = self.attribute_name_list.index(mod_attr_name)
          mod_attr_val = dup_rec_list[mod_attr_name_index]

          # Select an attribute to modify according to probability
          # distribution of corruption methods
          #
          attr_mod_data_list = self.attr_mod_data_dict[mod_attr_name]

          r = random.random()  # Random value between 0.0 and 1.0
          p_sum = attr_mod_data_list[0][0]
          i = 0
          while (r >= p_sum):
            i += 1
            p_sum += attr_mod_data_list[i][0]
          corruptor_method = attr_mod_data_list[i][1]
          # record level handling =============start================
          if mod_attr_name == 'crptr-record':
            mod_rec_list = dup_rec_list[:]
            new_rec_val = corruptor_method.corrupt_value(mod_rec_list)
            org_rec_val = rec_to_mod_list[:]
            if (new_rec_val != org_rec_val):
              print('  Selected attribute for modification:', mod_attr_name)
              print('    Selected corruptor:', corruptor_method.name)

              # The following weird string printing construct is to overcome
              # problems with printing non-ASCII characters
              #
              print('      Original record value:', str(org_rec_val)[1:-1])
              print('      Modified record value:', str(new_rec_val)[1:-1])

              dup_rec_list = new_rec_val

              # One more modification for this attribute
              #
              attr_mod_count_dict[mod_attr_name] += 1

              # The number of modifications in a record corresponds to the
              # number of modified attributes
              #
              num_mod_in_record = 0

              for num_attr_mods in list(attr_mod_count_dict.values()):
                if (num_attr_mods > 0):
                  num_mod_in_record += 1  # One more modification
                assert num_mod_in_record <= self.num_mod_per_rec

            num_tries += 1  # One more try to modify record

          # record level handling =============end===============
          else:

            # Modify the value from the selected attribute
            #
            new_attr_val = corruptor_method.corrupt_value(mod_attr_val)

            org_attr_val = rec_to_mod_list[mod_attr_name_index]

            # If the modified value is different insert it back into modified
            # record
            #
            if (new_attr_val != org_attr_val):
              print('  Selected attribute for modification:', mod_attr_name)
              print('    Selected corruptor:', corruptor_method.name)

              # The following weird string printing construct is to overcome
              # problems with printing non-ASCII characters
              #
              print('      Original attribute value:', str([org_attr_val])[1:-1])
              print('      Modified attribute value:', str([new_attr_val])[1:-1])

              dup_rec_list[mod_attr_name_index] = new_attr_val

              # One more modification for this attribute
              #
              attr_mod_count_dict[mod_attr_name] += 1

              # The number of modifications in a record corresponds to the
              # number of modified attributes
              #
              num_mod_in_record = 0

              for num_attr_mods in list(attr_mod_count_dict.values()):
                if (num_attr_mods > 0):
                  num_mod_in_record += 1  # One more modification
              assert num_mod_in_record <= self.num_mod_per_rec

            num_tries += 1  # One more try to modify record

      # Check if this duplicate is different from all others for this original
      # record
      #
      is_diff = True  # Flag to check if the latest duplicate is different

      if (this_dup_rec_list == []):  # No duplicate so far
        this_dup_rec_list.append(dup_rec_list)
      else:
        for check_dup_rec in this_dup_rec_list:
          if (check_dup_rec == dup_rec_list):  # Same as a previous duplicate
            is_diff = False
            print('Same duplicate:', check_dup_rec)
            print('               ', dup_rec_list)

      if (is_diff == True):  # Only keep duplicate records that are different

        # Safe the record into the overall record dictionary
        #
        rec_dict[dup_rec_id] = dup_rec_list

        d += 1
        num_dup_rec_created += 1

        print('Original record:')
        print(' ', rec_to_mod_list)
        print('Record with %d modified attributes' % (num_mod_in_record), end=' ')
        attr_mod_str = '('
        for a in self.attribute_name_list:
          if (attr_mod_count_dict.get(a, 0) > 0):
            attr_mod_str += '%d in %s, ' % (attr_mod_count_dict[a], a)
        attr_mod_str = attr_mod_str[:-1] + '):'
        print(attr_mod_str)
        print(' ', dup_rec_list)
        print('%d of %d duplicate records generated so far' % \
              (num_dup_rec_created, self.number_of_mod_records))
        print()

# =============================================================================