from Utilities import *

class Train():


    def __init__(self,location):
        self.data=''
        self.file={}
        self.location=location
        self.prob = {}
        self.nums = {}
        self.bag = {}
        self.amount_words={}
        self.utils=Utilities()

    """
    train the code by reading the files,marking missing data,
    calc the avg value and the word that shows up the most,complete missing values and write to the file
    """
    def train(self):
        try:
            self.data=self.utils.readStructe(self.location + '/' + 'Structure.txt')
            self.file = self.utils.readFile(self.location + '/' + 'train.csv')
            self.markNullTrain()
            self.completeMissing()
            self.utils.writeToCsvFile(self.location,self.file)
            return True
        except IOError:
            return False

    """
    mark missing values if numeric -1 else null
    """
    def markNullTrain(self):
        for i in self.data:
            if self.data[i] == "NUMERIC":
                for j in self.file:
                    if i == j:
                        list1 = self.file.get(j)
                        for s in range(len(list1)):
                            if type(list1[s]) == str:
                                if list1[s].isdigit():
                                    list1[s] = int(list1[s])
                                    if list1[s] <= 0:
                                        list1[s] = -1
                                else:
                                    list1[s] = -1
                            elif type(list1[s]) == int and list1[s] <= 0:
                                list1[s] = -1
                    else:
                        list1 = self.file.get(j)
                        for s in range(len(list1)):
                            if type(list1[s]) == str:
                                if list1[s] == '':
                                    list1[s] = "null"
                                if list1[s] in self.data[i]:
                                    list1[s] = "null"

    """
    count the apperance of every numeric value
    """
    def avgValues(self):
        avg = {}
        # run on dic for labels type
        for label in self.data:
            # check if type numeric
            if self.data[label] == 'NUMERIC':
                # get array size
                avg[label] = [len(self.file[label])]
                # run on train array
                for val in self.file:
                    # check if its the same label
                    if val == label:
                        # add sum counter
                        avg[label].append(0)
                        # run on the values and sum them if its not an empty value
                        for i in self.file[val]:
                            if i != -1:
                                avg[label][1] += i
        # return dic
        return avg

    """
    calc the avg of every attribute
    """
    def calcAvg(self):
        avg = self.avgValues()
        for arr in avg:
            size = avg[arr][0]
            count = avg[arr][1]
            avg[arr] = count / size
        return avg

    """
    count the amount of every word 
    """
    def bagOfWords(self):
        bag={}
        for label in self.data:
            if self.data[label] != 'NUMERIC':
                bag[label] = {}
                for val in self.file:
                    if val == label:
                        for i in range(len(self.file[val])):
                            self.file[val][i] = self.file[val][i].lower()
                        for i in self.file[val]:
                            if i in self.data[label]:
                                if not i in bag[label]:
                                    bag[label][i] = 0
                                bag[label][i] += 1
        return bag

    """
    check whice word shows up the most
    """
    def getBigWord(self):
        self.amount_words=self.bagOfWords()
        bag = self.bagOfWords()
        word = None
        num = 0
        for label in bag:
            for w in bag[label]:
                if num < bag[label][w]:
                    num = bag[label][w]
                    word = w
            bag[label] = word
            num = 0
        return bag

    """
    complete missing values
    """
    def completeMissing(self):
        avg = self.calcAvg()
        bag = self.getBigWord()
        for label in self.data:
            if self.data[label] == 'NUMERIC':
                for val in self.file:
                    if val == label:
                        for i in range(len(self.file[val])):
                            if self.file[val][i] == -1:
                                self.file[val][i] = avg[label]
            else:
                for val in self.file:
                    if val == label:
                        for i in range(len(self.file[val])):
                            if self.file[val][i] == 'null':
                                # bag is the word that has the biggest count
                                self.file[val][i] = bag[label]

    """
       add all the numeric values to a list
       """

    def getNumeric(self):
        nums = []
        for label in self.data:
            if self.data[label] == 'NUMERIC':
                for val in self.file:
                    if val == label:
                        for i in range(len(self.file[val])):
                            nums.append(self.file[val][i])
        return nums

    """
    divide all the numeric values to bins
    """
    def divideBins(self, bins):
        l = list(set(self.getNumeric()))
        l.sort()
        bins = int(bins)
        dic = {}
        size = len(l)
        min = l[0]
        max = l[size - 1]
        space = float(size) / bins
        for i in range(bins):
            dic[min + space] = []
            for j in l:
                if j < min + space and j > min:
                    dic[min + space].append(j)
            if min + space <= max:
                min += space
        return dic

    """
    calc the probablity of class
    """
    def probability_class(self):
        self.bag={'class':{'total': len(self.file['class'])}}
        for val in self.file['class']:
            if not val in self.bag['class']:
                self.bag['class'][val] = 0.0
            self.bag['class'][val]+=1
        self.prob['class']={}
        for i in self.amount_words['class']:
            #laplas
            self.prob['class'][i] =(self.bag['class'][i] + 1) / (self.bag['class']['total'] + len(self.prob['class']))

    """
    calc the probabilty of the numeric values
    """
    def probability_num(self):
        dic = {}
        for label in self.data:
            if self.data[label] == 'NUMERIC':
                self.nums[label] = {}
                for val in self.file:
                    if val == label:
                        for i in range(len(self.file[val])):
                            if not self.file[val][i] in self.nums[label]:
                                self.nums[label][self.file[val][i]] = {}
                            if not self.file['class'][i] in self.nums[label][self.file[val][i]]:
                                self.nums[label][self.file[val][i]][self.file['class'][i]] = 0.0
                            self.nums[label][self.file[val][i]][self.file['class'][i]] += 1
                        dic[val] = {}
                        for i in self.nums[val]:
                            dic[val][i]={}
                            for j in self.amount_words['class']:
                                if not j in self.nums[val][i]:
                                    self.nums[label][i][j]=0.0
                                dic[val][i][j] = (self.nums[label][i][j]) / (self.bag['class'][j])

        self.nums = dic

    """
    calc the probability by bins
    """
    def prob_by_bins(self, bins):
        dic = {}
        for i in bins:
            for val in self.nums:
                for j in self.nums[val]:
                    if len(bins[i]) != 0:
                        if j >= bins[i][0] and j <= bins[i][len(bins[i]) - 1]:
                            if not i in dic:
                                dic[i] = {}
                            for k in self.amount_words['class']:
                                if self.nums[val][j][k] > 0.0:
                                    if not k in dic[i]:
                                        dic[i][k]=1.0
                                    dic[i][k] *= self.nums[val][j][k]

            for j in self.amount_words['class']:
                if i in dic:
                    #laplas
                    dic[i][j] = (dic[i][j] + 1) / (self.bag['class'][j] + len(bins))
        self.nums = dic


    """
    calc the probability of all the string values
    """
    def probability_str(self):
        dic = {}
        self.probability_class()
        for label in self.data:
            if self.data[label] != 'NUMERIC':
                if label != 'class':
                    self.prob[label] = {}
                    for val in self.file:
                        if val == label and val != 'class':
                            for i in range(len(self.file[val])) :
                                if not self.file[val][i] in self.prob[label]:
                                    self.prob[label][self.file[val][i]] = {}
                                if not self.file['class'][i] in self.prob[label][self.file[val][i]]:
                                    self.prob[label][self.file[val][i]][self.file['class'][i]]=0.0
                                self.prob[label][self.file[val][i]][self.file['class'][i]] += 1

                            dic[val] = {}
                            for i in self.prob[val]:
                                dic[val][i] = {}
                                for j in self.amount_words['class']:
                                    #laplas
                                    dic[val][i][j]=(self.prob[label][i][j] + 1) / (self.bag['class'][j] + len(self.prob[label]))
        self.prob = dic
