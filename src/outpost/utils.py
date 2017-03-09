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
