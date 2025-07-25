#!/usr/bin/python
# Author: James Ross (jar35@st-andrews.ac.uk)
# 24/6/2015
#
# A config object implemention of the corruption profile 'C', for use with
# standard corruptor, as defined in Tom Daltons thesis (see 7.4)
# https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/26784/Thesis-Tom-Dalton-complete-version.pdf?sequence=4&isAllowed=y

class CorruptionProfileC:
    PROPORTION_TO_CORRUPT = 0.9
    MAX_MODIFICATIONS_PER_ATTR = 2
    MODIFICATIONS_PER_RECORD = 8
    # ATTR_LEVEL_PROPORTION is defined in Thesis but unused
    ATTR_LEVEL_PROPORTION = 0.5
    RECORD_LEVEL_PROPORTION = 0.5