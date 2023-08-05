import numpy as np
from . import _filter
from skimage.filters import gaussian
from skimage.transform import rescale, downscale_local_mean
import functools


def adaptive_denoise(img: np.ndarray, ada_interval=(2, 3, 3), flare_interval=(2, 8, 8),
                     ada_sampling=3, flare_sampling=8, flare_weight=.02, atten_depth=4., flare_x=True, flare_y=True):
    """
    Remove background noise and flare.

    :param img: 3D neuron fluorescent image array, 16bit.
    :param ada_interval: stride for adaptive threshold.
    :param flare_interval: stride for removing flare effect.
    :param ada_sampling: number of steps for adaptive threshold.
    :param flare_sampling: number of steps for removing flare effect.
    :param flare_weight: the weight of flare reduction.
    :param atten_depth: the unit attenuation distance of the flare.
    :param flare_x: whether calculate flare along x, when both do, take bigger.
    :param flare_y: whether calculate flare along y, when both do, take bigger.
    :return: denoised 3D image array, 16bit.
    """
    return _filter.adaptive_denoise(img, ada_interval, flare_interval, ada_sampling, flare_sampling, flare_weight, atten_depth,
                                    flare_x, flare_y)


def adaptive_denoise_16to8(img: np.ndarray, lower: int | float = 0, upper: int | float = 255, **kwargs):
    """
    The adaptive denoising is designed for 16bit raw image with full details.
    This wrapper appends a bit conversion afterward, by clipping and linear scaling.

    keyword arguments are passed to `adaptive_denoise`

    :param img: 3D neuron fluorescent image array, 16bit.
    :param lower: the lower threshold or quantile.
    :param upper: the lower threshold or quantile.
    :return: denoised 3D image array, 8bit.
    """
    assert img.dtype == np.uint16
    assert img.ndim == 3
    img = adaptive_denoise(img, **kwargs)
    if type(lower) is float:
        lower = np.quantile(img, lower)
    if type(upper) is float:
        upper = np.quantile(img, upper)
    return ((img.clip(lower, upper) - lower) / (upper - lower) * 255).astype(np.uint8)


def gauss_attenuation_filter(img: np.ndarray, sigma=32, attenuation=.1, truncate=2., warmup=32):
    """
    Fast and stable flare cancelling and overall denoising.

    :param img: 3D image array.
    :param sigma: gaussian sigma, scalar or a tuple of 2 scalar.
    :param attenuation: cancel weight of each z slice, the bigger the more removal.
    :param truncate: this many times of sigma will be truncated to speed up gaussian.
    :param warmup: the times that the gaussian is repeated on the init slice to warm up the filter.
    :return: image with flare removed
    """

    gpool = np.zeros([img.shape[1], img.shape[2]], dtype=float)
    out = np.zeros_like(img)
    for i in range(warmup):
        out[-1] = (img[-1] - gpool * attenuation).clip(0).astype(np.uint16)
        gpool = gaussian(gpool + out[-1], sigma, preserve_range=True, truncate=truncate)
    for i in range(img.shape[0] - 1, -1, -1):
        out[i] = (img[i] - gpool * attenuation).clip(0).astype(np.uint16)
        gpool = gaussian(gpool + out[i], sigma, preserve_range=True, truncate=truncate)
    return out


def adaptive_sectional_feedforward_filter(img: np.ndarray, sigma=10., truncate=3., scaling=1, suppression=.8):
    """
    cancel flare and background noise. More adaptive canceling, and its effect can be tuned.

    :param img: 3D image array.
    :param sigma: gaussian sigma, scalar or a tuple of 2 scalar.
    :param truncate: this many times of sigma will be truncated to speed up gaussian.
    :param scaling: downsampling times to speed up.
    :param suppression: 0-1, suppress the canceling effect.
    :return: processed image
    """
    diffuse = functools.partial(gaussian, sigma=sigma / scaling, preserve_range=True, truncate=truncate)
    downscale = functools.partial(downscale_local_mean, factors=scaling)
    upscale = functools.partial(rescale, scale=scaling)

    out = np.zeros_like(img)
    gpool = diffuse(downscale(img[-1]))
    for i in range(1, img.shape[0]):
        i = img.shape[0] - i - 1
        m = img[i].mean() / gpool.mean() * suppression
        out[i] = (img[i] - upscale(m * gpool)).clip(0)
        gpool = diffuse(downscale(out[i]) + gpool)
    return out