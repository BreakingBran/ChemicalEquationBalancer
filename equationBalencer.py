'''
equation balencer, that balences your chemical or math equations
Created on Jun 23, 2016
@author: Lance Pereira
'''
import re
import numpy
from itertools import chain
from fractions import  gcd
from functools import reduce
from builtins import max


class Equation():
    '''
    Takes an equation, splits it into reactants and products,
    splits thoose compounds into elements, and then treats each 
    element as a linear equation which it uses matricies to solve for
    '''
    
    def __init__(self,equation,doSolve = True):
        equation = equation.replace(" ","")
        self.equation = equation
        (self.reactants,self.products) = equation.split("=")
        self.reactantList = (self.reactants).split("+")
        self.productList = (self.products).split("+")
        self.compoundList = self.reactantList + self.productList
        self.lenCompoundList = len(self.compoundList)
        #Makes each compound an object
        self.compoundList = [ Compound(compound,True) if self.compoundList.index(compound) < len(self.reactantList) else Compound(compound,False) for compound in self.compoundList]
        self.balencedEquation = "Not solved yet"
        if doSolve: self.solve()
        
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
            newElementsList = [x for x in newElementsList if x not in self.allElements]
            self.allElements = self.allElements + newElementsList
        self.allElements.sort()
        #print (self.allElements)
        self.createMatrix()
        self.makeWhole()
        self.outputAnswer()
        
        
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
        
        factor = max(self.answerList)
        tempAnswerList = self.answerList
        
        if factor != 1: 
            tempAnswerList = [x/factor for x in self.answerList]
        
        self.denominatorList = [0]*self.lenCompoundList
        denominatorsMultiplied =1
        #Finds the denominators of all the ratio numbers
        for i,ratioNumber in enumerate(tempAnswerList):
            self.denominatorList[i] = (1/ratioNumber)
            denominatorsMultiplied *= self.denominatorList[i]
            
        #print(self.denominatorList, factor)
        #Puts all the numbers over the same denominator
        self.multipliedDenominatorList = [round(denominatorsMultiplied/x,6)*factor for x in self.denominatorList]
        #print(self.multipliedDenominatorList) #test_equation1: [12.0, 18.0, 6.0, 36.0]
        
        #Find the greatest common factor 
        greatestCommonFactor = reduce(gcd,self.multipliedDenominatorList)
        #print(greatestCommonFactor) #test_equation1: 6.0
        
        #Divides all the ratios by the greatest common factor
        self.answerList = [round(x/greatestCommonFactor) for x in self.multipliedDenominatorList]
        #print(self.answerList) #test_equation1: [2, 3, 1, 6]
            
    def outputAnswer(self):
        '''
        Pairs up the ratios with the numbers and creates
        a readable output for the user
        '''
        balencedEquation = ''
        for i,compounds in enumerate(self.compoundList):
            name = compounds.name
            #Pairs ratio and compound
            nameWithNmber = str(self.answerList[i]) + " " + name
            #Matches the appropriate connector (+ or =) depending on whats on either side
            if i == 0:
                balencedEquation = nameWithNmber
            elif (compounds.isReactant and self.compoundList[i-1].isReactant) or (not compounds.isReactant and not self.compoundList[i-1].isReactant):
                balencedEquation = balencedEquation + " + " + nameWithNmber
            elif not compounds.isReactant and self.compoundList[i-1].isReactant:
                balencedEquation = balencedEquation + " = " + nameWithNmber
        self.balencedEquation = balencedEquation
        #print (balencedEquation)
        return balencedEquation
    
    def __repr__(self):
        return self.balencedEquation
            

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
        
def main():
    done = False
    print("To use the equation solver, input the equation without any coefficants. Exmp(Na3PO4 + CaCl2 = Ca3(PO4)2 + NaCl).")
    print("To exit,type in exit.")
    while not done:
        raw_equation = input("\nWhat is your Equation: ")
        checkExit = raw_equation
        if (checkExit.strip()).lower() == "exit":
            done = True
            break
        equation = Equation(raw_equation)
        print ('Answer is: ',equation)
    print("\nThank you for using Chemical Equation Solver by Lance, please come again.")
    
if __name__ == "__main__":
    main()
    
