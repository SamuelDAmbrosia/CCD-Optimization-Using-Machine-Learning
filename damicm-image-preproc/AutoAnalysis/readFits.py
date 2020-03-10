import sys
import numpy as np
from astropy.io import fits
import palettable


def read(filename):
    """
	Reads the fits file from filename and returns the header information and 
	a numpy array of the data (nrows, ncolumns, nskips)
	"""

    fitsImg = fits.open(filename)

    # Get numpy of rows, columns, and skips
    header = fitsImg[0].header
    nrows = header["NAXIS2"]

    # Average image fits does not have an NDCMS key
    try:
        nskips = header["NDCMS"]
    except KeyError:
        nskips = 1

    ncolumns = header["NAXIS1"] // nskips

    # Get data and put it in the shape we want
    data = fitsImg[0].data
    data = np.reshape(data, (nrows, nskips, ncolumns), "F")
    data = np.transpose(data, (0, 2, 1))

    # Include the average image in the output array
    data = np.append(data, np.mean(data, -1, keepdims=True), axis=-1)

    fitsImg.close()
    return header, data


if __name__ == "__main__":
    # Testing the read function
    fitsFilename = "../Img_11.fits"
    header, data = read(fitsFilename)
    colors = palettable.scientific.sequential.Devon_20.mpl_colormap

    for key, val in header.items():
        print(key + ": " + str(val))

    import matplotlib.pyplot as plt

    img = data[:, :, -1]
    print(data.shape)
    imgMean = np.mean(img)
    imgStd = np.std(img)
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    cax = ax.imshow(
        img, vmin=imgMean - 3 * imgStd, vmax=imgMean + 3 * imgStd, cmap=colors
    )

    # n = 5
    # fig, axs = plt.subplots(n, n)
    # print(axs.shape)
    # for i in range(axs.size):
    # 	xi = i // n
    # 	yi = i % n
    # 	img = data[:,:,i]
    # 	imgMean = np.mean(img)
    # 	imgStd = np.std(img)
    # 	cax = axs[xi,yi].imshow(img, aspect="auto", vmin=imgMean - 3*imgStd, vmax=imgMean + 3*imgStd, cmap=colors)
    fig.colorbar(cax, ax=ax)

    # Image histogram
    figH, axH = plt.subplots(1, 1, figsize=(12, 8))
    bins = np.linspace(imgMean - 3 * imgStd, imgMean + 3 * imgStd, 1000)
    # bins = np.linspace(19400, 19500, 200)
    axH.hist(img.flatten(), bins=bins)
    axH.set_xlabel("Pixel Value", fontsize=16)
    axH.set_yscale("log")

    print(imgMean)
    print(imgStd)
    plt.show()
