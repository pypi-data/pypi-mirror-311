from skimage.transform import rescale
from skimage.transform import resize
import numpy as np
from superqt.utils import thread_worker
from torch import no_grad


@thread_worker()
@no_grad()
def runCellposeOnScaledImage(membranes, nuclei, scale=(1,1,1), scaleFactor=8, modelType="cyto3"):
    depth, height, width = membranes.shape[-3: ]
    scaleZ, scaleY, scaleX = scale[-3: ]
    zFactor = scaleZ / scaleX
    if len(scale) < 4:
        smallNuclei = rescale(nuclei, (zFactor / scaleFactor, 1.0 / scaleFactor, 1.0 / scaleFactor))
        smallMembranes = rescale(membranes, (zFactor / scaleFactor, 1.0 / scaleFactor, 1.0 / scaleFactor))
    else:
        smallNuclei = rescale(nuclei, (1, zFactor / scaleFactor, 1.0 / scaleFactor, 1.0 / scaleFactor))
        smallMembranes = rescale(membranes, (1, zFactor / scaleFactor, 1.0 / scaleFactor, 1.0 / scaleFactor))
    from cellpose import models
    image = np.concatenate((smallMembranes, smallNuclei))
    CP = models.CellposeModel(model_type=modelType, gpu=True)
    masks, flows, _ = CP.eval(image, do_3D=True)
    resultMask = resize(masks, (depth, height, width), mode='constant', anti_aliasing=False,
                                                        anti_aliasing_sigma=None, preserve_range=True, order=0, cval=0)
    return resultMask

