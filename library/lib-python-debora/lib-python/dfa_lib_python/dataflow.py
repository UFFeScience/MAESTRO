import requests
import os
from .ProvenanceObject import ProvenanceObject
from .transformation import Transformation

from .attribute import Attribute
from .attribute_type import AttributeType
from .set import Set
from .set_type import SetType

dfa_url = os.environ.get('DFA_URL', "http://localhost:22000/")


class Dataflow(ProvenanceObject):
    """
    This class defines a dataflow.
    
    Attributes:
        - tag (str): Dataflow tag.
        - transformations (list, optional): Dataflow transformations.
    """
    def __init__(self, tag, hyperparameters=False, transformations=[]):
        ProvenanceObject.__init__(self, tag)
        self.transformations = transformations
        self.hyperparameters = hyperparameters

    @property
    def transformations(self):
        """Get or set the dataflow transformations."""
        return self._transformations

    @transformations.setter
    def transformations(self, transformations):
        assert isinstance(transformations, list), \
            "The Transformations must be in a list."
        result = []
        for transformation in transformations:
            assert isinstance(transformation, Transformation), \
                "The Transformation must be valid."
            result.append(transformation.get_specification())
        self._transformations = result

    def add_transformation(self, transformation):
        """ Add a transformation to the dataflow.

        Args:
            transformation (:obj:`Transformation`): A dataflow transformation.
        """
        assert isinstance(transformation, Transformation), \
            "The parameter must must be a transformation."
        self._transformations.append(transformation.get_specification())

    @property
    def hyperparameters(self):
        return self._hyperparameters

    @hyperparameters.setter
    def hyperparameters(self, hyperparameters):
        if(hyperparameters == True):
            assert isinstance(hyperparameters, bool), \
                "The parameter must must be a user."   
            tf1 = Transformation("TrainingModel")
            tf1_input = Set("iTrainingModel", SetType.INPUT, 
                [Attribute("OPTIMIZER_NAME", AttributeType.TEXT), 
                Attribute("LEARNING_RATE", AttributeType.NUMERIC),
                Attribute("NUM_EPOCHS", AttributeType.NUMERIC),
                Attribute("NUM_LAYERS", AttributeType.NUMERIC)])
            tf1_output = Set("oTrainingModel", SetType.OUTPUT, 
                [Attribute("TIMESTAMP", AttributeType.TEXT), 
                Attribute("ELAPSED_TIME", AttributeType.TEXT),
                Attribute("LOSS", AttributeType.NUMERIC),
                Attribute("ACCURACY", AttributeType.NUMERIC),
                Attribute("VAL_LOSS", AttributeType.NUMERIC),
                Attribute("VAL_ACCURACY", AttributeType.NUMERIC),                
                Attribute("EPOCH", AttributeType.NUMERIC)])
            tf1.set_sets([tf1_input, tf1_output])
            self.add_transformation(tf1)

            tf2 = Transformation("Adaptation")
            tf2_input = Set("iAdaptation", SetType.INPUT, 
                [Attribute("EPOCHS_DROP", AttributeType.NUMERIC), 
                Attribute("DROP_N", AttributeType.NUMERIC),
                Attribute("INITIAL_LRATE", AttributeType.NUMERIC)])
            tf2_output = Set("oAdaptation", SetType.OUTPUT, 
                [Attribute("NEW_LRATE", AttributeType.NUMERIC),
                Attribute("TIMESTAMP", AttributeType.TEXT),
                Attribute("EPOCH_ID", AttributeType.NUMERIC),
                Attribute("ADAPTATION_ID", AttributeType.NUMERIC)])
            tf1_output.set_type(SetType.INPUT)
            tf1_output.dependency=tf1._tag
            tf2.set_sets([tf1_output, tf2_input, tf2_output])
            self.add_transformation(tf2)     
            
            tf3 = Transformation("TestingModel")
            tf3_output = Set("oTestingModel", SetType.OUTPUT, 
                [Attribute("LOSS", AttributeType.NUMERIC),
                Attribute("ACCURACY", AttributeType.NUMERIC)])
            tf1_output.set_type(SetType.INPUT)
            tf1_output.dependency=tf1._tag
            tf3.set_sets([tf1_output, tf3_output])
            self.add_transformation(tf3)     

    def save(self):
        """ Send a post request to the Dataflow Analyzer API to store
            the dataflow.
        """
        url = dfa_url + '/pde/dataflow/json'
        r = requests.post(url, json=self.get_specification())  
        print(r.status_code)
