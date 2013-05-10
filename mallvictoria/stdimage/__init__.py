# -*- coding: utf-8 -*-
"""__init__.py: Django apps package stdimage"""

__author__ = 'Marc Garcia'
__version_info__ = (0, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__date__ = '2011/06/22 09:59:51'
__credits__ = ['Marc Garcia', 'Steven Klass']
__license__ = 'GNU Lesser General Public License'

from fields import StdImageField

try:
    from south.modelsinspector import add_introspection_rules
    rules = [
        (
            (StdImageField,),
            [],
            {
                "size": ["size", {"default": None}],
                "thumbnail_size": ["thumbnail_size", {"default": None}],
                "upload_to": ["upload_to", {"default": None}],
            },
        )
    ]
    add_introspection_rules(rules, ["^stdimage\.fields"])
except ImportError:
    pass
