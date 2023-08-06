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


from __future__ import division
from pygal.graph.map import BaseMap
import os


REGIONS_ENG = {
    'cherkasy': 'Cherkasy Oblast',
    'chernihiv': 'Chernihiv Oblast',
    'chernivtsi': 'Chernivtsi Oblast',
    'crimea': 'Autonomous Republic of Crimea',
    'dnipropetrovsk': 'Dnipropetrovsk Oblast',
    'donetsk': 'Donetsk Oblast',
    'kharkiv': 'Kharkiv Oblast',
    'kherson': 'Kherson Oblast',
    'khmelnitskyi': 'Khmelnytskyi Oblast',
    'kyiv': 'Kyiv Oblast',
    'kyivcity': 'Kyiv',
    'kirovohrad': 'Kirovohrad Oblast',
    'lviv': 'Lviv Oblast',
    'luhansk': 'Luhansk Oblast',
    'mykolaiv': 'Mykolaiv Oblast',
    'odesa': 'Odesa Oblast',
    'poltava': 'Poltava Oblast',
    'rivne': 'Rivne Oblast',
    'sevastopolcity': 'Sevastopol',
    'sumy': 'Sumy Oblast',
    'ivano-frankivsk': 'Ivano-Frankivsk Oblast',
    'ternopil': 'Ternopil Oblast',
    'zakarpattia': 'Zakarpattia Oblast',
    'vinnytsia': 'Vinnytsia Oblast',
    'volyn': 'Volyn Oblast',
    'zaporizhzhia': 'Zaporizhzhia Oblast',
    'zhytomir': 'Zhytomyr Oblast'
}

REGIONS_UA = {
    'cherkasy': 'Черкаська область',
    'chernihiv': 'Чернігівська область',
    'chernivtsi': 'Чернівецька область',
    'crimea': 'Автономна Республіка Крим',
    'dnipropetrovsk': 'Дніпропетровська область',
    'donetsk': 'Донецька область',
    'kharkiv': 'Харківська область',
    'kherson': 'Херсонська область',
    'khmelnitskyi': 'Хмельницька область',
    'kyiv': 'Київська область',
    'kyivcity': 'Київ',
    'kirovohrad': 'Кіровоградська область',
    'lviv': 'Львівська область',
    'luhansk': 'Луганська область',
    'mykolaiv': 'Миколаївська область',
    'odesa': 'Одеська область',
    'poltava': 'Полтавська область',
    'rivne': 'Рівненська область',
    'sevastopolcity': 'Севастополь',
    'sumy': 'Сумська область',
    'ivano-frankivsk': 'Івано-Франківська область',
    'ternopil': 'Тернопільська область',
    'zakarpattia': 'Закарпатська область',
    'vinnytsia': 'Вінницька область',
    'volyn': 'Волинська область',
    'zaporizhzhia': 'Запорізька область',
    'zhytomir': 'Житомирська область'
}

REGIONS_ORDLO_ENG = REGIONS_ENG.copy()
REGIONS_ORDLO_ENG.update(
    {
        "ordlo": "Тимчасово окуповані райони Донецької і Луганської областей"
    }
)

REGIONS_ORDLO_UA = REGIONS_UA.copy()
REGIONS_ORDLO_UA.update(
    {
        "ordlo": "Temporarily occupied areas of Donetsk and Luhansk Oblasts"
    }
)

with open(
    os.path.join(os.path.dirname(__file__), 'UKR-ADM1_simplified.Svg')
) as file:
    REG_MAP = file.read()

with open(
    os.path.join(os.path.dirname(__file__), 'UKR-ADM1_simplified_ordlo.Svg')
) as file:
    REG_ORDLO_MAP = file.read()


class RegionsEng(BaseMap):
    x_labels = list(REGIONS_ENG.keys())
    area_names = REGIONS_ENG
    area_prefix = 'ua_'
    svg_map = REG_MAP
    kind = 'region'


class Regions(BaseMap):
    x_labels = list(REGIONS_ENG.keys())
    area_names = REGIONS_UA
    area_prefix = 'ua_'
    svg_map = REG_MAP
    kind = 'region'


class RegionsOrdlo(BaseMap):
    x_labels = list(REGIONS_ENG.keys())
    area_names = REGIONS_ORDLO_UA
    area_prefix = 'ua_'
    svg_map = REG_ORDLO_MAP
    kind = 'region'


class RegionsEngOrdlo(BaseMap):
    x_labels = list(REGIONS_ENG.keys())
    area_names = REGIONS_ORDLO_ENG
    area_prefix = 'ua_'
    svg_map = REG_ORDLO_MAP
    kind = 'region'


def set_regions(countries):
    REGIONS_UA.update(countries)
    REGIONS_ORDLO_UA.update(countries)


def set_regions_eng(countries):
    REGIONS_ENG.update(countries)
    REGIONS_ENG.update(countries)
