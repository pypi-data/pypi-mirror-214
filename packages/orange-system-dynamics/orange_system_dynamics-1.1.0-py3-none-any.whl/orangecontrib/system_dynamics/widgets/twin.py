from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output, Input, MultiInput
from AnyQt.QtGui import QPixmap
from AnyQt.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from Orange.data import Table, Domain, ContinuousVariable
from Orange.data.pandas_compat import table_from_frame, table_to_frame
from .DTDL import TwinModel
import os
import pandas as pd


class DigitalTwin:
    def __init__(self, model):
        self.model = model
        self.properties = {}
        for content in self.model.contents:
            value = None
            try:
                name = content["name"].value
            except AttributeError:
                name = content["name"]
                value = content["value"]
            self.properties[name] = value

    def set_property(self, name, value):
        if name not in self.properties:
            raise ValueError("Property name not found in interface")
        self.properties[name] = value

    def get_property(self, name):
        if name not in self.properties:
            raise ValueError("Property name not found in interface")
        return self.properties[name]

    def get_properties(self):
        return self.properties.copy()


class OWTwin(widget.OWWidget):
    name = "Twin"
    description = "Used to create/update a digital twin from " \
                  "model following DTDL"
    icon = "icons/twin.svg"
    priority = 80

    twins = []
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Inputs:
        model = Input("TwinModel", TwinModel, auto_summary=False)
        data = MultiInput("Data", Table)

    class Outputs:
        output = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.data = {}
        self.output = None

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def _set_new_model(self, model):
        self.output = None
        self.model = model

        self.contents_box = gui.widgetBox(self.controlArea, "Contents: ")
        gui.rubber(self.controlArea)

        for content in self.model.contents:
            value = 0.0
            try:
                name = content["name"].value
            except AttributeError:
                name = content['name']
                value = content['value']

            self.__setattr__(name, value)

            gui.doubleSpin(self.contents_box, self, name, 0, 10**10,
                           decimals=2,
                           label=name
                           )

        self.button = gui.button(
            self.contents_box, self, "Update Twin",
            autoDefault=False,
            callback=self.update_twin
        )

        self.twin = DigitalTwin(self.model)

    def set_variable(self, name):

        df = table_to_frame(self.data[name])

        self.twin.set_property(name, df.iloc[0])
        time_steps = df.iloc[:, 0]

        # Get all the properties of the digital twin
        props = self.twin.get_properties()

        # create an empty dataframe with the column names as the property names
        df = pd.DataFrame(columns=list(props.keys()))

        # repeat the single row for each time step
        df = pd.concat([df] * len(time_steps), ignore_index=True)

        # set the time as the index
        df.index.name = "Time"

        # fill in the initial values
        for prop, val in props.items():
            if isinstance(val, pd.DataFrame):
                df[prop] = val.iloc[0]

            else:
                df[prop] = val

        self.output = table_from_frame(df)
        self.commit.deferred()

    @Inputs.model
    def set_model(self, model):
        if model is not None:
            self._set_new_model(model)

    @Inputs.data
    def set_data(self, _, table):
        self.data[table[0]] = table[1]
        self.set_variable(table[0])

    @Inputs.data.insert
    def insert_data(self, _, table):
        self.data[table[0]] = table[1]
        self.set_variable(table[0])

    @Inputs.data.remove
    def remove_data(self, index):
        if index == 0:
            self.data = {}

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        if self.output:
            self.Outputs.output.send(self.output)

        else:
            self.Outputs.output.send(None)

    def update_twin(self):
        # Set the temperature property to a value
        for prop in self.twin.properties:

            value = self.__getattribute__(prop)
            self.twin.set_property(prop, value)

        # Get all the properties of the digital twin
        props = self.twin.get_properties()
        print(props)

        # create a DataFrame with a single row for the initial values
        df = pd.DataFrame(data=[props], index=[0])

        self.output = table_from_frame(df)
        self.commit.deferred()


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWTwin).run()
