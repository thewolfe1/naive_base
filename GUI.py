from Tkinter import *
import tkFileDialog
from tkMessageBox import *
from Train import *
from Classify import *

class GUI:

    def __init__(self):
        self.dic={'screen':Tk(),'path':"",'bins':0,'browse':None,'build':None,
                  'classify_btn':None,'directory_path':None,'discretization_bins':None,'train':None,'classify':None}
        self.dic['train']=Train('')
        self.setupScreen()
        self.createBrowse()
        self.createBuild()
        self.createClassify()
        self.createLabeles()
        self.createTextPath()
        self.createTextBins()

    """
    define screen settings
    """
    def setupScreen(self):
        self.dic['screen'].title("Naive Bayes Classifier")
        self.dic['screen'].geometry('500x350')
        self.dic['screen'].configure(background='snow2')

    """
    create browse button
    """
    def createBrowse(self):
        self.dic['browse'] = Button(self.dic['screen'], text="Browse", width=10, command=self.browsePath)
        self.dic['browse'].place(relx=0.9, rely=0.3, anchor=CENTER)

    """
    create build button
    """
    def createBuild(self):
        self.dic['build'] = Button(self.dic['screen'], text="Build", width=30, command=self.buildAction)
        self.dic['build'].place(relx=0.5, rely=0.6, anchor=CENTER)

    """
    create classify button
    """
    def createClassify(self):
        self.dic['classify_btn'] = Button(self.dic['screen'], text="Classify", width=30, command=self.classifyAction)
        self.dic['classify_btn'].place(relx=0.5, rely=0.73, anchor=CENTER)

    """
    create the descriptions 
    """
    def createLabeles(self):
        path_label = Label(self.dic['screen'], text="Directory Path")
        path_label.place(relx=0.13, rely=0.3, anchor=CENTER)
        bins_label = Label(self.dic['screen'], text="Discretization Bins")
        bins_label.place(relx=0.11, rely=0.4, anchor=CENTER)
        request_label = Label(self.dic['screen'], text="please press enter to save number of bins")
        request_label.place(relx=0.71, rely=0.4, anchor=CENTER)

    """
    create path text line
    """
    def createTextPath(self):
        self.dic['directory_path'] = Text(self.dic['screen'], width=35, height=1.3)
        self.dic['directory_path'].place(relx=0.5, rely=0.3, anchor=CENTER)

    """
    create bins text line
    """
    def createTextBins(self):
        self.dic['discretization_bins'] = Text(self.dic['screen'], width=15, height=1.3)
        self.dic['discretization_bins'].place(relx=0.34, rely=0.4, anchor=CENTER)
        self.dic['discretization_bins'].bind("<Return>", self.retrieveInput)

    """
    retrieve the bins input
    """
    def retrieveInput(self,event):
        bins_list=self.dic['discretization_bins'].get("1.0", END).split()
        self.dic['bins'] =int(bins_list[len(bins_list)-1])
    """
    run the screen
    """
    def run(self):
        self.dic['screen'].mainloop()

    """
    create path dialog
    """
    def browsePath(self):
        self.dic['path'] =tkFileDialog.askdirectory()
        self.dic['directory_path'].insert(END, self.dic['path'])
        self.dic['train']=Train(self.dic['path'])


    """
    activate all the function to train
    """
    def buildAction(self):
            self.dic['bins'] = int(self.dic['bins'])
            if self.dic['bins'] < 1:
                self.setError("bins error", "number of bins has not been selected or incorrect value")
            elif not self.dic['train'].train():
                self.setError("file error", "missing a file in directory")
            else:
                self.dic['bins_list'] = self.dic['train'].divideBins(self.getBins())
                self.dic['train'].probability_str()
                self.dic['train'].probability_class()
                self.dic['train'].probability_num()
                self.dic['train'].prob_by_bins(self.dic['bins_list'])
                self.dic['classify']=Classify(self.dic['path'],self.dic['train'])
                showinfo("complete", "Building classifier using train-set is done")

    """
    activate all the functions to classify
    """
    def classifyAction(self):
        if self.dic['classify']:
            if self.dic['classify'].classify():
                showinfo("complete", "classifieing using test-set is done,text file of the results is ready")
            else:
                self.setError("file error", "missing a file in directory")
        else:
            self.setError("wrong action","please train before you classify")
    """
    set error message
    """
    def setError(self,title,msg):
        showerror(title,msg)

    """
    get the path
    """
    def getPath(self):
        return self.dic['path']

    """
    get the bins
    """
    def getBins(self):
        return self.dic['bins']

g=GUI()
g.run()
