'''
This file mainly randomises Weights, inputs, labels, etc,
to test various implementations
'''
import numpy as np
import matplotlib.pyplot as plt


from Tests_Utils import jacobian_verification, network_gradient_verification, jacobian_verification_visualizer, parse_data, test_network_on_data_set
from Activation_Functions import softmax_calculate, softmax_regression_loss, least_squares_loss, sgd
from SGD import sgd_find_global_minimum
from Neural_Network import activations, Layer, ResidualLayer, LossLayer, NeuralNetwork


def P1Q1_test_softmax_regression_loss():
    num_features = 5
    num_classes = 3
    num_samples = 10
    X = np.random.rand(num_features, num_samples)
    W = np.random.rand(num_features, num_classes)
    b = np.random.rand(num_classes,1)
    #set Y to a random matrix with 1s in the correct class and 0s elsewhere:
    Y = np.zeros((num_classes, num_samples))
    for i in range(num_samples):
        Y[np.random.randint(0, num_classes), i] = 1
        # create a decending array of epsilon values:
        epsilons = np.array([(0.5)**i for i in range(1, 10)])
        loss_function = softmax_regression_loss

    losses_ord1, losses_ord2 = jacobian_verification(X , W, Y, b, epsilons, loss_function)
    jacobian_verification_visualizer(losses_ord1, losses_ord2, epsilons)


def P1Q2_test_sgd_with_least_squares():
    #create data A, b s.t the appropriate functions will make y=2x (for example):
    A = np.random.rand(100, 1)
    b = 2*A
    #initialize x to a different factor than 2:
    x = float(10)
    #perform sgd and plot the initialised x and the final x:
    alpha = 0.1
    num_iterations = 100
    loss_function = least_squares_loss
    x_final, _, losses = sgd(A, b, x, 0, loss_function, alpha, num_iterations)
    #add a fig for the loss and a fig for comparing the initial x to the final x on top of the data:
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))

    axs[0].scatter(A, b, label='Data')
    axs[0].plot(A, x*A, label='Initial x')
    axs[0].plot(A, x_final*A, label='Final x')
    axs[0].set_xlabel('A')
    axs[0].set_ylabel('b')
    axs[0].set_title('Linear Regression')
    axs[0].legend()

    axs[1].plot(losses)
    axs[1].set_xlabel('Iteration')
    axs[1].set_ylabel('Loss')
    axs[1].set_title('Least Squares Loss')

    plt.tight_layout()
    plt.show()

def P1Q3_test_sgd_with_softmax(data_set_name):
    Yt, Ct, Yv, Cv = parse_data(data_set_name)
    alpha = 0.1
    num_iterations = 200
    batch_size = 30
    test_size = 5000
    loss_function = softmax_regression_loss
    W_final, b_final, losses, test_losses, train_accuracies, test_accuracies = sgd_find_global_minimum(Yt, Ct, Yv, Cv, loss_function, alpha, num_iterations, batch_size, test_size)
    accuracy = np.mean(np.argmax(softmax_calculate(np.dot(Yv.T, W_final) + b_final.T), axis=1) == np.argmax(Cv.T, axis=1))
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].plot(losses, label='Train Loss')
    axs[0].plot(test_losses, label='Test Loss')
    axs[0].set_xlabel('Iteration')
    axs[0].set_ylabel('Loss')
    axs[0].set_title('Train & Test Losses.')
    axs[0].legend()
    axs[1].plot(train_accuracies, label='Train Accuracy')
    axs[1].plot(test_accuracies, label='Test Accuracy')
    axs[1].set_xlabel('Iteration')
    axs[1].set_ylabel('Accuracy')
    axs[1].set_title(f'Success Precentages of the data classification. Final Accuracy: {accuracy:.2f}')
    axs[1].legend()
    plt.tight_layout()
    plt.show()
    


def P2Q1_test_NN_all_layers():
    input_dim = 3
    hidden_1 = 2
    hidden_2 = 7
    output_dim = 5
    tanh_activation = activations["tanh"]
    layer1 = Layer(input_dim, hidden_1, tanh_activation)
    layer2 = Layer(hidden_1, hidden_2, tanh_activation)
    loss_layer = LossLayer(hidden_2, output_dim)
    network = NeuralNetwork([layer1, layer2, loss_layer])
    epsilons = np.array([(0.5)**i for i in range(1, 10)])
    input_features = network.layers[0].W.shape[1]
    classes = network.layers[-1].b.shape[1]
    num_samples = 10
    X = np.random.rand(input_features, num_samples)
    Y = np.zeros((classes, num_samples))
    Y[np.random.randint(0, classes)] = 1
    losses_ord1, losses_ord2 = network_gradient_verification(network, X, Y, epsilons)
    jacobian_verification_visualizer(losses_ord1, losses_ord2, epsilons)


def P2Q2_test_ResNet_all_layers():
    input_dim = 5
    num_samples = 10
    output_dim = 5
    tanh_activation = activations["tanh"]
    layer1 = ResidualLayer(input_dim, num_samples ,tanh_activation)
    layer2 = ResidualLayer(input_dim, num_samples ,tanh_activation)
    layer3 = ResidualLayer(input_dim, num_samples ,tanh_activation)
    loss_layer = LossLayer(input_dim, output_dim)
    network = NeuralNetwork([layer1, layer2, layer3, loss_layer])
    epsilons = np.array([(0.5)**i for i in range(1, 10)])
    input_features = network.layers[0].W1.shape[1]
    X = np.random.rand(input_features, num_samples)
    Y = np.zeros((output_dim, num_samples))
    Y[np.random.randint(0, input_features)] = 1
    losses_ord1, losses_ord2 = network_gradient_verification(network, X, Y, epsilons)
    jacobian_verification_visualizer(losses_ord1, losses_ord2, epsilons)

def P2Q3():
    pass

def P2Q4_test_networks_on_swissroll_data(limited=False):
    input_dim = 2
    hidden_layer = 6
    num_samples= 30
    relu_activation = activations["relu"]
    layer1 = ResidualLayer(input_dim, num_samples ,relu_activation)
    layer1_1 = Layer(input_dim, hidden_layer, relu_activation)
    layer2 = ResidualLayer(hidden_layer, num_samples ,relu_activation)
    layer2_1 = Layer(hidden_layer, input_dim, relu_activation)
    layer3 = ResidualLayer(input_dim, num_samples ,relu_activation)
    loss_layer = LossLayer(input_dim, input_dim)
    network = NeuralNetwork([layer1, layer1_1, layer2, layer2_1, layer3, loss_layer])
    train_losses, test_loss, test_accurcy = test_network_on_data_set("SwissRollData", network, limited)
    plt.plot(train_losses, label="train_loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title(f'Test Loss: {test_loss}, Model Accuracy: {test_accurcy:.2f}')
    plt.legend()
    plt.show()

def P2Q4_test_networks_on_peaks_data(limited=False):
    input_dim = 2
    hidden_layer = 6
    output_dim = 5
    num_samples= 30
    relu_activation = activations["relu"]
    layer1 = ResidualLayer(input_dim, num_samples ,relu_activation)
    layer1_1 = Layer(input_dim, hidden_layer, relu_activation)
    layer2 = ResidualLayer(hidden_layer, num_samples ,relu_activation)
    layer2_1 = Layer(hidden_layer, input_dim, relu_activation)
    layer3 = ResidualLayer(input_dim, num_samples ,relu_activation)
    loss_layer = LossLayer(input_dim, output_dim)
    network = NeuralNetwork([layer1, layer1_1, layer2, layer2_1, layer3, loss_layer])
    train_losses, test_loss, test_accurcy = test_network_on_data_set("PeaksData", network, limited)
    plt.plot(train_losses, label="train_loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title(f'Test Loss: {test_loss}, Model Accuracy: {test_accurcy:.2f}')
    plt.legend()
    plt.show()

def P2Q4_test_networks_on_gmm_data(limited=False):
    input_dim = 5
    hidden_layer = 6
    num_samples= 30
    relu_activation = activations["relu"]
    layer1 = ResidualLayer(input_dim, num_samples ,relu_activation)
    layer1_1 = Layer(input_dim, hidden_layer, relu_activation)
    layer2 = ResidualLayer(hidden_layer, num_samples ,relu_activation)
    layer2_1 = Layer(hidden_layer, input_dim, relu_activation)
    layer3 = ResidualLayer(input_dim, num_samples ,relu_activation)
    loss_layer = LossLayer(input_dim, input_dim)
    network = NeuralNetwork([layer1, layer1_1, layer2, layer2_1, layer3, loss_layer])
    train_losses, test_loss, test_accurcy = test_network_on_data_set("GMMData", network, limited)
    plt.plot(train_losses, label="train_loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title(f'Test Loss: {test_loss}, Model Accuracy: {test_accurcy:.2f}')
    plt.legend()
    plt.show()

data_to_test = {
    "SwissRollData": P2Q4_test_networks_on_swissroll_data,
    "PeaksData": P2Q4_test_networks_on_peaks_data,
    "GMMData": P2Q4_test_networks_on_gmm_data
}

def P2Q4_test_network_on_data_set(data_set_name):
    data_to_test[data_set_name]()

def P2Q5_test_network_on_limited_data_set(data_set_name):
    data_to_test[data_set_name](limited=True)

def main():
    P1Q3_test_sgd_with_softmax("SwissRollData")
    
if __name__ == "__main__":
    main()