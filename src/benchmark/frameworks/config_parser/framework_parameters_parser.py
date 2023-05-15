class FrameworkParameters:
    @staticmethod
    def _parameter_is_not_none(parameter):
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

    def _mean_is_correct(self, mean):
        mean_check = mean.replace('[', '').replace(']', '').replace(',', ' ').split()
        if len(mean_check) != 3:
            return False
        for i in mean_check:
            if not self._float_value_is_correct(i):
                return False
        return True

    @staticmethod
    def _channel_swap_is_correct(channel_swap):
        set_check = {'0', '1', '2'}
        set_in = set(channel_swap.split())
        return set_in == set_check
