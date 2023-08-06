from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output
from AnyQt.QtWidgets import QAction, QFileDialog, QPushButton
from drb.drivers.file import DrbFileNode
from drb.drivers.json import JsonNodeFactory, JsonBaseNode
import io
from Orange.data import Table
from Orange.data.pandas_compat import table_from_frame


class TwinModel:
    def __init__(self, model_id, display_name, contents):
        self.id = model_id
        self.display_name = display_name
        self.contents = contents


class OWLoadDTDL(widget.OWWidget):
    name = "Load DTDL"
    description = "Supports DTDL in json format," \
                  " generates a Twin Model to be used for" \
                  " generating Digital Twin(s)"
    icon = "icons/DTDL.svg"
    priority = 90
    statemachine = None
    current_path = None
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Outputs:
        output = Output("TwinModel", TwinModel, auto_summary=False)

    def __init__(self):
        super().__init__()
        self.output = None

        browse_action = QAction(
            self,
            text="\N{HORIZONTAL ELLIPSIS}",
        )

        browse_action.triggered.connect(self.__show_open_dialog_file)
        browse_button = QPushButton(
            browse_action.iconText(),
            clicked=browse_action.trigger
        )

        vbox = gui.vBox(self.controlArea,
                        box="Select File:")
        hbox = gui.hBox(vbox)
        hbox.layout().addWidget(browse_button)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """

        if self.current_path:
            model = _create_twin_model(self.current_path)
            self.Outputs.output.send(model)

        else:
            self.Outputs.output.send(None)

    def __show_open_dialog_file(self):
        self.current_path, f = QFileDialog.getOpenFileName(
            self, 'Select directory/file',
            'some/default/path/', 'Product files'
            '(*.json)')
        if self.current_path:
            self.commit.deferred()


def _create_twin_model(file):

    json_node = JsonNodeFactory().create(file)

    # Access the properties of the JSON node to create a Python object
    model_id = json_node[0]["@id"].value
    display_name = json_node[0]["displayName"].value

    contents = json_node[0]["contents", :]

    # for content in contents:
    #     print(content["name"].value)

    model = TwinModel(
        model_id=model_id,
        display_name=display_name,
        contents=contents
    )

    return model


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWLoadDTDL).run()
