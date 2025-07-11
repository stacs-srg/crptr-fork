# Reference guide for log-files
When run, the [example population corruptor](../../src/main/python/populations_crptr/population_corruptor.py) outputs a log file into the results directory for the run.

## Output location
The log-file will be output at a location similar to:

```txt
results/default/2025-07-10T16-11-49-938/default2025-07-10T16-11-49-938.log
```

Where:
- `results` - the results directory
- `default` - the value set for `purpose` in the Config object (see [configuration guide](./configuration.md))
- `2025-07-10T16-11-49-938` - timestamp of crptr run

## Log-file contents
The log file consists of two key sections, the header and the changelog.

### Log-file header
The header, found at the top of each log-file contains details about the corruption parameters and proportions of attributes being corrupted. This will look similar to:

```txt
Used seed: 1752160310.2947462
Records to be corrupted: 334
Probability distribution for number of duplicates per record:
[(1, 0.0)]
Distribution of number of original records with certain number of duplicates:
 Number of records with 1 duplicates: 334
```

### Changelog
The remainder of the log file consists of descriptions of changes made to the dataset during the corruption process. This will feature a number of blocks similar to this:
```txt
Generating 1 modified (duplicate) records for record "rec-271-org"
  Generate identifier for duplicate record based on "rec-271-org": rec-271-dup-0
  Selected attribute for modification: crptr-record
    Selected corruptor: Swap Attributes
      Original record value: '1112', 'Natalie', 'Jones', '', 'S', 'F', '', '', '9', 'JANUARY', '1891', "1 Baron's Court, Pulteneytown, Wick", '3', 'Harry', 'Jones', '', '', 'Sarah', 'Drake', '', '', 'J20.91', '', '', 'SYNTHETIC DATA PRODUCED USING VALIPOP', '1112', '', '1112', '740', '741', '', '1112', '226', '741', '740', '', '', 'NA', 'original'
      Modified record value: '1112', 'Natalie', 'Jones', '', 'S', 'F', '', '', '9', 'JANUARY', '1891', "1 Baron's Court, Pulteneytown, Wick", '3', 'Jones', 'Harry', '', '', 'Sarah', 'Drake', '', '', 'J20.91', '', '', 'SYNTHETIC DATA PRODUCED USING VALIPOP', '1112', '', '1112', '740', '741', '', '1112', '226', '741', '740', '', '', 'NA', 'original'
  Selected attribute for modification: age at death
    Selected corruptor: Missing value
      Original attribute value: '3'
      Modified attribute value: 'missing'
  Selected attribute for modification: forename(s) of deceased
    Selected corruptor: Phonetic value
      Original attribute value: 'Natalie'
      Modified attribute value: 'Natali'
  Selected attribute for modification: surname of deceased
    Selected corruptor: Missing value
      Original attribute value: 'Jones'
      Modified attribute value: 'missing'
Original record:
  ['1112', 'Natalie', 'Jones', '', 'S', 'F', '', '', '9', 'JANUARY', '1891', "1 Baron's Court, Pulteneytown, Wick", '3', 'Harry', 'Jones', '', '', 'Sarah', 'Drake', '', '', 'J20.91', '', '', 'SYNTHETIC DATA PRODUCED USING VALIPOP', '1112', '', '1112', '740', '741', '', '1112', '226', '741', '740', '', '', 'NA', 'original']
Record with 4 modified attributes (1 in forename(s) of deceased, 1 in surname of deceased, 1 in age at death, 1 in crptr-record,):
  ['1112', 'Natali', 'missing', '', 'S', 'F', '', '', '9', 'JANUARY', '1891', "1 Baron's Court, Pulteneytown, Wick", 'missing', 'Jones', 'Harry', '', '', 'Sarah', 'Drake', '', '', 'J20.91', '', '', 'SYNTHETIC DATA PRODUCED USING VALIPOP', '1112', '', '1112', '740', '741', '', '1112', '226', '741', '740', '', '', 'NA', 'original']
1 of 334 duplicate records generated so far
```
