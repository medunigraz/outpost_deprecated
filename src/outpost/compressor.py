from compressor.filters import CompilerFilter
from django.contrib.staticfiles import finders


class DjangoLessFilter(CompilerFilter):

    def __init__(self, content, **kwargs):
        DIRS = finders.find('.', all=True)
        c = 'lessc --include-path={path} {{infile}} {{outfile}}'.format(
            path=':'.join(DIRS)
        )
        super(DjangoLessFilter, self).__init__(content, command=c, **kwargs)
