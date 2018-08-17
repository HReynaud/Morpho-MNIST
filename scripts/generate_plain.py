import multiprocessing
import os
import timeit

import matplotlib.pyplot as plt
import numpy as np

from morphomnist import io, util
from morphomnist.morpho import ImageMorphology

DATA_ROOT = "../data/mnist"
THRESHOLD = .5
UP_FACTOR = 4


def process_image(i, img):
    start = timeit.default_timer()
    morph = ImageMorphology(img, THRESHOLD, UP_FACTOR)
    pert_img = morph.downscale(morph.binary_image)
    end = timeit.default_timer()
    print(f"[{i:5d}] Preprocessing: {1000. * (end - start):.1f} ms")
    return pert_img


if __name__ == '__main__':
    filenames = ["train-images-idx3-ubyte", "t10k-images-idx3-ubyte"]

    pool = multiprocessing.Pool()
    for filename in filenames:
        images = io.load_idx(os.path.join(DATA_ROOT, "raw", filename))

        pert_results = pool.starmap(process_image, zip(np.arange(len(images)), images),
                                    chunksize=1250)

        pert_images = np.array(pert_results)
        util.plot_digit(pert_images[0])
        plt.show()
        print(pert_images.shape)
        io.save_idx(pert_images, os.path.join(DATA_ROOT, "plain", filename) + '.gz')
    pool.close()
    pool.join()
