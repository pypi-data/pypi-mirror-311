import numpy as np
from scipy.stats import gaussian_kde
from scipy.integrate import quad
import time
import math
import sys


def dist_divergence(data_1, data_2):
    """
    Calculate the similarity between two datasets based on the symmetric Kullback-Leibler divergence of their estimated PDFs.

    Parameters
    ----------
    data_1 : array-like
        The first dataset for comparison.
    data_2 : array-like
        The second dataset for comparison.

    Returns
    -------
    float
        A similarity score between 0 and 1, where a higher score indicates more similar distributions.
    """

    dataFirst = np.array(data_1)
    dataSecond = np.array(data_2)
    intervalCount = 1000
    #Calculate the kernel-density estimation using Gaussian kernels
    kde1 = gaussian_kde(dataFirst)
    kde2 = gaussian_kde(dataSecond)
    #Get the data range of the two data sets
    maxVal = max([dataFirst.max(),dataSecond.max()])
    minVal = min([dataFirst.min(),dataSecond.min()])
    dataVar = (maxVal - minVal)/intervalCount
    dataMin = minVal
    #General the index for calculating the integration of probability density function
    iList = []
    for n in range(intervalCount):
        iList.append(dataMin + dataVar)
        dataMin = dataMin + dataVar
    #The probability density functions (PDFs)
    data1PDFs = kde1.pdf(iList)
    dataPDFs = kde2.pdf(iList)
    if len(data1PDFs) < len(dataPDFs):
        dataPDFs = dataPDFs[0:len(data1PDFs)]
        intervalCount = len(data1PDFs)
    else:
        data1PDFs = data1PDFs[0:len(dataPDFs)]
        intervalCount = len(dataPDFs)
    #Calculating the KL-Divergence
    dataKLM2 = 0
    dataKLM1 = 0
    for p in range(intervalCount):
        try:
            dataKLM2 += dataPDFs[p]* dataVar * math.log2((dataPDFs[p]*(10**300))/(data1PDFs[p]*(10**300)))
        except:
            e = sys.exc_info()[0]
            print( "Math Error in KLD: %s" % e )
            return 0
    for q in range(intervalCount):
        try:
            dataKLM1 += data1PDFs[q]* dataVar * math.log2((data1PDFs[q]*(10**300))/(dataPDFs[q]*(10**300)))
        except:
             e = sys.exc_info()[0]
             print( "Math Error in KLD: %s" % e )
             return 0
    #Calculating the symmetrical KL-Divergence, also known as Jeffreys’ J-Divergence
    symKL = dataKLM2 + dataKLM1
    #Calculating the likelihood 
    dataScoreM = 2**(-symKL)
    #print("Similarity probability(symmetric):", "%.2f%%" % float(100*round(dataScoreM,4)))
    return dataScoreM


def collect_data_for_interval(benchmark_function, interval_duration, sampling_portion):
    """
    Collect benchmark data for a specified time interval using periodic sampling.
    
    Args:
        benchmark_function (callable): Function that returns a single benchmark measurement
        interval_duration (float): Total duration to collect data in seconds
        sampling_portion (float): Fraction of the interval to spend collecting samples (0.0 to 1.0)
        
    Returns:
        list: Collected benchmark measurements
        
    Notes:
        - Actively collects samples during sampling_portion of the interval
        - Adapts to long-running benchmark functions
        - Ensures sampling_portion is respected over the total interval
        - Sleeps during non-sampling periods to reduce system load
    """
    data = []
    start_time = time.time()
    total_active_time = 0
    
    while time.time() - start_time < interval_duration:
        # Calculate whether we should run another benchmark
        elapsed_total = time.time() - start_time
        target_active_time = elapsed_total * sampling_portion
        
        if total_active_time < target_active_time:
            # Run benchmark and track how long it took
            benchmark_start = time.time()
            data.append(benchmark_function())
            benchmark_duration = time.time() - benchmark_start
            total_active_time += benchmark_duration
            
        else:
            sleep_duration = min(
                1.0,  # Maximum sleep of 1 second
                (total_active_time - target_active_time) / sampling_portion
            )
            time.sleep(sleep_duration)
    
    return data


def validate_stability(test_duration, benchmark_function, sampling_portion, stability_probability, existing_data):
    """
    Validate the stability of a performance distribution by comparing it with new data.
    
    Args:
        test_duration (float): Duration of the test interval in seconds
        benchmark_function (callable): Function that returns a single benchmark measurement
        sampling_portion (float): Fraction of each hour to spend collecting samples (0.0 to 1.0)
        stability_probability (float): Probability to determine stability
        existing_kde (scipy.stats.gaussian_kde): Existing kernel density estimate to compare against
        
    Returns:
        tuple: (
            bool: True if distribution is stable, False otherwise,
            list: Combined data from both collection intervals,
            scipy.stats.gaussian_kde: Updated kernel density estimate
        )
    """

    data_1, data_2 = collect_two_intervals(benchmark_function, test_duration, sampling_portion)
    data_combined = np.append(data_1, data_2)

    similarity_prob = dist_divergence(existing_data, data_combined)
    validate = similarity_prob >= stability_probability

    if(validate):
        print("Validation successful with similarity probability: ", "{0:.2%}".format(similarity_prob))
    else:
        print("Validation failed with similarity probability: ", "{0:.2%}".format(similarity_prob))

    return validate, np.append(existing_data, data_combined)


def collect_two_intervals(benchmark_function, interval_duration, sampling_portion):
    """
    Collect benchmark data over two consecutive intervals and compute their distributions.
    
    Args:
        benchmark_function (callable): Function that returns a single benchmark measurement
        interval_duration (float): Duration of each interval in seconds
        sampling_portion (float): Fraction of each hour to spend collecting samples (0.0 to 1.0)
        
    Returns:
        tuple: (
            scipy.stats.gaussian_kde: KDE for first interval,
            scipy.stats.gaussian_kde: KDE for combined intervals,
            list: Data from first interval,
            list: Data from second interval
        )
    """

    print("Collecting data for two intervals...")
    data_1 = collect_data_for_interval(benchmark_function, interval_duration, sampling_portion)
    data_2 = collect_data_for_interval(benchmark_function, interval_duration, sampling_portion)
    return data_1, data_2


def pt4cloud_lite(benchmark_function, stability_probability=0.9, max_intervals=10, interval_duration=(60*60*24), interval_increase=0.5, sampling_portion=1.0, validate=True):
    """
    Performance Testing for Cloud (Lite Version) - Analyzes performance stability over time.
    
    Args:
        benchmark_function (callable): Function that returns a single benchmark measurement
        stability_probability (float, optional): Probability to determine stability. 
            Defaults to 0.9
        max_intervals (int, optional): Maximum number of intervals to try before giving up. 
            Defaults to 10
        interval_duration (int, optional): Base duration of each interval in seconds. 
            Defaults to 24 hours
        interval_increase (float, optional): Factor to increase interval duration by after each 
            failed attempt. Defaults to 0.5
        sampling_portion (float, optional): Fraction of each hour to spend collecting samples 
            (0.0 to 1.0). Defaults to 1.0
        validate (bool, optional): Whether to perform additional validation of stability. 
            Defaults to True
            
    Returns:
        tuple: (
            list: All collected benchmark measurements,
            scipy.stats.gaussian_kde: Final kernel density estimate of the stable distribution
        )
        
    Notes:
        - Designed for performance testing intervals of less than 7 days
        - Uses KL divergence to measure distribution stability
        - Progressively increases interval duration until stability is achieved
        - Can perform additional validation of stability if requested
        - Returns None for both values if stability is not achieved within max_intervals
    """

    data = []

    for i in range(0, max_intervals-1):
        # Increase the duration of the interval for each failed iteration
        test_duration = interval_duration + interval_duration * interval_increase * i
        print("Current interval length is :", test_duration/3600, "hour(s)")

        # Collect data for two intervals
        data_1, data_2 = collect_two_intervals(benchmark_function, test_duration, sampling_portion)

        # Compute KL divergence between the two distributions
        similarity_prob = dist_divergence(data_1, data_2)

        print("Similarity probability is ", "{0:.2%}".format(similarity_prob))

        if similarity_prob >= stability_probability:
            if(validate):
                print("Performance distribution is stable with interval length : ", test_duration/3600, "hour(s)")
                # validate the stability of the distribution with more intervals
                print("Validating stability...")
                is_stable, data_3 = validate_stability(test_duration, benchmark_function, sampling_portion, stability_probability, np.append(data_1, data_2))
                if is_stable:
                    data = data_3
                    break
            else:
                print("Performance distribution is stable with interval length : ", test_duration/3600, "hour(s)")
                data = np.append(data_1, data_2)
                break
        else:
            print("Performance distribution is not stable with interval length : ", test_duration/3600, "hour(s)")
        print("Increasing interval length and retrying...")

    return data
