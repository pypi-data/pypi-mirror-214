from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output
from AnyQt.QtWidgets import QAction, QFileDialog, QPushButton
from PyQt5.QtCore import Qt, QEvent
from drb.drivers.file import DrbFileNode
from drb.drivers.json import JsonNodeFactory, JsonBaseNode

import io
import yaml
import pickle
from Orange.data import Table
from Orange.data.pandas_compat import table_from_frame
from .DTDL import TwinModel

from azure.identity import ClientSecretCredential
from azure.core.exceptions import HttpResponseError
from azure.digitaltwins.core import DigitalTwinsClient


class OWAzureTwins(widget.OWWidget):
    name = "Azure Twins"
    description = "Query available twins from Microsoft Azure Platform"
    icon = "icons/azure.svg"
    priority = 100
    twins = []
    models = []
    current_path = None
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Outputs:
        output = Output("Twin", TwinModel, auto_summary=False)

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
                        box="Select Config File:")
        hbox = gui.hBox(vbox)
        hbox.layout().addWidget(browse_button)

        self.query_button = gui.button(
            vbox, self, "Query Service",
            autoDefault=False,
            callback=self.query_service
        )

        self.box = gui.widgetBox(self.controlArea, " ")
        gui.rubber(self.controlArea)

        self.twins_combobox = gui.comboBox(
            self.box, self, "", items=self.twins,
            label="Select Twin:",
            orientation=Qt.Horizontal,
            contentsLength=8,
        )
        self.twins_combobox.activated.connect(self.create_twin)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self,
                        "auto_commit", "Send", box=False)

    def query_service(self):

        if self.current_path:
            with open(self.current_path) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)

        try:
            # Load the cached list of twins from disk
            with open('twins.pickle', 'rb') as f:
                self.twins = pickle.load(f)
                self.twins_combobox.clear()
                self.twins_combobox.addItems(
                    [twin['$dtId'] for twin in self.twins])
                for twin in self.twins:
                    print(twin)

        except FileNotFoundError:
            # Authenticate with Azure Digital Twins
            try:
                credentials = ClientSecretCredential(
                    tenant_id=config['tenant_id'],
                    client_id=config['client_id'],
                    client_secret=config['client_secret']
                )
                endpoint = config['endpoint']
                digital_twin_client = DigitalTwinsClient(endpoint, credentials)

                query_expression = "SELECT * FROM digitaltwins"

                # Get twins
                try:
                    self.twins = list(
                        digital_twin_client.query_twins(query_expression))
                    # Get the models
                    for twin in self.twins:
                        model_id = twin['$metadata']['$model']
                        model = digital_twin_client.get_model(model_id)
                        self.models.append(model)

                    # Cache the list of twins to disk
                    with open('twins.pickle', 'wb') as f:
                        pickle.dump(self.twins, f)

                except HttpResponseError as e:
                    print("\nThis HTTP request has failed: {}".format(e))

                self.twins_combobox.clear()
                self.twins_combobox.addItems(
                    [twin['$dtId'] for twin in self.twins])

            except AzureError as ex:
                print('Failed to authenticate with Azure'
                      ' Digital Twins: {}'.format(ex))

    def create_twin(self):
        twin_id = self.twins_combobox.currentIndex()
        twin = self.twins[twin_id]
        model_id = twin['$metadata']['$model']
        display_name = ''
        for m in self.models:
            if m['Id'] == model_id:
                model = m
                display_name = model['display_name'][0]

        contents = []
        for k, v in twin.items():
            if k not in ['$dtId', '$etag', '$metadata']:
                content = {'name': k, 'value': v}
                contents.append(content)

        self.model = TwinModel(
            model_id=model_id,
            display_name=display_name,
            contents=contents
        )

        self.commit.deferred()

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """

        if self.model:
            self.Outputs.output.send(self.model)

        else:
            self.Outputs.output.send(None)

    def __show_open_dialog_file(self):
        self.current_path, f = QFileDialog.getOpenFileName(
            self, 'Select directory/file',
            'some/default/path/', 'Product files'
            '(*.yaml *.yml)')


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWAzureTwins).run()
