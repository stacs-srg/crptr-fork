import EGSkyeCorrupter
import time

print "Init: " + str(time.time())

# Files
birthInputFile = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/input-files/birth_records.csv"
birthOutputFile = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/output-files/birth_records.csv"
birthLogFile = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/output-files/birth_crptr_log.csv"

deathInputFile = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/input-files/death_records.csv"
deathOutputFile = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/output-files/death_records.csv"
deathLogFile = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/output-files/death_crptr_log.csv"

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
print "Birth: " + str(time.time())
EGSkyeCorrupter.birthCorruptor(birthInputFile, birthOutputFile, birthLogFile, lookupFilesDir, deterministic, seed,
                               proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                               numberOfModificationsPerRecord, recordLevelProportion)
print "Birth conclude: " + str(time.time())
print "Birth Duration: " + str(time.time()-st)

st = time.time()
print "Death: " + str(time.time())
EGSkyeCorrupter.deathCorruptor(deathInputFile, deathOutputFile, deathLogFile, lookupFilesDir, deterministic, seed,
                               proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                               numberOfModificationsPerRecord, recordLevelProportion)
print "Death conclude: " + str(time.time())
print "Death Duration: " + str(time.time()-st)