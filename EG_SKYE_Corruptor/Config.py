import EGSkyeCorrupter
import time

print "Init: " + str(time.time())

# Files
birthInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/clean/birth_records.csv"
birthOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/corrupt/_1/birth_records.csv"
birthLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/corrupt/_1/logs/birth_crptr_log.csv"

deathInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/clean/death_records.csv"
deathOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/corrupt/_1/death_records.csv"
deathLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/corrupt/_1/logs/death_crptr_log.csv"

marriageInputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/clean/marriage_records.csv"
marriageOutputFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/corrupt/_1/marriage_records.csv"
marriageLogFile = "/Volumes/TSD4exHDD3/valipop-synthetic-populations/src/main/resources/uk/ac/standrews/cs/data/synthetic/scot_test/_570k/_1/corrupt/_1/logs/marriage_crptr_log.csv"

lookupFilesDir = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/lookup-files"


# Determinism
deterministic = True
seed = 12345

# Corruption setup
proportionOfRecordsToCorrupt = 0.1
maxModificationsPerAttribute = 2
numberOfModificationsPerRecord = 4
recordLevelProportion = 0.25

st = time.time()
print "Start time: " + str(time.time())
EGSkyeCorrupter.birthCorruptor(birthInputFile, birthOutputFile, birthLogFile, lookupFilesDir, deterministic, seed,
                               proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                               numberOfModificationsPerRecord, recordLevelProportion)
print "Birth Duration: " + str(time.time()-st)

st = time.time()
EGSkyeCorrupter.deathCorruptor(deathInputFile, deathOutputFile, deathLogFile, lookupFilesDir, deterministic, seed,
                               proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                               numberOfModificationsPerRecord, recordLevelProportion)
print "Death Duration: " + str(time.time()-st)

st = time.time()
EGSkyeCorrupter.marriageCorruptor(marriageInputFile, marriageOutputFile, marriageLogFile, lookupFilesDir, deterministic, seed,
                               proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                               numberOfModificationsPerRecord, recordLevelProportion)
print "Marriage Duration: " + str(time.time()-st)
print "End time: " + str(time.time())