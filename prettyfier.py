class Prettyfier:
    _columns = []

    def __init__(self, config):
        """
         :type config: config.Config
        """
        self._config = config
        self._columns = [0] * self._config.bars

    def update_heights(self, data):
        i = 0
        for height in data:
            height -= 8.0
            height /= 5
            if height < 0.05:
                height = 0
            elif height > 1.0:
                height = 1.0
            if height < self._columns[i]:
                self._columns[i] = self._columns[i] * self._config.decay
            else:
                self._columns[i] = height
            i += 1

    def get_heights(self):
        return self._columns
