# *******************************************************
# ****** Import libraries ******
# *******************************************************

from ..utils.Preprocessing_data import Train_reducer, Train_inverter, Reduce, Inverse

# *******************************************************
# ****** Up_search_space_params ******
# *******************************************************

def Up_search_space_params(x, x_tau, d_nc, dims, problem_type, n_components, reducer, inverter, inverter_transform):

    if reducer == "no":
        x_tau_ = x_tau
        reducer_trained = None
        inverter_ = None
    else:
        x_tau_, reducer_trained = Train_reducer(x, d_nc, dims, problem_type, n_components, reducer) 
        if inverter_transform == "no":
            inverter_ = Train_inverter(x, x_tau, dims, inverter)
        elif inverter_transform == "yes":
            inverter_ = reducer_trained
        else:
            pass
        
    return x_tau_, reducer_trained, inverter_