import random

from crptr import base_functions
from crptr.corrupt_values.base import CorruptValue


class CorruptValuePhonetic(CorruptValue):
  """Simulate phonetic errors using a list of phonetic rules which are stored
     in a CSV look-up file.

     Each line (row) in the CSV file must consist of seven columns that contain
     the following information:
     1) Where a phonetic modification can be applied. Possible values are:
        'ALL','START','END','MIDDLE'
     2) The original character sequence (i.e. the characters to be replaced)
     3) The new character sequence (which will replace the original sequence)
     4) Precondition: A condition that must occur before the original string
        character sequence in order for this rule to become applicable.
     5) Postcondition: Similarly, a condition that must occur after the
        original string character sequence in order for this rule to become
        applicable.
     6) Pattern existence condition: This condition requires that a certain
        given string character sequence does ('y' flag) or does not ('n' flag)
        occur in the input string.
     7) Start existence condition: Similarly, this condition requires that the
        input string starts with a certain string pattern ('y' flag) or not
        ('n' flag)

     A detailed description of this phonetic data generation is available in

       Accurate Synthetic Generation of Realistic Personal Information
       Peter Christen and Agus Pudjijono
       Proceedings of the Pacific-Asia Conference on Knowledge Discovery and
                          Data Mining (PAKDD), Bangkok, Thailand, April 2009.

     For a given input string, one of the possible phonetic modifications will
     be randomly selected without the use of the position function.

     The additional arguments (besides the base class argument
     'position_function') that have to be set when this attribute type is
     initialised are:

     lookup_file_name  Name of the file which contains the phonetic
                       modification patterns.

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
    self.replace_table =    []
    self.name =             'Phonetic value'

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
      if (len(rec_list) != 7):
        raise Exception('Illegal format in phonetic lookup file %s: %s' \
                         % (self.lookup_file_name, str(rec_list)))
      val_tuple = ()
      for val in rec_list:
        if (val != ''):
          val = val.strip()
          val_tuple += val,
        else:
          raise Exception('Empty value in phonetic lookup file %s" %s' % \
                           (self.lookup_file_name, str(rec_list)))
      self.replace_table.append(val_tuple)

  # ---------------------------------------------------------------------------

  def __apply_change__(self, in_str, ch):
    """Helper function which will apply the selected change to the input
       string.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    work_str = in_str
    list_ch = ch.split('>')
    subs = list_ch[1]
    if (list_ch[1] == '@'): # @ is blank
      subs = ''
    tmp_str = work_str
    org_pat_length = len(list_ch[0])
    str_length =     len(work_str)

    if (list_ch[2] == 'end'):
      org_pat_start = work_str.find(list_ch[0], str_length-org_pat_length)
    elif (list_ch[2] == 'middle'):
      org_pat_start = work_str.find(list_ch[0],1)
    else: # Start and all
      org_pat_start = work_str.find(list_ch[0],0)

    if (org_pat_start == 0):
      work_str = subs + work_str[org_pat_length:]
    elif (org_pat_start > 0):
      work_str = work_str[:org_pat_start] + subs + \
                 work_str[org_pat_start+org_pat_length:]

    if (work_str == tmp_str):
      work_str = in_str

    return work_str

  # ---------------------------------------------------------------------------

  def __slavo_germanic__(self, in_str):
    """Helper function which determines if the inputstring could contain a
       Slavo or Germanic name.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    if ((in_str.find('w') > -1) or (in_str.find('k') > -1) or \
        (in_str.find('cz') > -1) or (in_str.find('witz') > -1)):
      return 1
    else:
      return 0

  # ---------------------------------------------------------------------------

  def __collect_replacement__(self, s, where, orgpat, newpat, precond,
                              postcond, existcond, startcond):
    """Helper function which collects all the possible phonetic modification
       patterns that are possible on the given input string, and replaces a
       pattern in a string.

       The following arguments are needed:
       - where     Can be one of: 'ALL','START','END','MIDDLE'
       - precond   Pre-condition (default 'None') can be 'V' for vowel or
                   'C' for consonant
       - postcond  Post-condition (default 'None') can be 'V' for vowel or
                   'C' for consonant

       Developed by Agus Pudjijono, ANU, 2008.
    """

    if not is_ascii(s):
      return s

    vowels = 'aeiouy'
    tmpstr = s
    changesstr = ''

    start_search = 0  # Position from where to start the search
    pat_len =      len(orgpat)
    stop =         False

    # As long as pattern is in string
    #
    while ((orgpat in tmpstr[start_search:]) and (stop == False)):

      pat_start = tmpstr.find(orgpat, start_search)
      str_len =   len(tmpstr)

      # Check conditions of previous and following character
      #
      OKpre  = False   # Previous character condition
      OKpre1 = False   # Previous character1 condition
      OKpre2 = False   # Previous character2 condition

      OKpost  = False  # Following character condition
      OKpost1 = False  # Following character1 condition
      OKpost2 = False  # Following character2 condition

      OKexist = False  # Existing pattern condition
      OKstart = False  # Existing start pattern condition

      index =  0

      if (precond == 'None'):
        OKpre = True

      elif (pat_start > 0):
        if (((precond == 'V') and (tmpstr[pat_start-1] in vowels)) or \
            ((precond == 'C') and (tmpstr[pat_start-1] not in vowels))):
          OKpre = True

        elif ((precond.find(';')) > -1):
          if (precond.find('|') > -1):
            rls=precond.split('|')
            rl1=rls[0].split(';')

            if (int(rl1[1]) < 0):
              index =  pat_start+int(rl1[1])
            else:
              index =  pat_start+(len(orgpat)-1)+int(rl1[1])

            i=2
            if (rl1[0] == 'n'):
              while (i < (len(rl1))):
                if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                  OKpre1 = False
                  break
                else:
                  OKpre1 = True
                i+=1
            else:
              while (i < (len(rl1))):
                if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                  OKpre1 = True
                  break
                i+=1

            rl2=rls[1].split(';')

            if (int(rl2[1]) < 0):
              index =  pat_start+int(rl2[1])
            else:
              index =  pat_start+(len(orgpat)-1)+int(rl2[1])

            i=2
            if (rl2[0] == 'n'):
              while (i < (len(rl2))):
                if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                  OKpre2 = False
                  break
                else:
                  OKpre2 = True
                i+=1
            else:
              while (i < (len(rl2))):
                if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                  OKpre2 = True
                  break
                i+=1

            OKpre=OKpre1 and OKpre2

          else:
            rl=precond.split(';')
            #-
            if (int(rl[1]) < 0):
              index =  pat_start+int(rl[1])
            else:
              index =  pat_start+(len(orgpat)-1)+int(rl[1])

            i=2
            if (rl[0] == 'n'):
              while (i < (len(rl))):
                if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                  OKpre = False
                  break
                else:
                  OKpre = True
                i+=1
            else:
              while (i < (len(rl))):
                if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                  OKpre = True
                  break
                i+=1

      if (postcond == 'None'):
        OKpost = True

      else:
        pat_end = pat_start+pat_len

        if (pat_end < str_len):
          if (((postcond == 'V') and (tmpstr[pat_end] in vowels)) or \
              ((postcond == 'C') and (tmpstr[pat_end] not in vowels))):
            OKpost = True
          elif ((postcond.find(';')) > -1):
            if (postcond.find('|') > -1):
              rls=postcond.split('|')

              rl1=rls[0].split(';')

              if (int(rl1[1]) < 0):
                index =  pat_start+int(rl1[1])
              else:
                index =  pat_start+(len(orgpat)-1)+int(rl1[1])

              i=2
              if (rl1[0] == 'n'):
                while (i < (len(rl1))):
                  if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                    OKpost1 = False
                    break
                  else:
                    OKpost1 = True
                  i+=1
              else:
                while (i < (len(rl1))):
                  if (tmpstr[index:(index+len(rl1[i]))] == rl1[i]):
                    OKpost1 = True
                    break
                  i+=1

              rl2=rls[1].split(';')

              if (int(rl2[1]) < 0):
                index =  pat_start+int(rl2[1])
              else:
                index =  pat_start+(len(orgpat)-1)+int(rl2[1])

              i=2
              if (rl2[0] == 'n'):
                while (i < (len(rl2))):
                  if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                    OKpost2 = False
                    break
                  else:
                    OKpost2 = True
                  i+=1
              else:
                while (i < (len(rl2))):
                  if (tmpstr[index:(index+len(rl2[i]))] == rl2[i]):
                    OKpost2 = True
                    break
                  i+=1

              OKpost=OKpost1 and OKpost2

            else:
              rl=postcond.split(';')

              if (int(rl[1]) < 0):
                index =  pat_start+int(rl[1])
              else:
                index =  pat_start+(len(orgpat)-1)+int(rl[1])

              i=2
              if (rl[0] == 'n'):
                while (i < (len(rl))):
                  if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                    OKpost = False
                    break
                  else:
                    OKpost = True
                  i+=1
              else:
                while (i < (len(rl))):
                  if (tmpstr[index:(index+len(rl[i]))] == rl[i]):
                    OKpost = True
                    break
                  i+=1

      if (existcond == 'None'):
        OKexist = True

      else:
        rl=existcond.split(';')
        if (rl[1] == 'slavo'):
          r=self.__slavo_germanic__(s)
          if (rl[0] == 'n'):
            if (r == 0):
              OKexist=True
          else:
            if (r == 1):
              OKexist=True
        else:
          i=1
          if (rl[0] == 'n'):
            while (i < (len(rl))):
              if (s.find(rl[i]) > -1):
                OKexist = False
                break
              else:
                OKexist = True
              i+=i
          else:
            while (i < (len(rl))):
              if (s.find(rl[i]) > -1):
                OKexist = True
                break
              i+=i

      if (startcond == 'None'):
        OKstart = True

      else:
        rl=startcond.split(';')
        i=1
        if (rl[0] == 'n'):
          while (i < (len(rl))):
            if (s.find(rl[i]) > -1):
              OKstart = False
              break
            else:
              OKstart = True
            i+=i
        else:
          while (i < (len(rl))):
            if (s.find(rl[i]) == 0):
              OKstart = True
              break
            i+=i

      # Replace pattern if conditions and position OK
      #
      if ((OKpre == True) and (OKpost == True) and (OKexist == True) and \
          (OKstart == True)) and (((where == 'START') and (pat_start == 0)) \
          or ((where == 'MIDDLE') and (pat_start > 0) and \
          (pat_start+pat_len < str_len)) or ((where == 'END') and \
          (pat_start+pat_len == str_len)) or (where == 'ALL')):
        tmpstr = tmpstr[:pat_start]+newpat+tmpstr[pat_start+pat_len:]
        changesstr += ',' +orgpat + '>' + newpat + '>' + where.lower()
        start_search = pat_start + len(newpat)

      else:
        start_search = pat_start+1

      if (start_search >= (len(tmpstr)-1)):
        stop = True

    tmpstr += changesstr

    return tmpstr

  # ---------------------------------------------------------------------------

  def __get_transformation__(self, in_str):
    """Helper function which generates the list of possible phonetic
       modifications for the given input string.

       Developed by Agus Pudjijono, ANU, 2008.
    """

    if (in_str == ''):
      return in_str

    changesstr2 = ''

    workstr = in_str

    for rtpl in self.replace_table:  # Check all transformations in the table
      if (len(rtpl) == 3):
         rtpl += ('None','None','None','None')

      workstr = self.__collect_replacement__(in_str,rtpl[0],rtpl[1],rtpl[2],
                                             rtpl[3],rtpl[4],rtpl[5],rtpl[6])
      if (workstr.find(',') > -1):
        tmpstr = workstr.split(',')
        workstr = tmpstr[0]
        if (changesstr2.find(tmpstr[1]) == -1):
          changesstr2 += tmpstr[1]+';'
    workstr += ',' + changesstr2

    return workstr

  # ---------------------------------------------------------------------------

  def corrupt_value(self, in_str):
    """Method which corrupts the given input string by applying a phonetic
       modification.

       If several such modifications are possible then one will be randomly
       selected.
    """

    if (len(in_str) == 0):  # Empty string, no modification possible
      return in_str

    # Get the possible phonetic modifications for this input string
    #
    phonetic_changes = self.__get_transformation__(in_str)

    mod_str = in_str

    if (',' in phonetic_changes):  # Several modifications possible
      tmp_str = phonetic_changes.split(',')
      pc = tmp_str[1][:-1] # Remove the last ';'
      list_pc = pc.split(';')
      change_op = random.choice(list_pc)
      if (change_op != ''):
        mod_str = self.__apply_change__(in_str, change_op)
        #print in_str, mod_str, change_op

    return mod_str

def is_ascii(s):
  return all(ord(c) < 128 for c in s)