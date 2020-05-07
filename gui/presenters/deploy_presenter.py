class DeployPresenter(object):
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._view.buttons.addSignal.connect(self.handle_add_button)
        self._view.buttons.clearSignal.connect(self.handle_clear_button)
        self._view.dialog_add_computer.addComputerSignal.connect(self.handle_add_computer)

    def handle_add_button(self):
        self._view.show_dialog_add_computer()

    def handle_clear_button(self):
        self._view.table.clear()

    def handle_add_computer(self):
        self._model.add_computer(self._view.dialog_add_computer.get_computer())
        self._view.table.update(self._model.computers)
