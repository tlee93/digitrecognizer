import numpy as np
import scipy.io as so
import scipy.optimize as opt

def costFunction(nn_params, *args):
    input_layer_size, hidden_layer_size, num_labels, X, Y, lambd = args[0], args[1], args[2], args[3], args[4], args[5]
    length1 = (input_layer_size+1)*(hidden_layer_size)

    nn1 = nn_params[:length1]
    T1 = nn1.reshape((hidden_layer_size, input_layer_size+1))
    nn2 = nn_params[length1:]
    T2 = nn2.reshape((num_labels, 1+ hidden_layer_size))
    m = X.shape[0]# number of training examples, useful for calculations
    ## You need to return the following variables correctly
    J = 0
    Theta1_grad = np.zeros(T1.shape)
    Theta2_grad = np.zeros(T2.shape)

    Theta1_grad = T1
    Theta2_grad = T2
    X = np.c_[np.ones(m), X] #pad with 1 for theta1
    z1 = X.dot(Theta1_grad.T)
    a1 = sigmoid(z1) #first activation layer
    a1 = np.c_[np.ones(m), a1] #pad the a layer with a 1
    H = sigmoid(a1.dot(Theta2_grad.T)) #output layer
    eye = np.eye(num_labels, dtype=int) #diagonal of 1's to simulate y vectors, 1 = [1 0 0 0 0 0 0 0 0 0] when numlabels = 10
    newY = np.zeros((Y.shape[0], num_labels)) #create a new Y matrix to hold ^^^^^ those

    while eye.shape[0] < 10: #makes sure there are 10 rows in the eye matrix
        eye = np.r_[eye, eye[eye.shape[0]%num_labels].reshape(1, num_labels)]

    for i in range(m): #convert Y into 0 and 1 arrays
        newY[i] = eye[Y[i]-1]

    J = np.sum((newY)*np.log(H) + (1-newY)*np.log(1-H))
    J /= (-m)

    d2 = H - newY # delta2
    d1 = d2.dot(Theta2_grad[:,1:])*sigmoidGradient(z1)
    Theta1_grad = d1.T.dot(X)
    Theta2_grad = d2.T.dot(a1)
    Theta1_grad /= m
    Theta2_grad /= m
    # unroll gradients and concatenate
    grad = np.concatenate([Theta1_grad.flatten(), Theta2_grad.flatten()])
    # return variables
    return J, grad

def gradApprox(nn_params, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd):
    epsilon = 0.0001


    gradientApprox = np.zeros(nn_params.size)
    for i in range(nn_params.shape[0]):

        nn_params1 = np.copy(nn_params)
        nn_params2 = np.copy(nn_params)

        nn_params1[i] += epsilon
        nn_params2[i] -= epsilon
        cost_plus = costFunction(nn_params1, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)[0]
        cost_minus = costFunction(nn_params2, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)[0]
        cost_diff = (cost_plus - cost_minus)/(2*.0001)

        gradientApprox[i] = cost_diff

    return gradientApprox


def sigmoid(h):
    sigmoid = 0
    sigmoid = 1.0/(1.0 + np.e ** (-h))
    return sigmoid




def sigmoidGradient(z):
    sigmoidGrad = 0
    g = sigmoid(z)
    sigmoidGrad = g*(1-g)
    return sigmoidGrad


def forwardPropAndAccuracy(nn_params, input_layer_size, hidden_layer_size, num_labels, X, Y):

    predictions = 0
    percentCorrect = 0
    length1 = (input_layer_size+1)*(hidden_layer_size)

    nn1 = nn_params[:length1]
    Theta1_grad = nn1.reshape((hidden_layer_size, input_layer_size+1))
    nn2 = nn_params[length1:]
    Theta2_grad = nn2.reshape((num_labels, 1+ hidden_layer_size))
    m = X.shape[0]# number of training examples, useful for calculations

    X = np.c_[np.ones(m), X] #pad with 1 for theta1
    a1 = sigmoid(X.dot(Theta1_grad.T)) #first activation layer
    a1 = np.c_[np.ones(m), a1] #pad the a layer with a 1
    H = sigmoid(a1.dot(Theta2_grad.T)) #output layer

    #now we have the predictions H, compare with Y labels
    eye = np.eye(num_labels, dtype=int) #diagonal of 1's to simulate y vectors, 1 = [1 0 0 0 0 0 0 0 0 0] when numlabels = 10
    newY = np.zeros((Y.shape[0], num_labels)) #create a new Y matrix to hold ^^^^^ those

    while eye.shape[0] < 10: #makes sure there are 10 rows in the eye matrix
        eye = np.r_[eye, eye[eye.shape[0]%num_labels].reshape(1, num_labels)]

    for i in range(m): #convert Y into 0 and 1 arrays
        newY[i] = eye[Y[i]-1]

    #round H up/down and store in new matrix
    newH = np.zeros(H.shape)
    for i in range(m):
        for j in range(H.shape[1]):
            count = 0       #for each row, keep count of how many 1's
            if H[i, j] > .9:
                newH[i,j] = 1
                count += 1
                if(count != 1): #there should only be a single 1 for each row in the predictions
                    print("error with prediction j=", j, " count= ", count) #hopefully won't see this line

    result = newY.T.dot(newH) #dot product will give a 10x10 matrix with the number correct of each number (0-9). use sum to count total correct
    percentCorrect = np.sum(result)/m

    predictions = H

   #make sure you return these correctly
    return predictions, percentCorrect


def randomInitializeWeights(weights, factor):
    W = np.random.random(weights.shape)
    #normalize so that it spans a range of twice epsilon
    W = W * 2 * factor # applied element wise
    #shift so that mean is at zero
    W = W - factor#L_in is the number of input units, L_out is the number of output
    #units in layer

    return W

# helper methods
def getCost(nn_params, *args):
    input_layer_size, hidden_layer_size, num_labels, X, Y, lambd = args[0], args[1], args[2], args[3], args[4], args[5]
    cost = costFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)[0]
    return cost



def getGrad(nn_params, *args):
    input_layer_size, hidden_layer_size, num_labels, X, Y, lambd = args[0], args[1], args[2], args[3], args[4], args[5]
    return costFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd )[1]

# Start Program! #

print("Loading Saved Neural Network Parameters...")

data = so.loadmat('ex4data1.mat')

X = data['X']
Y = data['y']


#previously determined weights to check
weights = so.loadmat('ex4weights.mat')

weights1 = weights['Theta1']
weights2 = weights['Theta2']

#weights1 = weights1.T


input_layer_size  = 400
hidden_layer_size = 25
num_labels = 10
lambd = 0
params = np.concatenate([weights1.flatten(), weights2.flatten()])

j, grad = costFunction(params, input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)

print("Cost at parameters loaded from ex4weights.mat. (This value should be about 0.383770 with regularization, 0.287629 without.): ", j)

print("sigmoidGrad of 0 (should be 0.25): ", sigmoidGradient(0))

params_check = randomInitializeWeights(np.zeros(params.shape), 15)

grad_check = costFunction(params_check[:35], 4, 4, 3, X[:10, :4], Y[:10, :3], lambd)[1]

grad_approx =  gradApprox(params_check[:35], 4, 4, 3, X[:10, :4], Y[:10, :3], lambd)

checkGradient = np.column_stack((grad_check, grad_approx))

print("Gradient check: the two columns should be very close: ", checkGradient)

nn_params = randomInitializeWeights(np.zeros(params.shape), .12)

args = (input_layer_size, hidden_layer_size, num_labels, X, Y, lambd)

result = opt.fmin_cg(getCost, nn_params, fprime=getGrad, args = args, maxiter = 400)

print("Accuracy: ", forwardPropAndAccuracy(result, input_layer_size, hidden_layer_size, num_labels, X, Y)[1])
