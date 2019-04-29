from . import api

v1 = [
    (
        r'thesis/doctoralschool',
        api.DoctoralSchoolViewSet,
        'thesis-doctoralschool'
    ),
    (
        r'thesis/discipline',
        api.DisciplineViewSet,
        'thesis-discipline'
    ),
    (
        r'thesis/thesis',
        api.ThesisViewSet,
        'thesis-thesis'
    ),
    (
        r'thesis/search/thesis',
        api.ThesisSearchViewSet,
        'thesis-thesis-search'
    ),
]
