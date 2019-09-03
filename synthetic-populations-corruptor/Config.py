import Corrupter
import time

print "Init: " + str(time.time())

popNames = {"synthetic-scotland"}
popSizes = {"13k", "133k"} #{"13k","133k","530k"}
popNumbers = {"1","2" } # ,"3","4","5"}
corruptionNumbers = {"5","10"}

for popName in popNames:
    for popSize in popSizes:
        for popNumber in popNumbers:
            for corruptionNumber in  corruptionNumbers:
    
                # Files
                birthInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/clean/birth_records.csv"
                birthOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/corrupted/_"+corruptionNumber+"/birth_records.csv"
                birthLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/corrupted/_"+corruptionNumber+"/log/birth_crptr_log.csv"
                
                deathInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/clean/death_records.csv"
                deathOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/corrupted/_"+corruptionNumber+"/death_records.csv"
                deathLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/corrupted/_"+corruptionNumber+"/log/death_crptr_log.csv"
                
                marriageInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/clean/marriage_records.csv"
                marriageOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/corrupted/_"+corruptionNumber+"/marriage_records.csv"
                marriageLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/"+popName+"/_"+popSize+"/_"+popNumber+"/corrupted/_"+corruptionNumber+"/log/marriage_crptr_log.csv"
                
                lookupFilesDir = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/lookup-files"
                
                
                # Determinism
                deterministic = True
                seed = 12345
                
                # Corruption setup
                proportionOfRecordsToCorrupt = 0.1 * float(corruptionNumber)
                maxModificationsPerAttribute = 2
                numberOfModificationsPerRecord = 4
                recordLevelProportion = 0.25
                
                print "Corrupting " + popSize + "_" + popNumber + "_" + corruptionNumber
                
                st = time.time()
                print "Start time: " + str(time.time())
                Corrupter.birthCorruptor(birthInputFile, birthOutputFile, birthLogFile, lookupFilesDir, deterministic, seed,
                                         proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                                         numberOfModificationsPerRecord, recordLevelProportion)
                print "Birth Duration: " + str(time.time()-st)
                
                st = time.time()
                Corrupter.deathCorruptor(deathInputFile, deathOutputFile, deathLogFile, lookupFilesDir, deterministic, seed,
                                         proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                                         numberOfModificationsPerRecord, recordLevelProportion)
                print "Death Duration: " + str(time.time()-st)
                
                st = time.time()
                Corrupter.marriageCorruptor(marriageInputFile, marriageOutputFile, marriageLogFile, lookupFilesDir, deterministic, seed,
                                            proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                                            numberOfModificationsPerRecord, recordLevelProportion)
                print "Marriage Duration: " + str(time.time()-st)
                print "End time: " + str(time.time())
                    
