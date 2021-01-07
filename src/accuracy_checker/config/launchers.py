class launcher:
    def __init__(self, data):
        FRAMEWORK_TAG = 'framework'
        DEVICE_TAG = 'device'
        ADAPTER_TAG = 'adapter'

        self.framework = data[FRAMEWORK_TAG]
        self.device = data[DEVICE_TAG]
        self.adapter = data[ADAPTER_TAG]
