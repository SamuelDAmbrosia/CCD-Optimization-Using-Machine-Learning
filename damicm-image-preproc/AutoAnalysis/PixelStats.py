import numpy as np
import constants as c
import readFits
import matplotlib.pyplot as plt
import scipy.stats


def singlePixelVariance(skImage, ntrials=200):
    """
		Computes the median variance of the single pixel over multiple skips
		Inputs:
			skImage - (nrows, ncolumns, nskips) 3D numpy array containing pixel values
			ntrials - number of random pixels to sample in creating the variance distribution of single pixles
		Outputs:
			medianVarianceDist - median of the single pixel variance distributions (to avoid tails cause by clusters)
			varianceDist - (ntrials, ) 1D numpy array of the variance of the different pixles sampled
	"""

    # If we don't have the correct dimensions or not enough skips, returns -1
    if len(skImage.shape) != 3 or skImage.shape[-1] == 1:
        return -1.0, []

    nrows = skImage.shape[0]
    ncols = skImage.shape[1]

    # Get a random sample of points within the
    rowSamples = np.random.uniform(0, nrows, ntrials).astype(int)
    colSamples = np.random.uniform(0, ncols, ntrials).astype(int)

    # Compute the variance of every pixel in the image
    skImageVar = np.var(skImage[:, :, c.SKIPPER_OFFSET :], axis=-1)

    varianceDist = skImageVar[rowSamples, colSamples]

    return np.median(varianceDist), varianceDist


def imageNoiseVariance(image, npixels, ntrials=200):
    """
		Computes the variance of a region of the image. Performs variance calculation over a series (ntrials) of different
		regions (defined in size by npixels) and returns the median variance.
		Inputs:
			image - 2 or 3D numpy array (nrows, ncols) or (nrows, ncols, nskips) containing pixel values of an image
			npixels - the number of pixels in the cluster to take the variance over
			ntrials - size of the distribution
		Outputs
			medianPixelNoiseVarDist - double, the median value of the distribution of the ntrials different variances
			pixelNoiseVarDist - (ntrials, ) numpy array, full distribution of the variance
	"""

    # Get size of image
    nrows = image.shape[0]
    ncols = image.shape[1]
    nskips = 1 if len(image.shape) == 2 else image.shape[-1]

    # Create pixel array
    # If we have less than two, we can't construct the variance of the cluster
    if npixels < 2:
        return -1.0, []

    rowIndex, colIndex = generatePixelArray(npixels, nrows, ncols, ntrials)

    # Generate skip image index (ntrials, npixels) array (same index for a given sample number)
    if nskips > c.SKIPPER_OFFSET:
        skipIndex = np.random.uniform(c.SKIPPER_OFFSET, nskips, ntrials).astype(int)
        skipIndex = np.reshape(np.repeat(skipIndex, npixels), (ntrials, npixels))

    # If we have a single image (2D, no skip axis) or only two skips
    if len(image.shape) == 2:
        pixelValues = image[rowIndex, colIndex]
    elif nskips <= c.SKIPPER_OFFSET:
        # If for some reason we have less skips than the number of "bad" skips, we use only one of the images.
        # But this shouldn't really happen
        pixelValues = image[rowIndex, colIndex, 0]
    else:
        pixelValues = image[rowIndex, colIndex, skipIndex]

    # Get the variance of the pixel values for all the different trials
    pixelNoiseVarDist = np.var(pixelValues, axis=1)
    return np.median(pixelNoiseVarDist), pixelNoiseVarDist


def generatePixelArray(npixels, nrows, ncolumns, ntrials):
    """
	Generates a cluster of adjacent pixels with npixels in the array. Tries to make it as square as possible
	Inputs:
		npixels - int, how many pixels in the clusetr
		nrows - int, max number of rows in the image (used to revent IndexErrors)
		ncolumns - int, max number of columns in the image
		ntrials - int, number of clusters to generate
	Outputs:
		rowIndex - (ntrials, npixels) numpy array containing the row indices for ntrials different clusters
		colIndex - (ntrials, npixels)  "                "        column indices
	"""

    # Define the max and min edge length
    pixelArrayMaxEdgeRow = np.min([np.ceil(np.sqrt(npixels)), nrows])
    pixelArrayMaxEdgeCol = np.ceil(npixels / pixelArrayMaxEdgeRow)

    # Define arrays to hold the index of pixel array
    rowIndex = np.zeros((ntrials, npixels), dtype=int)
    colIndex = np.zeros((ntrials, npixels), dtype=int)

    # Start at a random spot within the image
    rowIndex[:, 0] = np.random.uniform(0, nrows - pixelArrayMaxEdgeRow, ntrials).astype(
        int
    )
    colIndex[:, 0] = np.random.uniform(
        0, ncolumns - pixelArrayMaxEdgeCol, ntrials
    ).astype(int)

    # Create pixel array to be as much of a square as possible
    for i in range(npixels):
        rowIndex[:, i] = rowIndex[:, 0] + i % pixelArrayMaxEdgeRow
        colIndex[:, i] = colIndex[:, 0] + i // pixelArrayMaxEdgeRow

    return rowIndex, colIndex


if __name__ == "__main__":

    header, data = readFits.read("../Img_20.fits")

    median, dist = singlePixelVariance(data[:, :, :-1], ntrials=100000)

    print("Individual Pixel Variance Median: %0.2f" % median)
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    med = np.median(dist)
    mad = scipy.stats.median_absolute_deviation(dist)
    bins = np.linspace(med - 3 * mad, med + 5 * mad, 200)
    ax.hist(dist, bins=bins)
    ax.set_title("Single Pixel Noise", fontsize=18)
    ax.set_xlabel("Variance of Single Pixels", fontsize=16)
    # plt.show()

    pixMed, pixDist = imageNoiseVariance(
        data[:, :, :-1], header["NDCMS"] - c.SKIPPER_OFFSET, ntrials=100000
    )
    print("Image Noise Variance Median: %0.2f" % pixMed)
    pixmed = np.median(pixDist)
    pixmad = scipy.stats.median_absolute_deviation(pixDist)
    bins = np.linspace(pixmed - 3 * pixmad, pixmed + 5 * pixmad, 200)
    figN, axN = plt.subplots(1, 1, figsize=(12, 8))
    axN.set_title("Image Noise", fontsize=18)
    axN.set_xlabel("Variance of Image Noise", fontsize=16)
    axN.hist(pixDist, bins=bins)
    print(pixDist)
    plt.show()
