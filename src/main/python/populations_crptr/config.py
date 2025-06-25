#!/usr/bin/python
# Author: James Ross (jar35@st-andrews.ac.uk)
# 24/6/2015
#
# Config object for population_corruptor.py example population corruptor.

from populations_crptr.example_profiles.profile_a import CorruptionProfileA
from populations_crptr.example_profiles.profile_b import CorruptionProfileB
from populations_crptr.example_profiles.profile_c import CorruptionProfileC
import populations_crptr.example_corruptors.standard_corruptors_td as StandardCorruptorsTD
import populations_crptr.example_corruptors.ocr_corruptors_td as OcrCorruptorsTD


class Config:
    PROFILE = CorruptionProfileA
    CORRUPTORS = StandardCorruptorsTD
    OUTPUT_DIR = "results"
    PURPOSE = "default"
    LOOKUP_FILES_DIR = "src/main/resources/lookup-files"
    DETERMINISTIC = False
    SEED = None