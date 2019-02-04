import locale

from IPy import IP


class IPList(list):

    def __init__(self, addresses):
        super(IPList, self).__init__()
        for address in addresses:
            self.append(IP(address))

    def __contains__(self, address):
        for net in self:
            if address in net:
                return True
        return False


class LocaleManager:
    def __init__(self, localename):
        self.name = localename

    def __enter__(self):
        self.orig = locale.setlocale(locale.LC_CTYPE)
        locale.setlocale(locale.LC_ALL, self.name)

    def __exit__(self, exc_type, exc_value, traceback):
        locale.setlocale(locale.LC_ALL, self.orig)
