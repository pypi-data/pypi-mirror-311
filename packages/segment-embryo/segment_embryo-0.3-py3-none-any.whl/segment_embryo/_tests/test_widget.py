import numpy as np
from vispy.testing import assert_true

from segment_embryo._widget import (
    EmbryoSegmentationWidget
)


# capsys is a pytest fixture that captures stdout and stderr output streams
def test_example_q_widget(make_napari_viewer, capsys):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((1, 1, 1)))

    # create our widget, passing in the viewer
    my_widget = EmbryoSegmentationWidget(viewer)

    assert my_widget.scalingFactorInput
    assert my_widget.membranesLayerCombo
    assert my_widget.nucleiLayerCombo
