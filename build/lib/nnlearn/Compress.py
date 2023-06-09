
from nnlearn.Network import *
from matplotlib import pyplot as plt
from matplotlib import image
from threading import Thread
from multiprocessing import Process




def image_to_tab(image):
    shape = image.shape
    x = []
    y = []

    for row in range(shape[0]):
        for col in range(shape[1]):

            x.append([row/shape[0], col/shape[1]])
            y.append(image[row,col])

    x = np.array(x)
    y = np.array(y)
    
    return (x, y)



class nn_image_compresser():
    def __init__(self, hidden_layers = 2, layer_width = 7, activation = leaky_relu_activation_layer):

        assert hidden_layers >= 1, "must have at least 1 hidden layer"
        assert layer_width >= 1, "layer width must be at least 1"

        layers = (
            [input_layer(size = 2)] +
            
            [connected_layer(num_neurons = layer_width, prev_neurons = 2),
             activation(layer_width)] +
            
                

            [connected_layer(num_neurons = layer_width, prev_neurons = layer_width),
             activation(layer_width)] * (hidden_layers - 1) +
            
            
            [connected_layer(num_neurons = 1, prev_neurons = layer_width)]

            )
        
        self.network = test_net = network(layers)



    
    def fit(self, image, batch_size = None, epochs = 500, learn_coef = .2, verbose = True):

        x, y = image_to_tab(image)
    
        self.network.minibatch_fit(x, y, batch_size = batch_size, epochs = epochs, learn_coef = learn_coef, verbose = verbose)


    def simul_fit(self, image, batch_size = None, epochs = 500, learn_coef = .2, threads = 3):

        workers = []

        for i in range(threads):

            thread = Process( target = self.fit(image, batch_size = batch_size, epochs = epochs, verbose = False, learn_coef = learn_coef) )
            workers.append(thread)


        for wrkr in workers:
            wrkr.run()

        print("complete")



    def create_image(self, width, height = None):
        
        if height == None: height = width

        predicted_image = np.zeros((width,height))

        for row in range(height):
            for col in range(width):

                prediction = self.network.predict(np.array([row/height, col/width]))
                predicted_image[row, col] = prediction

        return predicted_image
    




