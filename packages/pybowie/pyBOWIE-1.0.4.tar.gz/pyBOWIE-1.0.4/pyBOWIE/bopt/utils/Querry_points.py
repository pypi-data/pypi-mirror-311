# *******************************************************
# Import libraries
# *******************************************************

import numpy as np
from scipy.optimize import minimize

# *******************************************************
# ****** Querry ******
# *******************************************************

def Querry(x_l, x_u, bnds, dims, af_params, constraints_method, sense, model, models_const, engine, Acq_fun):

    # Acquisition function for the optimization
    def Acquisition_function_opt(x, af_params, sense, model, models_const, engine):

        if sense == "maximize":
            af_opt = -Acq_fun(x.reshape(1,-1), af_params, constraints_method, model, models_const, engine)
        elif sense == "minimize":
            af_opt = Acq_fun(x.reshape(1,-1), af_params, constraints_method, model, models_const, engine)
        
        return af_opt
    
    # Main program
    
    res = minimize(Acquisition_function_opt, x0=np.random.uniform(x_l, x_u, (1,dims)).flatten(), args=(af_params, sense, model, models_const, engine), method='BFGS', bounds=bnds)
    x_opt = res.x

    return x_opt