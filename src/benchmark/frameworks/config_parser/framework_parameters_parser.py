class FrameworkParameters:
    @staticmethod
    def _parameter_not_is_none(parameter):
        return parameter is not None

    @staticmethod
    def _int_value_is_correct(int_value):
        for i in range(len(int_value)):
            if (i < 0) or (9 < i):
                return False
        return True

    def _float_value_is_correct(self, float_value):
        for i in float_value.split('.'):
            if not self._int_value_is_correct(i):
                return False
        return True
