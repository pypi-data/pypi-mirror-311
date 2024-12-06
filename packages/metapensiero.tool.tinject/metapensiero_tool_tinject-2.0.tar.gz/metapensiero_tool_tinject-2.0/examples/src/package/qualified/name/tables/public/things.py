# -*- coding: utf-8 -*-
# :Project:   package.qualified.name -- SA definition of table public.things
# :Created:   lun 11 nov 2024 12:10:44 CET
# :Author:    Lele Gaifax <lele@example.com>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2024 Lele Gaifax
#

import sqlalchemy as sa
from .. import meta, translatable_string as _


things = meta.TimeStampedTable('things', meta.metadata,
    #sa.Column('title', meta.text_t,
    #          nullable=False,
    #          info=dict(label=_('Title'),
    #                    hint=_('The title of the entry'))),
    schema='public')
