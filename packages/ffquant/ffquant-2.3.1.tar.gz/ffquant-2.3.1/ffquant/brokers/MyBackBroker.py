from backtrader.brokers import BackBroker
from backtrader.utils import AutoOrderedDict

__ALL__ = ['MyBackBroker']

class MyBackBroker(BackBroker):
    def __init__(self):
        super(MyBackBroker, self).__init__()

    def submit(self, order, check=True, **kwargs):
        o = super().submit(order, check)
        info = AutoOrderedDict()
        info.symbol = order.data.p.symbol
        info.is_close_pos = kwargs.get('is_close_pos', False)
        order.info = info
        return o