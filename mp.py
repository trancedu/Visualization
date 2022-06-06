import numpy as np

# I am just putting this funtion to sleep
def comp_intense_function_ext(itr):
    # this is just some matrix multiplication that takes about 2 seconds
    x = np.random.rand(12000, 12000)
    x * x.T
    
    return('done with {}'.format(itr))

print("hello world")
print('good')