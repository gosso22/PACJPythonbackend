import csv
import sys

if __name__ == "__main__":

    file_name = sys.argv[1]

    reader = csv.reader(open(file_name))

    for row in reader:

        for i in range(len(row)):

            print(row[i], "&", end="", flush=True)

        print(r" \\\hline")
       
        #print(row[0], "&", row[1], "&", row[2], "&", row[3], "&", row[4], r"\\\hline")
