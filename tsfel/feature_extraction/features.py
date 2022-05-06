import scipy.signal
from tsfel.feature_extraction.features_utils import *


# ############################################# TEMPORAL DOMAIN ##################################################### #
@set_domain("domain", "temporal")
@set_domain("tag", "inertial")
@vectorize
def autocorr(signal):
    """Computes autocorrelation of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which autocorrelation is computed

    Returns
    -------
    float
        Cross correlation of 1-dimensional sequence

    """
    signal = np.array(signal)
    return float(np.correlate(signal, signal))


@set_domain("domain", "temporal")
def calc_centroid(signal, fs):
    """Computes the centroid along the time axis.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which centroid is computed
    fs: int
        Signal sampling frequency

    Returns
    -------
    float
        Temporal centroid

    """

    time = compute_time(signal, fs)

    energy = signal ** 2

    t_energy = np.sum(time * energy, axis=-1)
    energy_sum = np.array(np.sum(energy, axis=-1), dtype=float)
    return devide_keep_zero(t_energy, energy_sum)


@set_domain("domain", "temporal")
@set_domain("tag", "emg")
@vectorize
def negative_turning(signal):
    """Computes number of negative turning points of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which minimum number of negative turning points are counted
    Returns
    -------
    float
        Number of negative turning points

    """
    diff_sig = np.diff(signal)
    array_signal = np.arange(len(diff_sig[:-1]))
    negative_turning_pts = np.where((diff_sig[array_signal] < 0) & (diff_sig[array_signal + 1] > 0))[0]

    return len(negative_turning_pts)


@set_domain("domain", "temporal")
@set_domain("tag", "emg")
@vectorize
def positive_turning(signal):
    """Computes number of positive turning points of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which  positive turning points are counted

    Returns
    -------
    float
        Number of positive turning points

    """
    diff_sig = np.diff(signal)

    array_signal = np.arange(len(diff_sig[:-1]))

    positive_turning_pts = np.where((diff_sig[array_signal + 1] < 0) & (diff_sig[array_signal] > 0))[0]

    return len(positive_turning_pts)


@set_domain("domain", "temporal")
def mean_abs_diff(signal):
    """Computes mean absolute differences of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which mean absolute deviation is computed

    Returns
    -------
    float
        Mean absolute difference result

    """
    return np.mean(np.abs(np.diff(signal)), axis=-1)


@set_domain("domain", "temporal")
def mean_diff(signal):
    """Computes mean of differences of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which mean of differences is computed

    Returns
    -------
    float
        Mean difference result

    """
    return np.mean(np.diff(signal), axis=-1)


@set_domain("domain", "temporal")
def median_abs_diff(signal):
    """Computes median absolute differences of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which median absolute difference is computed

    Returns
    -------
    float
        Median absolute difference result

    """
    return np.median(np.abs(np.diff(signal)), axis=-1)


@set_domain("domain", "temporal")
def median_diff(signal):
    """Computes median of differences of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which median of differences is computed

    Returns
    -------
    float
        Median difference result

    """
    return np.median(np.diff(signal), axis=-1)


@set_domain("domain", "temporal")
def distance(signal):
    """Computes signal traveled distance.

     Calculates the total distance traveled by the signal
     using the hypotenuse between 2 datapoints.

    Feature computational cost: 1

     Parameters
     ----------
     signal : nd-array
         Input from which distance is computed

     Returns
     -------
     float
         Signal distance

    """
    return np.sum(np.sqrt(np.diff(signal) ** 2 + 1), axis=-1)


@set_domain("domain", "temporal")
def sum_abs_diff(signal):
    """Computes sum of absolute differences of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which sum absolute difference is computed

    Returns
    -------
    float
        Sum absolute difference result

    """
    return np.sum(np.abs(np.diff(signal)), axis=-1)


@set_domain("domain", "temporal")
@set_domain("tag", ["audio", "emg"])
def zero_cross(signal):
    """Computes Zero-crossing rate of the signal.

    Corresponds to the total number of times that the signal changes from
    positive to negative or vice versa.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which the zero-crossing rate are computed

    Returns
    -------
    int
        Number of times that signal value cross the zero axis

    """
    return np.sum(np.abs(np.diff(np.sign(signal))) == 2, axis=-1)


@set_domain("domain", "temporal")
@vectorize
def slope(signal):
    """Computes the slope of the signal.

    Slope is computed by fitting a linear equation to the observed data.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which linear equation is computed

    Returns
    -------
    float
        Slope

    """
    t = np.linspace(0, len(signal) - 1, len(signal))

    return np.polyfit(t, signal, 1)[0]


@set_domain("domain", "temporal")
def auc(signal, fs):
    """Computes the area under the curve of the signal computed with trapezoid rule.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which the area under the curve is computed
    fs : float
        Sampling Frequency
    Returns
    -------
    float
        The area under the curve value

    """
    t = compute_time(signal, fs)
    return np.sum(0.5 * np.diff(t, axis=-1) * np.abs(signal[..., :-1] + signal[..., 1:]), axis=-1)


@set_domain("domain", "temporal")
def neighbourhood_peaks(signal, n=10):
    """Computes the number of peaks from a defined neighbourhood of the signal.

    Reference: Christ, M., Braun, N., Neuffer, J. and Kempa-Liehr A.W. (2018). Time Series FeatuRe Extraction on basis
     of Scalable Hypothesis tests (tsfresh -- A Python package). Neurocomputing 307 (2018) 72-77

    Parameters
    ----------
    signal : nd-array
         Input from which the number of neighbourhood peaks is computed
    n :  int
        Number of peak's neighbours to the left and to the right

    Returns
    -------
    int
        The number of peaks from a defined neighbourhood of the signal
    """
    signal = np.array(signal)
    subsequence = signal[n:-n]
    # initial iteration
    peaks = ((subsequence > np.roll(signal, 1)[n:-n]) & (subsequence > np.roll(signal, -1)[n:-n]))
    for i in range(2, n + 1):
        peaks &= (subsequence > np.roll(signal, i)[n:-n])
        peaks &= (subsequence > np.roll(signal, -i)[n:-n])
    return np.sum(peaks)


# ############################################ STATISTICAL DOMAIN #################################################### #
@set_domain("domain", "statistical")
@set_domain("tag", "audio")
def abs_energy(signal):
    """Computes the absolute energy of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which the area under the curve is computed

    Returns
    -------
    float
        Absolute energy

    """
    return np.sum(signal ** 2, axis=-1)


@set_domain("domain", "statistical")
@set_domain("tag", "audio")
def average_power(signal, fs):
    """Computes the average power of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Signal from which average power is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Average power

    """
    return np.sum(signal ** 2, axis=-1) / (np.ma.size(signal, axis=-1) / fs - 1.0 / fs)


@set_domain("domain", "statistical")
@set_domain("tag", "eeg")
@vectorize
def entropy(signal, prob="standard"):
    """Computes the entropy of the signal using the Shannon Entropy.

    Description in Article:
    Regularities Unseen, Randomness Observed: Levels of Entropy Convergence
    Authors: Crutchfield J. Feldman David

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which entropy is computed
    prob : string
        Probability function (kde or gaussian functions are available)

    Returns
    -------
    float
        The normalized entropy value

    """

    if prob == "standard":
        value, counts = np.unique(signal, return_counts=True)
        p = counts / counts.sum()
    elif prob == "kde":
        p = kde(signal)
    elif prob == "gauss":
        p = gaussian(signal)

    if np.sum(p) == 0:
        return 0.0

    # Handling zero probability values
    p = p[np.where(p != 0)]

    # If probability all in one value, there is no entropy
    if np.log2(len(signal)) == 1:
        return 0.0
    elif np.sum(p * np.log2(p)) / np.log2(len(signal)) == 0:
        return 0.0
    else:
        return -np.sum(p * np.log2(p)) / np.log2(len(signal))


@set_domain("domain", "temporal")
@vectorize
def neighbourhood_peaks(signal, n=10):
    """Computes the number of peaks from a defined neighbourhood of the signal.

    Reference: Christ, M., Braun, N., Neuffer, J. and Kempa-Liehr A.W. (2018). Time Series FeatuRe Extraction on basis
     of Scalable Hypothesis tests (tsfresh -- A Python package). Neurocomputing 307 (2018) 72-77

    Parameters
    ----------
    signal : nd-array
         Input from which the number of neighbourhood peaks is computed
    n :  int
        Number of peak's neighbours to the left and to the right

    Returns
    -------
    int
        The number of peaks from a defined neighbourhood of the signal
    """
    signal = np.array(signal)
    subsequence = signal[n:-n]
    # initial iteration
    peaks = (subsequence > np.roll(signal, 1)[n:-n]) & (subsequence > np.roll(signal, -1)[n:-n])
    for i in range(2, n + 1):
        peaks &= subsequence > np.roll(signal, i)[n:-n]
        peaks &= subsequence > np.roll(signal, -i)[n:-n]
    return np.sum(peaks)


# ############################################ STATISTICAL DOMAIN #################################################### #
@set_domain("domain", "statistical")
@vectorize
def hist(signal, nbins=10, r=1):
    """Computes histogram of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from histogram is computed
    nbins : int
        The number of equal-width bins in the given range
    r : float
        The lower(-r) and upper(r) range of the bins

    Returns
    -------
    nd-array
        The values of the histogram

    """
    histsig, bin_edges = np.histogram(signal, bins=nbins, range=[-r, r])  # TODO:subsampling parameter

    return tuple(histsig)


@set_domain("domain", "statistical")
def interq_range(signal):
    """Computes interquartile range of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which interquartile range is computed

    Returns
    -------
    float
        Interquartile range result

    """
    return np.percentile(signal, 75, axis=-1) - np.percentile(signal, 25, axis=-1)


@set_domain("domain", "statistical")
def kurtosis(signal):
    """Computes kurtosis of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which kurtosis is computed

    Returns
    -------
    float
        Kurtosis result

    """
    return scipy.stats.kurtosis(signal, axis=-1)


@set_domain("domain", "statistical")
def skewness(signal):
    """Computes skewness of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which skewness is computed

    Returns
    -------
    int
        Skewness result

    """
    return scipy.stats.skew(signal, axis=-1)


@set_domain("domain", "statistical")
def calc_max(signal):
    """Computes the maximum value of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
       Input from which max is computed

    Returns
    -------
    float
        Maximum result

    """
    return np.max(signal, axis=-1)


@set_domain("domain", "statistical")
def calc_min(signal):
    """Computes the minimum value of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which min is computed

    Returns
    -------
    float
        Minimum result

    """
    return np.min(signal, axis=-1)


@set_domain("domain", "statistical")
@set_domain("tag", "inertial")
def calc_mean(signal):
    """Computes mean value of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which mean is computed.

    Returns
    -------
    float
        Mean result

    """
    return np.mean(signal, axis=-1)


@set_domain("domain", "statistical")
def calc_median(signal):
    """Computes median of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which median is computed

    Returns
    -------
    float
        Median result

    """
    return np.median(signal, axis=-1)


@set_domain("domain", "statistical")
def mean_abs_deviation(signal):
    """Computes mean absolute deviation of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which mean absolute deviation is computed

    Returns
    -------
    float
        Mean absolute deviation result

    """
    return np.mean(np.abs(signal - match_last_dim_by_value_repeat(np.mean(signal, axis=-1), signal)), axis=-1)


@set_domain("domain", "statistical")
def median_abs_deviation(signal):
    """Computes median absolute deviation of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which median absolute deviation is computed

    Returns
    -------
    float
        Mean absolute deviation result

    """
    return scipy.stats.median_absolute_deviation(signal, scale=1, axis=-1)


@set_domain("domain", "statistical")
@set_domain("tag", ["inertial", "emg"])
def rms(signal):
    """Computes root mean square of the signal.

    Square root of the arithmetic mean (average) of the squares of the original values.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which root mean square is computed

    Returns
    -------
    float
        Root mean square

    """
    return np.sqrt(np.mean(np.square(signal), axis=-1))


@set_domain("domain", "statistical")
def calc_std(signal):
    """Computes standard deviation (std) of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which std is computed

    Returns
    -------
    float
        Standard deviation result

    """
    return np.std(signal, axis=-1)


@set_domain("domain", "statistical")
def calc_var(signal):
    """Computes variance of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
       Input from which var is computed

    Returns
    -------
    float
        Variance result

    """
    return np.var(signal, axis=-1)


@set_domain("domain", "statistical")
def pk_pk_distance(signal):
    """Computes the peak to peak distance.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which peak to peak is computed

    Returns
    -------
    float
        peak to peak distance

    """
    return np.ptp(signal, axis=-1)


@set_domain("domain", "statistical")
def ecdf(signal, d=10):
    """Computes the values of ECDF (empirical cumulative distribution function) along the time axis.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which ECDF is computed
    d: integer
        Number of ECDF values to return

    Returns
    -------
    float
        The values of the ECDF along the time axis
    """
    _, y = calc_ecdf(signal)
    if len(signal) <= d:
        return tuple(y)
    else:
        return tuple(y[:d])


@set_domain("domain", "statistical")
@vectorize
def ecdf_slope(signal, p_init=0.5, p_end=0.75):
    """Computes the slope of the ECDF between two percentiles.
    Possibility to return infinity values.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which ECDF is computed
    p_init : float
        Initial percentile
    p_end : float
        End percentile

    Returns
    -------
    float
        The slope of the ECDF between two percentiles
    """
    signal = np.array(signal)
    # check if signal is constant
    if np.sum(np.diff(signal)) == 0:
        return np.inf
    else:
        x_init, x_end = ecdf_percentile(signal, percentile=[p_init, p_end])
        return (p_end - p_init) / (x_end - x_init)


@set_domain("domain", "statistical")
@vectorize
def ecdf_percentile(signal, percentile=[0.2, 0.8]):
    """Computes the percentile value of the ECDF.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which ECDF is computed
    percentile: list
        Percentile value to be computed

    Returns
    -------
    float
        The input value(s) of the ECDF
    """
    signal = np.array(signal)
    if isinstance(percentile, str):
        percentile = eval(percentile)
    if isinstance(percentile, (float, int)):
        percentile = [percentile]

    # calculate ecdf
    x, y = calc_ecdf(signal)

    if len(percentile) > 1:
        # check if signal is constant
        if np.sum(np.diff(signal)) == 0:
            return tuple(np.repeat(signal[0], len(percentile)))
        else:
            return tuple([x[y <= p].max() for p in percentile])
    else:
        # check if signal is constant
        if np.sum(np.diff(signal)) == 0:
            return signal[0]
        else:
            return x[y <= percentile].max()


@set_domain("domain", "statistical")
@vectorize
def ecdf_percentile_count(signal, percentile=[0.2, 0.8]):
    """Computes the cumulative sum of samples that are less than the percentile.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which ECDF is computed
    percentile: list
        Percentile threshold

    Returns
    -------
    float
        The cumulative sum of samples
    """
    signal = np.array(signal)
    if isinstance(percentile, str):
        percentile = eval(percentile)
    if isinstance(percentile, (float, int)):
        percentile = [percentile]

    # calculate ecdf
    x, y = calc_ecdf(signal)

    if len(percentile) > 1:
        # check if signal is constant
        if np.sum(np.diff(signal)) == 0:
            return tuple(np.repeat(signal[0], len(percentile)))
        else:
            return tuple([x[y <= p].shape[0] for p in percentile])
    else:
        # check if signal is constant
        if np.sum(np.diff(signal)) == 0:
            return signal[0]
        else:
            return x[y <= percentile].shape[0]


# ############################################## SPECTRAL DOMAIN ##################################################### #
@set_domain("domain", "spectral")
def spectral_distance(signal, fs):
    """Computes the signal spectral distance.

    Distance of the signal's cumulative sum of the FFT elements to
    the respective linear regression.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral distance is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        spectral distance

    """
    _, fmag = calc_fft(signal, fs)

    cum_fmag = np.cumsum(fmag, axis=-1)

    # Compute the linear regression
    # TODO: there must be a nicer version than this transpose...
    points_y = np.linspace(0, cum_fmag[..., -1], np.ma.size(cum_fmag, axis=-1))
    points_y = points_y.transpose(np.append(np.arange(1, signal.ndim), 0))

    return np.sum(points_y - cum_fmag, axis=-1)


@set_domain("domain", "spectral")
@vectorize
def fundamental_frequency(signal, fs):
    """Computes fundamental frequency of the signal.

    The fundamental frequency integer multiple best explain
    the content of the signal spectrum.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which fundamental frequency is computed
    fs : float
        Sampling frequency

    Returns
    -------
    f0: float
       Predominant frequency of the signal

    """
    signal = signal - np.mean(signal)
    f, fmag = calc_fft(signal, fs)

    # Finding big peaks, not considering noise peaks with low amplitude

    bp = scipy.signal.find_peaks(fmag, height=max(fmag) * 0.3)[0]

    # # Condition for offset removal, since the offset generates a peak at frequency zero
    bp = bp[bp != 0]
    if not list(bp):
        f0 = 0
    else:
        # f0 is the minimum big peak frequency
        f0 = f[min(bp)]

    return f0


@set_domain("domain", "spectral")
@vectorize
def max_power_spectrum(signal, fs):
    """Computes maximum power spectrum density of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which maximum power spectrum is computed
    fs : float
        Sampling frequency

    Returns
    -------
    nd-array
        Max value of the power spectrum density

    """
    if np.std(signal) == 0:
        return float(max(scipy.signal.welch(signal, fs, nperseg=len(signal))[1]))
    else:
        return float(max(scipy.signal.welch(signal / np.std(signal), fs, nperseg=len(signal))[1]))


@set_domain("domain", "spectral")
def max_frequency(signal, fs):
    """Computes maximum frequency of the signal.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Input from which maximum frequency is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        0.95 of maximum frequency using cumsum
    """
    f, fmag = calc_fft(signal, fs)

    cum_fmag = np.cumsum(fmag, axis=-1)
    expanded = match_last_dim_by_value_repeat(np.take(cum_fmag, -1, axis=-1), cum_fmag)

    try:
        ind_mag = np.argmax(np.array(np.asarray(cum_fmag > expanded * 0.95)), axis=-1)
    except IndexError:
        ind_mag = np.argmax(cum_fmag, axis=-1)

    ind_mag = np.expand_dims(ind_mag, axis=-1)
    return np.squeeze(np.take(f, ind_mag), axis=-1)


@set_domain("domain", "spectral")
def median_frequency(signal, fs):
    """Computes median frequency of the signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which median frequency is computed
    fs: int
        Sampling frequency

    Returns
    -------
    f_median : int
       0.50 of maximum frequency using cumsum.
    """
    f, fmag = calc_fft(signal, fs)

    cum_fmag = np.cumsum(fmag, axis=-1)
    expanded = match_last_dim_by_value_repeat(np.take(cum_fmag, -1, axis=-1), cum_fmag)

    try:
        ind_mag = np.argmax(np.array(np.asarray(cum_fmag > expanded * 0.5)), axis=-1)
    except IndexError:
        ind_mag = np.argmax(cum_fmag, axis=-1)

    ind_mag = np.expand_dims(ind_mag, axis=-1)
    return np.squeeze(np.take(f, ind_mag), axis=-1)


@set_domain("domain", "spectral")
@set_domain("tag", "audio")
def spectral_centroid(signal, fs):
    """Barycenter of the spectrum.

    Description and formula in Article:
    The Timbre Toolbox: Extracting audio descriptors from musicalsignals
    Authors Peeters G., Giordano B., Misdariis P., McAdams S.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral centroid is computed
    fs: int
        Sampling frequency

    Returns
    -------
    float
        Centroid

    """
    f, fmag = calc_fft(signal, fs)
    summedFmag = match_last_dim_by_value_repeat(np.sum(fmag, axis=-1), fmag)
    return np.sum(f * devide_keep_zero(fmag, summedFmag), axis=-1)


@set_domain("domain", "spectral")
def spectral_decrease(signal, fs):
    """Represents the amount of decreasing of the spectra amplitude.

    Description and formula in Article:
    The Timbre Toolbox: Extracting audio descriptors from musicalsignals
    Authors Peeters G., Giordano B., Misdariis P., McAdams S.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral decrease is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Spectral decrease

    """
    _, fmag = calc_fft(signal, fs)

    fmag_band = fmag[..., 1:]
    len_fmag_band = np.arange(1, np.ma.size(fmag, axis=-1))

    # Sum of numerator
    soma_num = np.sum((fmag_band - match_last_dim_by_value_repeat(fmag[..., 0], fmag_band)) / len_fmag_band, axis=-1)

    return devide_keep_zero(1, np.sum(fmag_band, axis=-1)) * soma_num


@set_domain("domain", "spectral")
def spectral_kurtosis(signal, fs):
    """Measures the flatness of a distribution around its mean value.

    Description and formula in Article:
    The Timbre Toolbox: Extracting audio descriptors from musicalsignals
    Authors Peeters G., Giordano B., Misdariis P., McAdams S.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral kurtosis is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Spectral Kurtosis

    """
    f, fmag = calc_fft(signal, fs)
    spect_centr = spectral_centroid(signal, fs)
    spread = spectral_spread(signal, fs)

    summedFmag = match_last_dim_by_value_repeat(np.sum(fmag, axis=-1), fmag)
    spect_kurt = ((f - match_last_dim_by_value_repeat(spect_centr, f)) ** 4) * devide_keep_zero(fmag, summedFmag)
    return devide_keep_zero(np.sum(spect_kurt, axis=-1), spread ** 4)


@set_domain("domain", "spectral")
def spectral_skewness(signal, fs):
    """Measures the asymmetry of a distribution around its mean value.

    Description and formula in Article:
    The Timbre Toolbox: Extracting audio descriptors from musicalsignals
    Authors Peeters G., Giordano B., Misdariis P., McAdams S.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral skewness is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Spectral Skewness

    """
    f, fmag = calc_fft(signal, fs)
    spect_centr = spectral_centroid(signal, fs)
    summedFmag = match_last_dim_by_value_repeat(np.sum(fmag, axis=-1), fmag)

    skew = ((f - match_last_dim_by_value_repeat(spect_centr, f)) ** 3) * devide_keep_zero(fmag, summedFmag)
    return devide_keep_zero(np.sum(skew, axis=-1), spectral_spread(signal, fs) ** 3)


@set_domain("domain", "spectral")
def spectral_spread(signal, fs):
    """Measures the spread of the spectrum around its mean value.

    Description and formula in Article:
    The Timbre Toolbox: Extracting audio descriptors from musicalsignals
    Authors Peeters G., Giordano B., Misdariis P., McAdams S.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral spread is computed.
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Spectral Spread

    """
    f, fmag = calc_fft(signal, fs)
    spect_centroid = spectral_centroid(signal, fs)
    helper = (f - match_last_dim_by_value_repeat(spect_centroid, f)) ** 2
    summedFmag = match_last_dim_by_value_repeat(np.sum(fmag, axis=-1), fmag)
    return np.sum(helper * devide_keep_zero(fmag, summedFmag), axis=-1) ** 0.5


@set_domain("domain", "spectral")
def spectral_slope(signal, fs):
    """Computes the spectral slope.

    Spectral slope is computed by finding constants m and b of the function aFFT = mf + b, obtained by linear regression
    of the spectral amplitude.

    Description and formula in Article:
    The Timbre Toolbox: Extracting audio descriptors from musicalsignals
    Authors Peeters G., Giordano B., Misdariis P., McAdams S.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral slope is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Spectral Slope

    """
    f, fmag = calc_fft(signal, fs)

    num_ = devide_keep_zero(1, np.sum(fmag, axis=-1)) * (
        np.ma.size(f, axis=-1) * np.sum(f * fmag, axis=-1) - np.sum(f, axis=-1) * np.sum(fmag, axis=-1)
    )
    denom_ = np.ma.size(f, axis=-1) * np.sum(f * f, axis=-1) - np.sum(f, axis=-1) ** 2
    if len(np.shape(signal)) > 1:
        denom_ = np.tile(denom_, np.shape(signal)[0])
    return devide_keep_zero(num_, denom_)


@set_domain("domain", "spectral")
def spectral_variation(signal, fs):
    """Computes the amount of variation of the spectrum along time.

    Spectral variation is computed from the normalized cross-correlation between two consecutive amplitude spectra.

    Description and formula in Article:
    The Timbre Toolbox: Extracting audio descriptors from musicalsignals
    Authors Peeters G., Giordano B., Misdariis P., McAdams S.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral variation is computed.
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Spectral Variation

    """
    _, fmag = calc_fft(signal, fs)

    sum1 = np.sum(fmag[..., :-1] * fmag[..., 1:], axis=-1)
    sum2 = np.sum(fmag[..., 1:] ** 2, axis=-1)
    sum3 = np.sum(fmag[..., :-1] ** 2, axis=-1)

    return 1 - devide_keep_zero(sum1, ((sum2 ** 0.5) * (sum3 ** 0.5)))


@set_domain("domain", "spectral")
@vectorize
def spectral_positive_turning(signal, fs):
    """Computes number of positive turning points of the fft magnitude signal.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which the number of positive turning points of the fft magnitude are computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Number of positive turning points

    """
    f, fmag = calc_fft(signal, fs)
    diff_sig = np.diff(fmag)

    array_signal = np.arange(len(diff_sig[:-1]))

    positive_turning_pts = np.where((diff_sig[array_signal + 1] < 0) & (diff_sig[array_signal] > 0))[0]

    return len(positive_turning_pts)


@set_domain("domain", "spectral")
@set_domain("tag", "audio")
def spectral_roll_off(signal, fs):
    """Computes the spectral roll-off of the signal.

    The spectral roll-off corresponds to the frequency where 95% of the signal magnitude is contained
    below of this value.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral roll-off is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Spectral roll-off

    """
    f, fmag = calc_fft(signal, fs)
    cum_fmag = np.cumsum(fmag, axis=-1)
    value = match_last_dim_by_value_repeat(0.95 * np.sum(fmag, axis=-1), cum_fmag)
    ind_mag = np.argmax(np.array(np.asarray(cum_fmag > value)), axis=-1)
    ind_mag = np.expand_dims(ind_mag, axis=-1)
    return np.squeeze(np.take(f, ind_mag), axis=-1)


@set_domain("domain", "spectral")
def spectral_roll_on(signal, fs):
    """Computes the spectral roll-on of the signal.

    The spectral roll-on corresponds to the frequency where 5% of the signal magnitude is contained
    below of this value.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Signal from which spectral roll-on is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Spectral roll-on

    """
    f, fmag = calc_fft(signal, fs)
    cum_fmag = np.cumsum(fmag, axis=-1)
    value = match_last_dim_by_value_repeat(0.05 * np.sum(fmag, axis=-1), cum_fmag)
    ind_mag = np.argmax(np.array(np.asarray(cum_fmag >= value)), axis=-1)
    ind_mag = np.expand_dims(ind_mag, axis=-1)
    return np.squeeze(np.take(f, ind_mag), axis=-1)


@set_domain("domain", "spectral")
@set_domain("tag", "inertial")
def human_range_energy(signal, fs):
    """Computes the human range energy ratio.

    The human range energy ratio is given by the ratio between the energy
    in frequency 0.6-2.5Hz and the whole energy band.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Signal from which human range energy ratio is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Human range energy ratio

    """
    f, fmag = calc_fft(signal, fs)

    allenergy = np.sum(fmag ** 2, axis=-1)

    hr_energy = np.sum(fmag[..., np.argmin(np.abs(0.6 - f[..., :])) : np.argmin(np.abs(2.5 - f[..., :]))] ** 2, axis=-1)

    return devide_keep_zero(hr_energy, allenergy)


@set_domain("domain", "spectral")
@set_domain("tag", ["audio", "emg"])
@vectorize
def mfcc(signal, fs, pre_emphasis=0.97, nfft=512, nfilt=40, num_ceps=12, cep_lifter=22):
    """Computes the MEL cepstral coefficients.

    It provides the information about the power in each frequency band.

    Implementation details and description on:
    https://www.kaggle.com/ilyamich/mfcc-implementation-and-tutorial
    https://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html#fnref:1

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which MEL coefficients is computed
    fs : float
        Sampling frequency
    pre_emphasis : float
        Pre-emphasis coefficient for pre-emphasis filter application
    nfft : int
        Number of points of fft
    nfilt : int
        Number of filters
    num_ceps: int
        Number of cepstral coefficients
    cep_lifter: int
        Filter length

    Returns
    -------
    nd-array
        MEL cepstral coefficients

    """
    filter_banks = filterbank(signal, fs, pre_emphasis, nfft, nfilt)

    mel_coeff = scipy.fft.dct(filter_banks, type=2, axis=0, norm="ortho")[1 : (num_ceps + 1)]  # Keep 2-13

    mel_coeff -= np.mean(mel_coeff, axis=0) + 1e-8

    # liftering
    ncoeff = len(mel_coeff)
    n = np.arange(ncoeff)
    lift = 1 + (cep_lifter / 2) * np.sin(np.pi * n / cep_lifter)  # cep_lifter = 22 from python_speech_features library

    mel_coeff *= lift

    return tuple(mel_coeff)


@set_domain("domain", "spectral")
@vectorize
def power_bandwidth(signal, fs):
    """Computes power spectrum density bandwidth of the signal.

    It corresponds to the width of the frequency band in which 95% of its power is located.

    Description in article:
    Power Spectrum and Bandwidth Ulf Henriksson, 2003 Translated by Mikael Olofsson, 2005

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which the power bandwidth computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        Occupied power in bandwidth

    """
    # Computing the power spectrum density
    if np.std(signal) == 0:
        freq, power = scipy.signal.welch(signal, fs, nperseg=len(signal))
    else:
        freq, power = scipy.signal.welch(signal / np.std(signal), fs, nperseg=len(signal))

    if np.sum(power) == 0:
        return 0.0

    # Computing the lower and upper limits of power bandwidth
    cum_power = np.cumsum(power)
    f_lower = freq[np.where(cum_power >= cum_power[-1] * 0.95)[0][0]]

    cum_power_inv = np.cumsum(power[::-1])
    f_upper = freq[np.abs(np.where(cum_power_inv >= cum_power[-1] * 0.95)[0][0] - len(power) + 1)]

    # Returning the bandwidth in terms of frequency

    return np.abs(f_upper - f_lower)


@set_domain("domain", "spectral")
def fft_mean_coeff(signal, fs, nfreq=256):
    """Computes the mean value of each spectrogram frequency.

    nfreq can not be higher than half signal length plus one.
    When it does, it is automatically set to half signal length plus one.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which fft mean coefficients are computed
    fs : float
        Sampling frequency
    nfreq : int
        The number of frequencies

    Returns
    -------
    nd-array
        The mean value of each spectrogram frequency

    """
    nfreq = min(nfreq, np.ma.size(signal, axis=-1) // 2 + 1)

    return np.mean(scipy.signal.spectrogram(signal, fs, nperseg=nfreq * 2 - 2, axis=-1)[2], axis=-1)


@set_domain("domain", "spectral")
@set_domain("tag", "audio")
@vectorize
def lpcc(signal, n_coeff=12):
    """Computes the linear prediction cepstral coefficients.

    Implementation details and description in:
    http://www.practicalcryptography.com/miscellaneous/machine-learning/tutorial-cepstrum-and-lpccs/

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from linear prediction cepstral coefficients are computed
    n_coeff : int
        Number of coefficients

    Returns
    -------
    nd-array
        Linear prediction cepstral coefficients

    """
    # 12-20 cepstral coefficients are sufficient for speech recognition
    lpc_coeffs = lpc(signal, n_coeff)

    if np.sum(lpc_coeffs) == 0:
        return tuple(np.zeros(len(lpc_coeffs)))

    # Power spectrum
    powerspectrum = np.abs(np.fft.fft(lpc_coeffs)) ** 2
    lpcc_coeff = np.fft.ifft(np.log(powerspectrum))

    return tuple(np.abs(lpcc_coeff))


# @set_domain("domain", "spectral")
# def spectral_entropy(signal, fs):
#     """Computes the spectral entropy of the signal based on Fourier transform.

#     Feature computational cost: 1

#     Parameters
#     ----------
#     signal : nd-array
#         Input from which spectral entropy is computed
#     fs : int
#         Sampling frequency

#     Returns
#     -------
#     float
#         The normalized spectral entropy value

#     """
#     # TODO: this norm is copied form original, but feels weird, check if necessary
#     sig = signal - np.expand_dims(np.mean(signal, axis=-1), axis=-1)
#     f, fmag = calc_fft(sig, fs)

#     power = fmag ** 2
#     prob = power / np.expand_dims(np.sum(power, axis=-1), axis=-1)

#     return entropy_vectorized(prob)


@set_domain("domain", "spectral")
@set_domain("tag", "eeg")
@vectorize
def spectral_entropy(signal, fs):
    """Computes the spectral entropy of the signal based on Fourier transform.

    Feature computational cost: 1

    Parameters
    ----------
    signal : nd-array
        Input from which spectral entropy is computed
    fs : float
        Sampling frequency

    Returns
    -------
    float
        The normalized spectral entropy value

    """
    # Removing DC component
    sig = signal - np.mean(signal)

    f, fmag = calc_fft(sig, fs)

    power = fmag ** 2

    if power.sum() == 0:
        return 0.0

    prob = np.divide(power, power.sum())

    prob = prob[prob != 0]

    # If probability all in one value, there is no entropy
    if prob.size == 1:
        return 0.0

    return -np.multiply(prob, np.log2(prob)).sum() / np.log2(prob.size)


@set_domain("domain", "spectral")
@set_domain("tag", "eeg")
@vectorize
def wavelet_entropy(signal, function=scipy.signal.ricker, widths=np.arange(1, 10)):
    """Computes CWT entropy of the signal.

    Implementation details in:
    https://dsp.stackexchange.com/questions/13055/how-to-calculate-cwt-shannon-entropy
    B.F. Yan, A. Miyamoto, E. Bruhwiler, Wavelet transform-based modal parameter identification considering uncertainty

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Input from which CWT is computed
    function :  wavelet function
        Default: scipy.signal.ricker
    widths :  nd-array
        Widths to use for transformation
        Default: np.arange(1,10)

    Returns
    -------
    float
        wavelet entropy

    """
    if np.sum(signal) == 0:
        return 0.0

    cwt = wavelet(signal, function, widths)
    energy_scale = np.sum(np.abs(cwt), axis=1)
    t_energy = np.sum(energy_scale)
    prob = energy_scale / t_energy
    w_entropy = -np.sum(prob * np.log(prob))

    return w_entropy


@set_domain("domain", "spectral")
@set_domain("tag", ["eeg", "ecg"])
@vectorize
def wavelet_abs_mean(signal, function=scipy.signal.ricker, widths=np.arange(1, 10)):
    """Computes CWT absolute mean value of each wavelet scale.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Input from which CWT is computed
    function :  wavelet function
        Default: scipy.signal.ricker
    widths :  nd-array
        Widths to use for transformation
        Default: np.arange(1,10)

    Returns
    -------
    tuple
        CWT absolute mean value

    """
    return tuple(np.abs(np.mean(wavelet(signal, function, widths), axis=1)))


@set_domain("domain", "spectral")
@set_domain("domain", "eeg")
@vectorize
def wavelet_std(signal, function=scipy.signal.ricker, widths=np.arange(1, 10)):
    """Computes CWT std value of each wavelet scale.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Input from which CWT is computed
    function :  wavelet function
        Default: scipy.signal.ricker
    widths :  nd-array
        Widths to use for transformation
        Default: np.arange(1,10)

    Returns
    -------
    tuple
        CWT std

    """
    return tuple((np.std(wavelet(signal, function, widths), axis=1)))


@set_domain("domain", "spectral")
@set_domain("tag", "eeg")
@vectorize
def wavelet_var(signal, function=scipy.signal.ricker, widths=np.arange(1, 10)):
    """Computes CWT variance value of each wavelet scale.

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Input from which CWT is computed
    function :  wavelet function
        Default: scipy.signal.ricker
    widths :  nd-array
        Widths to use for transformation
        Default: np.arange(1,10)

    Returns
    -------
    tuple
        CWT variance

    """
    return tuple((np.var(wavelet(signal, function, widths), axis=1)))


@set_domain("domain", "spectral")
@set_domain("tag", "eeg")
@vectorize
def wavelet_energy(signal, function=scipy.signal.ricker, widths=np.arange(1, 10)):
    """Computes CWT energy of each wavelet scale.

    Implementation details:
    https://stackoverflow.com/questions/37659422/energy-for-1-d-wavelet-in-python

    Feature computational cost: 2

    Parameters
    ----------
    signal : nd-array
        Input from which CWT is computed
    function :  wavelet function
        Default: scipy.signal.ricker
    widths :  nd-array
        Widths to use for transformation
        Default: np.arange(1,10)

    Returns
    -------
    tuple
        CWT energy

    """
    cwt = wavelet(signal, function, widths)
    energy = np.sqrt(np.sum(cwt ** 2, axis=1) / np.shape(cwt)[1])

    return tuple(energy)
