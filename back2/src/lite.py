import tensorflow as tf

class LitePredictionModel:


    def __init__(self, path):
        self.interpreter = tf.lite.Interpreter(model_path=path)
        self.interpreter.allocate_tensors()
        self.__input__ = self.interpreter.get_input_details()
        self.__output__ = self.interpreter.get_output_details()


    def predict(self, image):
        self.interpreter.set_tensor(self.__input__[0]['index'], image)
        self.interpreter.invoke()
        pred = self.interpreter.get_tensor(self.__output__[0]['index'])
        return pred
