import keras
import os

from app.shape_inputs import available_functions

# Model for storing information about available models, which are obtained from a JSON file upon the FastAPI application's startup
class AvailableModel:
    name: str       # Human-readable model name
    description: str    # Human-readable description
    endpoint_extension: str     # Extension to use for calling the prediction endpoint or obtaining its diagram
    model_object: str           # Keras model object that is loaded upon startup
    model_diagram_path: str     # Path to the model_diagram; may be an empty string
    input_shaping_func: function    # Input shaping function to use when shaping inputs before prediction

    def __init__(self, name, endpoint_extension, obj_path, input_shaping, description='', diagram_path=''):
        self.name = name
        self.endpoint_extension = endpoint_extension
        self.description = description

        # Test if the model object's path exists; raise exception if not; load the model otherwise
        if not os.path.exists(obj_path):
            raise Exception(f"Received invalid path for model object, {name}: {obj_path}\nMake sure the file exists and the path is relative to the 'app' directory.")
        self.model_object = keras.models.load_model(obj_path)

        # Test if the model diagram's path exists, if it is not empty
        if not os.path.exists(obj_path) and diagram_path != '':
            raise Exception(f"Received invalid path for model diagram, {name}: {diagram_path}\nMake sure the file exists and the path is relative to the 'app' directory. An empty path is allowed.")
        self.model_diagram_path = diagram_path

        # Test the validity of the input-shaping function
        if input_shaping not in available_functions:
            raise Exception(f"Input shaping function for the model named '{name}' is not valid.\nReceived '{input_shaping}'. Valid inputs are {list(available_functions.keys())}.")
        self.input_shaping_func = available_functions[input_shaping]

    # Function for obtaining predictions from the model
    def make_prediction(self, pixelValues):
        data = self.input_shaping_func(pixelValues)
        return self.model_object.predict(data, verbose=0)

    # Function for obtaining a JSON-serializable dictionary of model information that can be made available to API clients
    def get_client_API_info(self):
        return {"Name" : self.name, \
                "Description" : self.description, \
                "Endpoint Extension" : self.endpoint_extension}
