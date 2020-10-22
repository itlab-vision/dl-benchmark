from .model import Model


class Models:
    def __init__(self):
        self.__models = []

    def get_models(self):
        return self.__models

    def get_models_list(self):
        models_list = []
        for model in self.__models:
            models_list.append(model.get_str())
        return models_list

    def set_models(self, models):
        self.__models.clear()
        for model in models:
            if model not in self.__models:
                self.__models.append(model)

    def add_model(self, task, name, precision, framework, model_path, weights_path):
        self.__models.append(Model(task, name, precision, framework, model_path, weights_path))

    def change_model(self, row, task, name, precision, framework, model_path, weights_path):
        self.__models[row] = Model(task, name, precision, framework, model_path, weights_path)

    def delete_model(self, index):
        self.__models.pop(index)

    def delete_models(self, indexes):
        for index in indexes:
            if index < len(self.__models):
                self.delete_model(index)

    def clear(self):
        self.__models.clear()
