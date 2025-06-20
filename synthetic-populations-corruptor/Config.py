from . import CorrupterBStandard
from . import CorrupterAocr
import time
import sys

print("Init: " + str(time.time()))

dirName = "scotland-l"

popNames = {"synthetic-scotland"}
popSizes = {"10m"} #{"13k","133k","530k"} #{"120k","178k","235k"} #"2390k","3200k","4800k"
popNumbers = {"1"} #,"2","3","4","5"}
corruptionLetters = {"A", "B", "C"}

for popName in popNames:
    for popSize in popSizes:
        for popNumber in popNumbers:
            for corruptionLetter in  corruptionLetters:
    
                # Files
                birthInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/clean/birth_records.csv"
                birthOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/" + popName +"/_" + popSize +"/_" + popNumber +"/corrupted/_" + corruptionLetter + "/birth_records.csv"
                birthLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/" + popName +"/_" + popSize +"/_" + popNumber +"/corrupted/_" + corruptionLetter + "/log/birth_crptr_log.csv"
                
                deathInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/clean/death_records.csv"
                deathOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/" + popName +"/_" + popSize +"/_" + popNumber +"/corrupted/_" + corruptionLetter + "/death_records.csv"
                deathLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/" + popName +"/_" + popSize +"/_" + popNumber +"/corrupted/_" + corruptionLetter + "/log/death_crptr_log.csv"
                
                marriageInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/clean/marriage_records.csv"
                marriageOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/" + popName +"/_" + popSize +"/_" + popNumber +"/corrupted/_" + corruptionLetter + "/marriage_records.csv"
                marriageLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations-"+dirName+"/src/main/resources/uk/ac/standrews/cs/data/synthetic/" + popName +"/_" + popSize +"/_" + popNumber +"/corrupted/_" + corruptionLetter + "/log/marriage_crptr_log.csv"
                
                lookupFilesDir = "/Users/tdalton/tom/phd/repos/crptr-fork/lookup-files"
                

                # Determinism
                deterministic = True
                seed = 12345
                
                # Corruption setup
                a_proportionOfRecordsToCorrupt = 0.4
                a_maxModificationsPerAttribute = 2
                a_numberOfModificationsPerRecord = 4
                a_recordLevelProportion = 0.25

                b_proportionOfRecordsToCorrupt = 0.4
                b_maxModificationsPerAttribute = 2
                b_numberOfModificationsPerRecord = 4
                b_recordLevelProportion = 0.25

                c_proportionOfRecordsToCorrupt = 0.9
                c_maxModificationsPerAttribute = 2
                c_numberOfModificationsPerRecord = 8
                c_recordLevelProportion = 0.5

                sys.stdout.write(popSize + "," + popNumber + "," + corruptionLetter + ",")
                st = time.time()

                if corruptionLetter == "A":
                    CorrupterAocr.birthCorruptor(birthInputFile, birthOutputFile, birthLogFile, lookupFilesDir, deterministic, seed,
                                                  a_proportionOfRecordsToCorrupt, a_maxModificationsPerAttribute,
                                                 a_numberOfModificationsPerRecord, a_recordLevelProportion)

                if corruptionLetter == "B":
                    CorrupterBStandard.birthCorruptor(birthInputFile, birthOutputFile, birthLogFile, lookupFilesDir, deterministic, seed,
                                                  b_proportionOfRecordsToCorrupt, b_maxModificationsPerAttribute,
                                                      b_numberOfModificationsPerRecord, b_recordLevelProportion)

                if corruptionLetter == "C":
                    CorrupterBStandard.birthCorruptor(birthInputFile, birthOutputFile, birthLogFile, lookupFilesDir, deterministic, seed,
                                                  c_proportionOfRecordsToCorrupt, c_maxModificationsPerAttribute,
                                                      c_numberOfModificationsPerRecord, c_recordLevelProportion)

                sys.stdout.write(str(time.time()-st) + ",")
                
                st = time.time()

                if corruptionLetter == "A":
                    CorrupterAocr.deathCorruptor(deathInputFile, deathOutputFile, deathLogFile, lookupFilesDir, deterministic, seed,
                                                 a_proportionOfRecordsToCorrupt, a_maxModificationsPerAttribute,
                                                 a_numberOfModificationsPerRecord, a_recordLevelProportion)

                if corruptionLetter == "B":
                    CorrupterBStandard.deathCorruptor(deathInputFile, deathOutputFile, deathLogFile, lookupFilesDir, deterministic, seed,
                                                      b_proportionOfRecordsToCorrupt, b_maxModificationsPerAttribute,
                                                      b_numberOfModificationsPerRecord, b_recordLevelProportion)

                if corruptionLetter == "C":
                    CorrupterBStandard.deathCorruptor(deathInputFile, deathOutputFile, deathLogFile, lookupFilesDir, deterministic, seed,
                                                      c_proportionOfRecordsToCorrupt, c_maxModificationsPerAttribute,
                                                      c_numberOfModificationsPerRecord, c_recordLevelProportion)

                sys.stdout.write(str(time.time()-st) + ",")
                
                st = time.time()

                if corruptionLetter == "A":
                    CorrupterAocr.marriageCorruptor(marriageInputFile, marriageOutputFile, marriageLogFile, lookupFilesDir, deterministic, seed,
                                                    a_proportionOfRecordsToCorrupt, a_maxModificationsPerAttribute,
                                                    a_numberOfModificationsPerRecord, a_recordLevelProportion)


                if corruptionLetter == "B":
                    CorrupterBStandard.marriageCorruptor(marriageInputFile, marriageOutputFile, marriageLogFile, lookupFilesDir, deterministic, seed,
                                                         b_proportionOfRecordsToCorrupt, b_maxModificationsPerAttribute,
                                                         b_numberOfModificationsPerRecord, b_recordLevelProportion)

                if corruptionLetter == "C":
                    CorrupterBStandard.marriageCorruptor(marriageInputFile, marriageOutputFile, marriageLogFile, lookupFilesDir, deterministic, seed,
                                                         c_proportionOfRecordsToCorrupt, c_maxModificationsPerAttribute,
                                                         c_numberOfModificationsPerRecord, c_recordLevelProportion)

                sys.stdout.write(str(time.time()-st) + "\n")
                    
