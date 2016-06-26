'''
equation balencer
Created on Jun 23, 2016
@author: Lance Pereira
'''
import re
import numpy

class Equation():
    '''
    Takes an equation, splits it into reactants and products,
    splits thoose compounds into elements, and then treats each 
    element as a linear equation which it uses matricies to solve for
    '''
    
    def __init__(self,equation):
        equation = equation.replace(" ","")
        (self.reactants,self.products) = equation.split("=")
        self.reactantList = (self.reactants).split("+")
        self.productList = (self.products).split("+")
        self.compoundList = self.reactantList + self.productList
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
        
        
    def createMatrix(self):
        '''
        Creates a matrix which then uses numpy to solve
        '''
        self.CompoundMatrix = numpy.zeros((len(self.allElements),len(self.compoundList)-1))
        self.ProductMatrix = numpy.zeros((len(self.allElements),1))
        #print(CompoundMatrix)
        for compoundIndexes in range(len(self.compoundList)):
            compound = self.compoundList[compoundIndexes]
            compoundValueRow = []
            for element in self.allElements:
                if element not in compound.ElementsDict:
                    value = 0
                else:
                    value = compound.ElementsDict[element]
                    if not compound.isReactant and compoundIndexes != len(self.compoundList)-1:
                        value *= -1
                compoundValueRow.append(value)
            if compoundIndexes != len(self.compoundList)-1:
                self.CompoundMatrix[:,compoundIndexes] = compoundValueRow
            else:
                self.ProductMatrix[:,0] = compoundValueRow
        
        #print(self.CompoundMatrix)
        #print(self.ProductMatrix)
        self.answerMatrix = numpy.linalg.solve(self.CompoundMatrix, self.ProductMatrix)
        print (self.answerMatrix)
                
        

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
        
    
    
