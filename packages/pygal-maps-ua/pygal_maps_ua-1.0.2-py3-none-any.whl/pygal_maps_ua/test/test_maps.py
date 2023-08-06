# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.

from pygal_maps_ua.maps import Regions, REGIONS_UA


def test_regions():
    uamap = Regions()

    datas = {}
    for i, oblast in enumerate(REGIONS_UA):
        datas[oblast] = i

    uamap.add('regions', datas)
    q = uamap.render_pyquery()
    assert len(q('#regions .region,#dom-com .region')) == len(REGIONS_UA)
