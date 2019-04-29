from . import api

v1 = [
    (
        r'positioning/locate',
        api.LocateView,
        'positioning-locate'
    ),
    (
        r'positioning/beacons',
        api.BeaconViewSet,
        'positioning-beacons'
    ),
]
