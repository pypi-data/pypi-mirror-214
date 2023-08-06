
import numpy

from Orange.data import Table

from orangewidget import gui
from orangewidget.widget import OWBaseWidget, Input, Output


class OWDataSampler(OWBaseWidget):
    name = "Data Sampler"
    description = "Randomly selects a subset of instances from the dataset"
    icon = "icons/DataSampler.svg"

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        sample = Output("Sampled Data", Table)

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = gui.widgetLabel(box, '')

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText('%d instances in input dataset' % len(dataset))
            indices = numpy.random.permutation(len(dataset))
            indices = indices[:int(numpy.ceil(len(dataset) * 0.1))]
            sample = dataset[indices]
            self.infob.setText('%d sampled instances' % len(sample))
            self.Outputs.sample.send(sample)
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.infob.setText('')
            self.Outputs.sample.send("Sampled Data")
