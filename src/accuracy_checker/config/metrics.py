class metric:
    def __init__(self, data):
        TYPE_TAG = 'type'
        self.type = data[TYPE_TAG]

    def get_type(self):
        return self.type

    @staticmethod
    def get_metric(data):
        TYPE_TAG = 'type'
        type = data[TYPE_TAG]
        if type == 'accuracy':
            return metric_accuracy(data)
        else:
            return metric(data)


class metric_accuracy(metric):
    def __init__(self, data):
        super().__init__(data)
        TOP_K_TAG = 'top_k'
        self.top_k = data[TOP_K_TAG]

    def get_type(self):
        return self.type + '@top_k_' + str(self.top_k)
