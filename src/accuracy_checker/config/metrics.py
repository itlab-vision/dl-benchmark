class MetricAccuracy:
    def __init__(self, data):
        TYPE_TAG = 'type'
        TOP_K_TAG = 'top_k'

        self.type = data[TYPE_TAG]
        self.top_k = data[TOP_K_TAG]