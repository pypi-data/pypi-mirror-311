import time
from typing import TYPE_CHECKING

import numpy as np
from PyQt5.QtWidgets import QGroupBox, QFormLayout, QVBoxLayout
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget
from segment_embryo.napari_util import NapariUtil
from segment_embryo.qtutil import WidgetTool
from napari.utils.events import Event
from napari.layers.image.image import Image
from segment_embryo.segmentation import runCellposeOnScaledImage
from napari.qt.threading import create_worker
from napari.utils import progress

if TYPE_CHECKING:
    import napari


class EmbryoSegmentationWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self.viewer = viewer
        self.napariUtil = NapariUtil(self.viewer)
        self.setLayout(QVBoxLayout())
        self.progressThread = None
        self.membranesLayerCombo = None
        self.nucleiLayerCombo = None
        self.scalingFactorInput = None
        self.scalingFactor = 8
        self.layout().addWidget(self.getSegmentEmbryoWidget())
        self.viewer.layers.events.inserted.connect(self.onLayerAddedOrRemoved)
        self.viewer.layers.events.removed.connect(self.onLayerAddedOrRemoved)
        self.worker = None


    def getSegmentEmbryoWidget(self):
        layerNames = [layer.name for layer in self.viewer.layers]
        groupBox = QGroupBox("Embryo Segmentation")
        formLayout = QFormLayout()
        inputImageLabel, self.membranesLayerCombo = WidgetTool.getComboInput(self,
                                                                        "input image: ",
                                                                        layerNames)
        nucleiImageLabel, self.nucleiLayerCombo = WidgetTool.getComboInput(self,
                                                                        "nuclei image: ",
                                                                        layerNames)
        scalingFactorLabel, self.scalingFactorInput =  WidgetTool.getLineInput(self,
                                                                        "scaling factor: ",
                                                                        self.scalingFactor,
                                                                               50)
        formLayout.addRow(inputImageLabel, self.membranesLayerCombo)
        formLayout.addRow(nucleiImageLabel, self.nucleiLayerCombo)
        formLayout.addRow(scalingFactorLabel, self.scalingFactorInput)
        btn = QPushButton("run")
        btn.clicked.connect(self._on_click)
        verticalLayout = QVBoxLayout()
        verticalLayout.addLayout(formLayout)
        verticalLayout.addWidget(btn)
        groupBox.setLayout(verticalLayout)
        return groupBox


    def _on_click(self):
        membranesLayerName = self.membranesLayerCombo.currentText()
        nucleiLayerName = self.nucleiLayerCombo.currentText()
        membranes = self.napariUtil.getDataOfLayerWithName(membranesLayerName)
        nuclei = self.napariUtil.getDataOfLayerWithName(nucleiLayerName)
        scale = self.viewer.layers[membranesLayerName].scale
        self.scalingFactor = int(self.scalingFactorInput.text())
        cp_worker = runCellposeOnScaledImage(
            membranes,
            nuclei,
            scale=scale,
            scaleFactor=self.scalingFactor
        )
        cp_worker.returned.connect(self._new_segmentation)
        cp_worker.start()
        self.worker = cp_worker
        self.progressThread = IndeterminateProgressThread("Segmenting embryo...")
        self.progressThread.start()


    def onLayerAddedOrRemoved(self, event: Event):
        self.updateLayerSelectionComboBoxes()


    def updateLayerSelectionComboBoxes(self):
        comboBoxes = [self.membranesLayerCombo, self.nucleiLayerCombo]
        layerNames = [layer.name for layer in self.viewer.layers if isinstance(layer, Image)]
        for comboBox in comboBoxes:
            WidgetTool.replaceItemsInComboBox(comboBox, layerNames)


    def _new_segmentation(self, mask):
        membranesLayerName = self.membranesLayerCombo.currentText()
        name = "Labels of " + membranesLayerName
        maskImage = np.array([mask])
        self.viewer.add_labels(maskImage, name=name)
        self.viewer.layers[name].scale = self.viewer.layers[membranesLayerName].scale[-4: ]
        self.viewer.layers[name].translate = self.viewer.layers[membranesLayerName].translate[-3: ]
        self.viewer.layers[name].units = self.viewer.layers[membranesLayerName].units[-4: ]
        self.progressThread.stop()



class IndeterminateProgressThread:
    """An indeterminate progress indicator that moves while an operation is
    still working.
    """

    def __init__(self, description):
        """Create a new indetermined progress indicator with the given
        description.
        """
        self.worker = create_worker(self.yieldUndeterminedProgress)
        self.progress = progress(total=0)
        self.progress.set_description(description)

    def yieldUndeterminedProgress(self):
        """The progress indicator has nothing to do by himself, so just
        sleep and yield, while still running.
        """
        while True:
            time.sleep(0.05)
            yield

    def start(self):
        """Start the operation in a parallel thread"""
        self.worker.start()

    def stop(self):
        """Close the progress indicator and quite the parallel thread.
        """
        self.progress.close()
        self.worker.quit()