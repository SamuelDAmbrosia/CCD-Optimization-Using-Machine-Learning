# damicm-image-preproc

Information on the image preprocessing and intial characterization of DAMIC-M skipper images. 

## Requirements

This code uses Python3 and the packages listed in requirements.txt to run. It is recommended that you use a virtualenv. To set up a virtual environment, from the code directory, run:

```
virtualenv env --python=python3 # creates virtual environment in ./env/
pip install -r requirements.txt # installs packages
source env/bin/activate # activates the environmnet
``` 

`python3` should be replaced with the location of the python executable you want to use. For ease of use, you may wish to create an alias to activate the environment and run the code; if so, add the following command to your `.bashrc` or `.bash_profile`:

```
alias imgproc='source <path-to-code>/env/bin/activate; python <path-to-code>/image_preproc.py'

```

So that you can just run `imgproc [options]` from any directory.

## Usage

This code is intended to process images stored in fits files to make a quick evaluation on the quality of the image. The usage is:

```python image_preproc.py```

By default, the code searchs for any files matching "Img_[0-9]+.fits" in the current working directory, performs a series of desired computations, and writes the result in a tabulated form in the file "image_preproc_out.txt".

Additionally, the following command line arguments can be used:

```
-f --filenames <filenames>
-o --output <outfilename>
-d --directory <dir>
-a --all
-r --recursive
-p --print
-h --help
```

The arguments for `-f` can be a list of filenames (also supports wildcard matching) or a regex pattern, and all files in the directory that match the pattern will be processed. `-d` is the directory to search for files to process. By default, only files where the processed results are not in the `<outfilename>` will be processed; to process all files that match, use the `-a` flag. To print to terminal instead of saving to file, use the `-p` flag.

Use `python image_preproc.py -h` for help.

## Explanation of variables

When the data is read, the pixel values are stored in a numpy array with shape `(nrows, ncols, nskips+1)`, where the `data[:, :, -1]` is the average image, and all other z-slices are the raw pixel data. 

The output of this code is a table of variables for each processed file. Below is an explanation for what these variables mean:

- `filename` - file processed.
- `nskips` - number of NDCM made on the image. Extracted from the .fits header information.
- `aveImgS` - the entropy of the average image. Entropy is defined as $-\sum_i p_i \log (p_i)$ where $p_i$ is the probability of a pixel measurement calculated from the histogram of the image. 
- `dSdskip` - The rate of change of entropy as a function of skips. Slope is computed from a fit to the entropy of each individual image. Units are millidits and values of $<-10$ typically corresponde to charge lost between skips. 
- `imgNoise` - average noise (in ADU) of the images taken (if more than one skip used). Fit to the central distribution of image.
- `skNoise` - noise of the individual peaks in the average image. Code looks for minima in a smoothed histogram to set the bounds on the fitting. If two minima are not found (i.e. no single electron peaks) the fit returns -1. 
- `pixVar` - variance of a single pixel over the number of skips. Selects a random `(i,j)` pixel and computes the variance of all skips with that coordinate; repeates the process over a number of different coordinates and returns the median of that distribution.
- `clustVar` - takes a cluster of pixels in a given image (and the same `npixels` as used to compute `pixVar`) and computes the variance of the pixel values in that cluster. Repeats for a number of trials and returns the median of that distribution. Should be used to compare to `pixVar` and the two values should be equal/similar if things are working.
- `tailRatio` - ratio of the number of events in the less than $4\sigma$ from the central noise peak to the number of expected events if the pixel distribution was drawn from a Gaussian source. Value is a proxy for tracks/charge transfer.

If the return of any value is -1, it means the value doesn't make sense (not enough skips for example) or a fit/computation failed. Additionally in the values that are fit, the fit uncertainty is also returned, so use that to evaluate the quality of the fit. 
