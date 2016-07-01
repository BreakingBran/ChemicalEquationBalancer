'''
equation balencer
Created on Jun 23, 2016
@author: Lance Pereira
'''
import re
import numpy
from itertools import chain
from fractions import  gcd
from functools import reduce


class Equation():
    '''
    Takes an equation, splits it into reactants and products,
    splits thoose compounds into elements, and then treats each 
    element as a linear equation which it uses matricies to solve for
    '''
    
    def __init__(self,equation):
        equation = equation.replace(" ","")
        self.equation = equation
        (self.reactants,self.products) = equation.split("=")
        self.reactantList = (self.reactants).split("+")
        self.productList = (self.products).split("+")
        self.compoundList = self.reactantList + self.productList
        self.lenCompoundList = len(self.compoundList)
        #Makes each compound an object
        self.compoundList = [ Compound(compound,True) if self.compoundList.index(compound) < len(self.reactantList) else Compound(compound,False) for compound in self.compoundList]
        
        
    def solve(self):
        '''
        Solves the linear system
        '''
        #Creates a list of all elements on one side of the reaction ()same on other side as well
        self.allElements = list(self.compoundList[0].ElementsDict.keys())
        for compound in range(1,len(self.reactantList)):
            compound = self.compoundList[compound]
            #print (compound)
            newElementsList = list(compound.ElementsDict.keys())
            newElementsList = [x if x not in self.allElements else None for x in newElementsList]
            self.allElements = self.allElements + newElementsList
        self.allElements.sort()
        #print (self.allElements)
        self.createMatrix()
        self.makeWhole()
        
        
    def createMatrix(self):
        '''
        Creates a matrix which then uses numpy to solve
        '''
        #Creates matricies filled with zeros to save memoeary
        self.CompoundMatrix = numpy.zeros((len(self.allElements),self.lenCompoundList-1))
        self.ProductMatrix = numpy.zeros((len(self.allElements),1))
        
        #print(CompoundMatrix)
        
        #Assigns the element numercal values into the matrix
        for compoundIndexes in range(self.lenCompoundList):
            compound = self.compoundList[compoundIndexes]
            compoundValueRow = []
            for element in self.allElements:
                #If the element is not in the compound, assigns it a value of 0
                if element not in compound.ElementsDict:
                    value = 0
                else:
                    value = compound.ElementsDict[element]
                    #For the products so that their values are negative
                    if not compound.isReactant and compoundIndexes != self.lenCompoundList-1:
                        value *= -1
                compoundValueRow.append(value)
            #Catches to see if the compound is the last one, which is given a by default a value of 1
            if compoundIndexes != self.lenCompoundList-1:
                self.CompoundMatrix[:,compoundIndexes] = compoundValueRow
            else:
                self.ProductMatrix[:,0] = compoundValueRow
        
        #print(self.CompoundMatrix)
        #print(self.ProductMatrix)
        
        #Solves for b in A.b = x, with some complicated math i don't understand
        self.answerList = numpy.linalg.lstsq(self.CompoundMatrix, self.ProductMatrix)[0]
        self.answerList = (self.answerList).tolist() 
        self.answerList = list(chain.from_iterable(self.answerList))
        #Add the 1 that we used to get the rest of the formula
        self.answerList.append(1)
        #print (self.answerMatrix)
        
        
    def makeWhole(self):
        '''
        Takes the decimal value matrix that was solved and turns it into whole numbers
        '''
        self.denominatorList = [0]*self.lenCompoundList
        denominatorsMultiplied =1
        #Dinds the denominators of all the 
        for i,ratioNumber in enumerate(self.answerList):
            self.denominatorList[i] = (1/ratioNumber)
            denominatorsMultiplied *= self.denominatorList[i]
            
        self.multipliedDenominatorList = [round(denominatorsMultiplied/x,3) for x in self.denominatorList]
        print(self.multipliedDenominatorList)
        greatestCommonFactor = reduce(gcd,self.multipliedDenominatorList)
        print(greatestCommonFactor)
        self.answerList = [round(x/greatestCommonFactor) for x in self.multipliedDenominatorList]
        print(self.answerList)      
            
            
                
        

class Compound():
    '''
    Takes compounds, splits them into elements
    '''
    def __init__(self,compound,isReactant):
        self.name = compound
        self.isReactant = isReactant
        self.ElementsDict = {}
        self.elements()
        
        
    def elements(self):
        '''
        I'll be honest, I made this late at night one day and have no idea how it works, there's
        probabley some corner cases I missed, byut hey, have fun
        '''
        compound = self.name
        if re.search("\(", compound):
            elements = re.findall('[(]*[A-Z]+[a-z]*[1-9]*[)]*[1-9]*',compound)
        else:
            elements = re.findall('[(]*[A-Z][a-z]*[1-9]*[)]*[1-9]*',compound)
        #print(elements)
        for values in elements:
            factor = 1
            valueList = []
            if re.search('\(',values):
                #print(values)
                factor = re.findall('\)([1-9]+)',values)
                #print (factor)
                try:
                    factor = int(factor[0])
                except SyntaxError: 
                    print ('You used paranthesis without placing a subscript, add a subscript or remove the parenthis')
                elements2 = re.findall('[A-Z][a-z]*[1-9]*',values)
                values = elements2
                valueList = list(elements2)
            else:
                valueList.append(values)
            for items in valueList:
                letter = re.findall('[A-Z]+[a-z]*',items)
                number = (re.findall('[1-9]',items))
                if number == []:
                    number = factor
                else:
                    #print ('This is number',number)
                    number = int(number[0])
                    number *= factor
                #print (letter,number)
                self.ElementsDict[letter[0]] = number
                
        def __repr__(self):
            return self.name
        
        def __str__(self):
            return self.name
        
    
    
