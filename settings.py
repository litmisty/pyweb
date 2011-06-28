# pyweb-ko
# Copyright (C) 2011  mimu
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    ROOT_PATH + '/template',
)

USE_I18N = True
LOCALE_PATHS = (
    ROOT_PATH + '/locale',
)
TIME_ZONE = 'Asia/Tokyo'

LANGUAGE_CODE = 'ko-KR'

# Valid languages
LANGUAGES = (
    ('en', 'English'),
    ('ko', 'Korean'),
)

RECAPTCHA_PUBLICKEY = "6LeY9sMSAAAAAEuvkWkp2BlH_l4xjOAmp7qzfZ5j"
RECAPTCHA_PRIVATEKEY = "6LeY9sMSAAAAAIMyi5mdgGpxORpuT8ewFQxXClb2"
