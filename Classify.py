from Utilities import *
from Train import *

class Classify():

    def __init__(self,location,train):
        self.file={}
        self.data=train.data
        self.location=location
        self.prob=train.prob
        self.nums=train.nums
        self.bag=train.bag
        self.amount=train.amount_words
        self.acc={}
        self.utils=Utilities()

    """
    classify by reading the test file,calc the probability of every line, 
    choosing the bigger probability and writing it to a txt file
    """
    def classify(self):
        try:
            self.file = self.utils.readFile(self.location + '/' + 'test.csv')
            dic=self.calc_probability()
            self.calc_acc(dic)
            self.utils.writeToText(self.location,dic,self.acc)
            return True
        except IOError:
            return False

    """
    calc the probability for every line
    """
    def calc_probability(self):
        dic = {}
        count = 0
        for label in self.data:
            if self.data[label] != 'NUMERIC' and label != 'class':
                for val in self.file:
                    if label == val:
                        for i in self.file[val]:
                            if i in self.data[label]:
                                if not count in dic:
                                    dic[count] = {}
                                for j in self.prob[label]:
                                    for k in self.amount['class']:
                                        if j == i:
                                            if not k in dic[count]:
                                                dic[count][k]=1.0
                                            dic[count][k] *= self.prob[label][j][k]
                                count += 1
                        count = 0
            elif self.data[label] == 'NUMERIC' and label != 'class':
                for val in self.file:
                    if label == val:
                        for i in self.file[val]:
                            if i in self.data[label]:
                                if not count in dic:
                                    dic[count] = {}
                                for j in self.nums[label]:
                                    for k in self.amount:
                                        if i > j and i < self.nums[label][len(self.nums[label]) - 1]:
                                            dic[count][k] *= self.nums[label][j][k]
                                            break
                                        elif i > j and len(self.nums[label]) - 1 == j:
                                            dic[count][k] *= self.nums[label][j][k]
                                            break
                                count += 1
                        count = 0
        newDic = []
        for i in dic:
            count = 0
            for k in self.amount['class']:
                dic[i][k] *= (self.prob['class'][k])
            for k in self.amount['class']:
               if count==0:
                   big=dic[i][k]
                   word=k
                   count+=1
               elif big<dic[i][k]:
                   big=dic[i][k]
                   word=k
            newDic.append((i + 1, word))
        return newDic

    """
    calc the accurtacy of the prediction
    """
    def calc_acc(self,dic):
        num = 0.0
        for i in range(len(dic)):
            if dic[i][1] == self.file['class'][i]:
                num += 1
        self.acc = (num / len(dic)) * 100