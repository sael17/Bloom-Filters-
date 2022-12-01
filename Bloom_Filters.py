import sys 
import csv


# we specify the newline keyword argument and pass an empty string
# this is because depending on the system, strings may end with a newline,
# This technique makes sure that that the csv module works correctly accross all platforms
if len(sys.argv) > 1:
    csv_file = open(sys.argv[1],newline="")
    reader = csv.reader(csv_file)  # the first line is the header
    header = next(reader)  # skip the header (first line)

