'''
Unit test equation balencer
Created on Jun 23, 2016
@author: Lance Pereira
'''

import unittest
from equationBalencer import Equation
import numpy


raw_equation = 'Na3PO4 + CaCl2 = Ca3(PO4)2 + NaCl'
equation = Equation(raw_equation.replace(" ",""))
equation.solve()

class EquationBalencerTest(unittest.TestCase):
   
    def test_compoundsAreSplit(self):
        #self.equation = Equation('Na3PO4 + CaCl2 = Ca3(PO4)2 + NaCl')
        #self.equation = Equation('Na3PO4 + CaCl2 = Ca3(PO4)2 + NaCl')
        self.assertEqual(equation.reactants, "Na3PO4+CaCl2", msg = 'Compounds did not split properly')
        self.assertEqual(equation.products, "Ca3(PO4)2+NaCl",msg = 'Compounds did not split properly')
        
    def test_reactantsAndProdcutsSplit(self):
        self.assertEqual(equation.reactantList, ["Na3PO4","CaCl2"], msg = 'Reactants did not split properly')
        self.assertEqual(equation.productList, ["Ca3(PO4)2","NaCl"], msg = 'Products did not split properly')
        
    def test_compoundsSplitProperly(self):
        self.assertEqual(equation.compoundList[0].name, "Na3PO4", msg = "Name Na3PO4 does not match up for first compound")
        self.assertTrue(equation.compoundList[0].isReactant, msg = "Na3PO4 is not considred reactant")
        
        self.assertEqual(equation.compoundList[1].name, "CaCl2", msg = "Name CaCl2 does not match up for first compound")
        self.assertTrue(equation.compoundList[1].isReactant, msg = "CaCl2 is not considred reactant")
        
        self.assertEqual(equation.compoundList[2].name, "Ca3(PO4)2", msg = "Name Ca3(PO4)2 does not match up for first compound")
        self.assertFalse(equation.compoundList[2].isReactant, msg = "Ca3(PO4)2 is not considred product")
        
        self.assertEqual(equation.compoundList[3].name, "NaCl", msg = "Name NaCl does not match up for first compound")
        self.assertFalse(equation.compoundList[3].isReactant, msg = "NaCl is not considred product")
    
    def test_elementsSplitProperly(self):
        Dict_Na3PO4 = {'Na':3,'P':1,"O":4}
        self.assertDictEqual(equation.compoundList[0].ElementsDict, Dict_Na3PO4, msg = "Na3PO4 dictionary not equal")
        Dict_CaCl2 = {'Ca':1,'Cl':2}
        self.assertDictEqual(equation.compoundList[1].ElementsDict, Dict_CaCl2, msg = "CaCl2 dictionary not equal")
        Dict_Ca3PO42 = {'Ca':3,'P':2,"O":8}
        self.assertDictEqual(equation.compoundList[2].ElementsDict, Dict_Ca3PO42, msg = "Ca3(PO4)2 dictionary not equal")
        Dict_NaCl = {'Na':1,'Cl':1}
        self.assertDictEqual(equation.compoundList[3].ElementsDict, Dict_NaCl, msg = "NaCl dictionary not equal")
        
    def test_allElements(self):
        self.assertListEqual(equation.allElements, ['Ca','Cl','Na','O','P'],msg = 'Elements list is not equal')
        
    def test_createMatrix(self):
        testCompoundMatrix = numpy.matrix([[0,1,-3],[0,2,0],[3,0,0],[4,0,-8],[1,0,-2]]) 
        self.assertFalse((numpy.subtract(testCompoundMatrix,equation.CompoundMatrix)).any(), msg = "Compound Matrix not equal")
        testProductMatrix = numpy.matrix([[0],[1],[1],[0],[0]]) 
        self.assertFalse((numpy.subtract(testProductMatrix,equation.ProductMatrix)).any(), msg = "Product Matrix not equal")
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()