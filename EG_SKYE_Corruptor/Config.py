import EGSkyeCorrupter

# Files
birthInputFile = "/Users/tsd4/OneDrive/cs/PhD/code/population-model/src/main/resources/valipop/results/batch39-job36-sc500k/20180604-121800:537/records/birth_10k.csv"
birthOutputFile = "/Users/tsd4/OneDrive/cs/PhD/code/population-model/src/main/resources/valipop/results/batch39-job36-sc500k/20180604-121800:537/records/birth_10k_corrupted.csv"
birthLogFile = "/Users/tsd4/OneDrive/cs/PhD/code/population-model/src/main/resources/valipop/results/batch39-job36-sc500k/20180604-121800:537/records/birth_10k_corruption_log.txt"

deathInputFile = "/Users/tsd4/OneDrive/cs/PhD/code/population-model/src/main/resources/valipop/results/batch39-job36-sc500k/20180604-121800:537/records/death_10k.csv"
deathOutputFile = "/Users/tsd4/OneDrive/cs/PhD/code/population-model/src/main/resources/valipop/results/batch39-job36-sc500k/20180604-121800:537/records/death_10k_corrupted.csv"
deathLogFile = "/Users/tsd4/OneDrive/cs/PhD/code/population-model/src/main/resources/valipop/results/batch39-job36-sc500k/20180604-121800:537/records/death_10k_corruption_log.txt"

lookupFilesDir = "/Users/tsd4/OneDrive/cs/PhD/repos/crptr-fork/lookup-files"

# Determinism
deterministic = True
seed = 12345

# Corruption setup
proportionOfRecordsToCorrupt = 0.1
maxModificationsPerAttribute = 2
numberOfModificationsPerRecord = 4
recordLevelProportion = 0.25

EGSkyeCorrupter.birthCorruptor(birthInputFile, birthOutputFile, birthLogFile, lookupFilesDir, deterministic, seed,
                               proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                               numberOfModificationsPerRecord, recordLevelProportion)

EGSkyeCorrupter.deathCorruptor(deathInputFile, deathOutputFile, deathLogFile, lookupFilesDir, deterministic, seed,
                               proportionOfRecordsToCorrupt, maxModificationsPerAttribute,
                               numberOfModificationsPerRecord, recordLevelProportion)
