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
