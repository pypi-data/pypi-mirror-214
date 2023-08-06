import numpy as np

class hypbench:
    '''
    The features class provides methods for machine learning features analysis
    '''
    def __init__(self, name):
        """
        Instantiate a class instance
        
        :param name: object's name
        :type name: string
        """
        self.name = name

    def example_fun(self, data):
        """
        Apply the example function to the given data
        
        :param data: An object containing the training data 
        :type number: string
    
        :return: None
        :rtype: NoneType
        """
        rubbish = data