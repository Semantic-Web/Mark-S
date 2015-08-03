import shutil, csv, datetime, operator

# Assign date of Sunday being analyzed for Garmin data
YEAR = 2015
MONTH = 7
DAY = 19
# Set format for integrated file
itg_fieldnames = ['date', 'event', 'value']

# Copy timestamp file as starting point for integrated file
shutil.copyfile('TIMESTAMPS_ALL_EVENTS_2015_07_19.csv', 'HEALTH_DATA_2015_07_19.csv')

# Create file writer for integrated file
itg_file = open('HEALTH_DATA_2015_07_19.csv', 'a')
itg_writer = csv.DictWriter(itg_file, fieldnames=itg_fieldnames)

# Read Garmin data, skipping extraneous first line, write to integrated file format
with open('WELLNESS_TOTAL_STEPS_2015_07_19_WEEK.csv', 'r') as steps:
    steps.readline()
    steps_reader = csv.DictReader(steps)
    steps_fieldnames = steps_reader.fieldnames
    date_iter = 0
    for row in steps_reader:
        itg_writer.writerow({'date': str(datetime.datetime(YEAR, MONTH, DAY+date_iter)), 'event': 'steps', 'value': row['Actual']})
        date_iter += 1

# Close integrated file
itg_file.close()

# Sort integrated file on 'date' field, descending order
sort_file_read = open('HEALTH_DATA_2015_07_19.csv', 'r')
sort_file_reader = csv.reader(sort_file_read, delimiter=",")
sort_header = sort_file_reader.next()
sorted_rows = sorted(sort_file_reader, key=operator.itemgetter(0))
itg_file.close()
sort_file_write = open('HEALTH_DATA_2015_07_19.csv', 'w')
sort_file_writer = csv.writer(sort_file_write, delimiter=",")
sort_file_writer.writerow(sort_header)
sort_file_writer.writerows(sorted_rows)
sort_file_write.close()
