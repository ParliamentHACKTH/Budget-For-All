import numpy as np
def remove_comma_and_convert_to_int(x: str):
    return int(x.replace(",", ""))

def remove_comma_and_convert_to_float(x: str):
    return float(x.replace(",", ""))

def remove_word_province(x: str):
    return x.replace("จังหวัด", "")

def mahalanobis_distance(x, mean, cov):
    """
    Calculate the Mahalanobis distance between a point x and a distribution with given mean and covariance matrix.
    
    Parameters:
    x (numpy.ndarray): The data point (1-dimensional array).
    mean (numpy.ndarray): The mean of the distribution (1-dimensional array).
    cov (numpy.ndarray): The covariance matrix of the distribution (2-dimensional array).
    
    Returns:
    float: The Mahalanobis distance.
    """
    x_minus_mean = x - mean
    inv_cov = np.linalg.inv(cov)
    distance = np.sqrt(np.dot(np.dot(x_minus_mean.T, inv_cov), x_minus_mean))
    return distance
