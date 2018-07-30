import csv
from collections import defaultdict

class Utilities():

    def __init__(self):
        self.header=None

    """
    read the structure file 
    """
    def readStructe(self, name):
        data={}
        fileStruct = open(name, 'r')
        for line in fileStruct:
            k = line.split()
            data[k[1]] = k[2]
        fileStruct.close()
        return data

    """
    read the csv file to a dictionary that every key holds a list of values
    """
    def readFile(self, name):
        dataRows = csv.reader(open(name, 'r'), delimiter=',')
        # Read the column names from the first line of the file
        self.header = dataRows.next()
        # Create dictionary of columns as list
        dic = defaultdict(list)
        for row in dataRows:
            for index, cell in enumerate(row):
                columnName = self.header[index]
                dic[columnName].append(cell)
        return dic

    """
    write to csv file
    """
    def writeToCsvFile(self,location,file):
        with open(location + '/' + 'train.csv', 'w') as f:
            f.truncate()
            thewriter = csv.writer(f)
            thewriter.writerow(list(file.keys()))
            thewriter.writerows(zip(*file.values()))

    """
    write to txt file
    """
    def writeToText(self,location,list_of_tuples,acc):
        f = open(location + '/' + 'output.txt', 'w')
        for t in list_of_tuples:
            line = ' '.join(str(x) for x in t)
            f.write(line + '\n')
        f.write('accurtacy: ' + str(acc));
        f.close()

    """
    get header
    """
    def getHeader(self):
        return self.header
