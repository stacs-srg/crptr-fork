import random
from crptr import base_functions
from crptr.corrupt_values.base import CorruptValue


class CorruptDate(CorruptValue):

  def __init__(self, **kwargs):
    """Constructor. Process the derived keywords first, then call the base
       class constructor.
    """

    self.date_order =  None
    self.separator = None
    self.components_to_modify = None
    self.date_corruption_methods = None
    self.name =            'Date'

    def dummy_position(s):  # Define a dummy position function
      return 0

    # Process all keyword arguments
    #
    base_kwargs = {}  # Dictionary, will contain unprocessed arguments

    for (keyword, value) in list(kwargs.items()):

      if (keyword.startswith('date_ord')):
        base_functions.check_date_order('date_order', value)
        self.date_order = value

      elif (keyword.startswith('separator')):
        base_functions.check_date_separator('separator', value)
        self.separator = value

      elif (keyword.startswith('components')):
        base_functions.check_date_components_to_modify('components_to_modify', value)
        self.components_to_modify = value

      elif (keyword.startswith('date_corruption')):
        base_functions.check_date_modification_methods('date_corruption_methods', value)
        self.date_corruption_methods = value

      else:
        base_kwargs[keyword] = value
    base_kwargs['position_function'] = dummy_position

    CorruptValue.__init__(self, base_kwargs)  # Process base arguments

    # Check if the necessary variables have been set
    #
    base_functions.check_is_non_empty_string('date_order',
                                              self.date_order)
    base_functions.check_is_non_empty_string('separator',
                                self.separator)
    base_functions.check_is_list('components_to_modify',
                                self.components_to_modify)
    base_functions.check_is_list('date_corruption_methods',
                                self.date_corruption_methods)

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string and returns the modified
       string by randomly selecting an edit operation and position in the
       string where to apply this edit.
    """

    if in_str == "missing":
      return in_str  # i.e. previous corruption prevents this corruption

    if self.date_order == "dd-mm-yyyy":
      day, month, year = in_str.split(self.separator)
      day = day.zfill(2)
      month = month.zfill(2)
      year = year.zfill(4)
    elif self.date_order == "mm-dd-yyyy":
      month, day, year = in_str.split(self.separator)
      day = day.zfill(2)
      month = month.zfill(2)
      year = year.zfill(4)
    elif self.date_order == "yyyy-mm-dd":
      year, month, day = in_str.split(self.separator)
      day = day.zfill(2)
      month = month.zfill(2)
      year = year.zfill(4)
    else:
      print("date format and order is not correct")

    comp_mod = random.choice(self.components_to_modify)
    crpt_method = random.choice(self.date_corruption_methods)

    ran_num = random.randint(1, 10)

    if crpt_method == 'add':
      if comp_mod == 'day':
        day = int(day) + ran_num
      elif comp_mod == "month":
        month = int(month) + ran_num
      elif comp_mod == "year":
        year = int(year) + ran_num

    elif crpt_method == "decline":
      if comp_mod == 'day':
        if int(day) - ran_num < 1:
          day = 1
        else:
          day = int(day) - ran_num
      elif comp_mod == "month":
        if int(month) - ran_num < 1:
          month = 1
        else:
          month = int(month) - ran_num
      elif comp_mod == "year":
        year = int(year) - ran_num

    elif crpt_method == "first":
      day = '01'
      month = '01'

    elif crpt_method == "random":
      if comp_mod == "day":
        ran_day = random.randint(1, 30)
        day = ran_day
      elif comp_mod == "month":
        ran_month = random.randint(1, 12)
        month = ran_month
      elif comp_mod == "year":
        ran_year = random.randint(1750, 2100)
        year = ran_year

    elif crpt_method == "swap_comp":
      if comp_mod == "day":
        other_comp = ['month', 'year']
        swap_attr = random.choice(other_comp)
        print(swap_attr)
        if swap_attr == "month":
          h_day = day
          day = month
          month = h_day
        elif swap_attr == "year":
          h_day = day
          day = year
          year = h_day
      elif comp_mod == "month":
        other_comp = ['day', 'year']
        swap_attr = random.choice(other_comp)
        print(swap_attr)
        if swap_attr == "day":
          h_month = month
          month = day
          day = h_month
        elif swap_attr == "year":
          h_month = month
          month = year
          year = h_month
      elif comp_mod == "year":
        other_comp = ['day', 'month']
        swap_attr = random.choice(other_comp)
        print(swap_attr)
        if swap_attr == "day":
          h_year = year
          year = day
          day = h_year
        elif swap_attr == "month":
          h_year = year
          year = month
          month = h_year

    elif crpt_method == "swap_digit":
      if comp_mod == "day":
        comp_lst = list(day)
        print(comp_lst)
        index_lst = list(range(0, len(comp_lst)))
        print(index_lst)
        swap_lst = sorted(random.sample(index_lst, 2))
        print(swap_lst)
        fst_index = comp_lst[swap_lst[0]]
        print(fst_index)
        snd_index = comp_lst[swap_lst[1]]
        print(snd_index)
        comp_lst[swap_lst[0]] = snd_index
        comp_lst[swap_lst[1]] = fst_index
        new_comp = ''.join(comp_lst)
        print(comp_lst)
        print(new_comp)
        day = new_comp

      elif comp_mod == "month":
        comp_lst = list(month)
        print(comp_lst)
        index_lst = list(range(0, len(comp_lst)))
        print(index_lst)
        swap_lst = sorted(random.sample(index_lst, 2))
        print(swap_lst)
        fst_index = comp_lst[swap_lst[0]]
        print(fst_index)
        snd_index = comp_lst[swap_lst[1]]
        print(snd_index)
        comp_lst[swap_lst[0]] = snd_index
        comp_lst[swap_lst[1]] = fst_index
        new_comp = ''.join(comp_lst)
        print(comp_lst)
        print(new_comp)
        month = new_comp
      elif comp_mod == "year":
        comp_lst = list(year)
        print(comp_lst)
        index_lst = list(range(0, len(comp_lst)))
        print(index_lst)
        swap_lst = sorted(random.sample(index_lst, 2))
        print(swap_lst)
        fst_index = comp_lst[swap_lst[0]]
        print(fst_index)
        snd_index = comp_lst[swap_lst[1]]
        print(snd_index)
        comp_lst[swap_lst[0]] = snd_index
        comp_lst[swap_lst[1]] = fst_index
        new_comp = ''.join(comp_lst)
        print(comp_lst)
        print(new_comp)
        year = new_comp

    elif crpt_method == "full_month" or "abbr_month":
      comp_mod = "month"

      try:
        base_functions.check_is_integer('month', month)
      except Exception:
        return in_str  # i.e. previous corruption prevents this corruption

      month = int(month)
      if crpt_method == "full_month":
        full_month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, \
                           'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        for key, value in full_month_dict.items():
          if value == month:
            month = key
      elif crpt_method == "abbr_month":
        abbr_month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, \
                           'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        for key, value in abbr_month_dict.items():
          if value == month:
            month = key

    if self.date_order == "dd-mm-yyyy":
      new_date = str(day) + self.separator + str(month) + self.separator + str(year)
    elif self.date_order == "mm-dd-yyyy":
      new_date = str(month) + self.separator + str(day) + self.separator + str(year)
    elif self.date_order == "yyyy-mm-dd":
      new_date = str(year) + self.separator + str(month) + self.separator + str(day)

    return new_date
