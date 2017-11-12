from __future__ import print_function
import os
import sys
import re
import logging
import unicodedata
from codecs import open
from random import shuffle, randint, choice

replacement_pattern = re.compile(ur'\$\{(?P<token>[^}]+)\}')

# iOS 11 + Android 26
mobile_safe_pattern = re.compile(ur'[\u0000-\u0377\u037a-\u037f\u0384-\u038a\u038c\u038e-\u03a1\u03a3-\u052f\u0531-\u0556\u0559-\u055f\u0561-\u0587\u0589-\u058a\u058f\u0591-\u05c7\u05d0-\u05ea\u05f0-\u05f4\u0600-\u0604\u0606-\u061c\u061e-\u070d\u070f-\u074a\u074d-\u07b1\u07c0-\u07fa\u0800-\u082d\u0830-\u083e\u0840-\u085b\u085e\u08a0\u08a2-\u08ac\u08e4-\u08f9\u08fb-\u08fe\u0900-\u097f\u0981-\u0983\u0985-\u098c\u098f-\u0990\u0993-\u09a8\u09aa-\u09b0\u09b2\u09b6-\u09b9\u09bc-\u09c4\u09c7-\u09c8\u09cb-\u09ce\u09d7\u09dc-\u09dd\u09df-\u09e3\u09e6-\u09fb\u0a01-\u0a03\u0a05-\u0a0a\u0a0f-\u0a10\u0a13-\u0a28\u0a2a-\u0a30\u0a32-\u0a33\u0a35-\u0a36\u0a38-\u0a39\u0a3c\u0a3e-\u0a42\u0a47-\u0a48\u0a4b-\u0a4d\u0a51\u0a59-\u0a5c\u0a5e\u0a66-\u0a75\u0a81-\u0a83\u0a85-\u0a8d\u0a8f-\u0a91\u0a93-\u0aa8\u0aaa-\u0ab0\u0ab2-\u0ab3\u0ab5-\u0ab9\u0abc-\u0ac5\u0ac7-\u0ac9\u0acb-\u0acd\u0ad0\u0ae0-\u0ae3\u0ae6-\u0af1\u0b01-\u0b03\u0b05-\u0b0c\u0b0f-\u0b10\u0b13-\u0b28\u0b2a-\u0b30\u0b32-\u0b33\u0b35-\u0b39\u0b3c-\u0b44\u0b47-\u0b48\u0b4b-\u0b4d\u0b56-\u0b57\u0b5c-\u0b5d\u0b5f-\u0b63\u0b66-\u0b77\u0b82-\u0b83\u0b85-\u0b8a\u0b8e-\u0b90\u0b92-\u0b95\u0b99-\u0b9a\u0b9c\u0b9e-\u0b9f\u0ba3-\u0ba4\u0ba8-\u0baa\u0bae-\u0bb9\u0bbe-\u0bc2\u0bc6-\u0bc8\u0bca-\u0bcd\u0bd0\u0bd7\u0be6-\u0bfa\u0c01-\u0c03\u0c05-\u0c0c\u0c0e-\u0c10\u0c12-\u0c28\u0c2a-\u0c33\u0c35-\u0c39\u0c3d-\u0c44\u0c46-\u0c48\u0c4a-\u0c4d\u0c55-\u0c56\u0c58-\u0c59\u0c60-\u0c63\u0c66-\u0c6f\u0c78-\u0c7f\u0c82-\u0c83\u0c85-\u0c8c\u0c8e-\u0c90\u0c92-\u0ca8\u0caa-\u0cb3\u0cb5-\u0cb9\u0cbc-\u0cc4\u0cc6-\u0cc8\u0cca-\u0ccd\u0cd5-\u0cd6\u0cde\u0ce0-\u0ce3\u0ce6-\u0cef\u0cf1-\u0cf2\u0d02-\u0d03\u0d05-\u0d0c\u0d0e-\u0d10\u0d12-\u0d3a\u0d3d-\u0d44\u0d46-\u0d48\u0d4a-\u0d4e\u0d57\u0d60-\u0d63\u0d66-\u0d75\u0d79-\u0d7f\u0d82-\u0d83\u0d85-\u0d96\u0d9a-\u0db1\u0db3-\u0dbb\u0dbd\u0dc0-\u0dc6\u0dca\u0dcf-\u0dd4\u0dd6\u0dd8-\u0ddf\u0df2-\u0df4\u0e01-\u0e3a\u0e3f-\u0e5b\u0e81-\u0e82\u0e84\u0e87-\u0e88\u0e8a\u0e8d\u0e94-\u0e97\u0e99-\u0e9f\u0ea1-\u0ea3\u0ea5\u0ea7\u0eaa-\u0eab\u0ead-\u0eb9\u0ebb-\u0ebd\u0ec0-\u0ec4\u0ec6\u0ec8-\u0ecd\u0ed0-\u0ed9\u0edc-\u0edd\u0f00-\u0f47\u0f49-\u0f6c\u0f71-\u0f8b\u0f90-\u0f97\u0f99-\u0fbc\u0fbe-\u0fcc\u0fce-\u0fd8\u1000-\u1021\u1023-\u1027\u1029-\u1032\u1036-\u1059\u10a0-\u10c5\u10d0-\u10fc\u1100-\u1112\u115f-\u1175\u119e\u11a8-\u11c2\u1200-\u1248\u124a-\u124d\u1250-\u1256\u1258\u125a-\u125d\u1260-\u1288\u128a-\u128d\u1290-\u12b0\u12b2-\u12b5\u12b8-\u12be\u12c0\u12c2-\u12c5\u12c8-\u12d6\u12d8-\u1310\u1312-\u1315\u1318-\u135a\u135f-\u137c\u1380-\u1399\u13a0-\u13f4\u1401-\u1676\u1680-\u169c\u16a0-\u16f0\u1700-\u170c\u170e-\u1714\u1720-\u1736\u1740-\u1753\u1760-\u176c\u176e-\u1770\u1772-\u1773\u1780-\u17dd\u17e0-\u17e9\u17f0-\u17f9\u1800-\u180e\u1810-\u1819\u1820-\u1877\u1880-\u18aa\u1900-\u191c\u1920-\u192b\u1930-\u193b\u1940\u1944-\u196d\u1970-\u1974\u1980-\u19ab\u19b0-\u19c9\u19d0-\u19da\u19de-\u1a1b\u1a1e-\u1a5e\u1a60-\u1a7c\u1a7f-\u1a89\u1a90-\u1a99\u1aa0-\u1aad\u1b00-\u1b4b\u1b50-\u1b7c\u1b80-\u1bf3\u1bfc-\u1c37\u1c3b-\u1c49\u1c4d-\u1c7f\u1cc0-\u1cc7\u1d00-\u1dca\u1dcd\u1dfe-\u1f15\u1f18-\u1f1d\u1f20-\u1f45\u1f48-\u1f4d\u1f50-\u1f57\u1f59\u1f5b\u1f5d\u1f5f-\u1f7d\u1f80-\u1fb4\u1fb6-\u1fc4\u1fc6-\u1fd3\u1fd6-\u1fdb\u1fdd-\u1fef\u1ff2-\u1ff4\u1ff6-\u1ffe\u2000-\u2027\u202a-\u205f\u206a-\u2071\u2074-\u208e\u2090-\u2094\u20a0-\u20bf\u20d0-\u20e1\u20e3-\u20f0\u2100-\u214e\u2150-\u2184\u2189\u2190-\u237a\u237c-\u237d\u2380-\u2383\u2388-\u238b\u2393-\u2395\u239b-\u23b9\u23ce-\u23d0\u23da-\u23e7\u23e9-\u23f3\u23f8-\u23fa\u2400-\u2424\u2440-\u244a\u2460-\u269c\u26a0-\u26b2\u26bd-\u26be\u26c4-\u26c5\u26c8\u26ce-\u26cf\u26d1\u26d3-\u26d4\u26e2\u26e9-\u26ea\u26f0-\u26f5\u26f7-\u26fa\u26fd\u2701-\u275e\u2761-\u27c9\u27cb-\u27cd\u27d0-\u2aff\u2b05-\u2b07\u2b12-\u2b4c\u2b50-\u2b55\u2c00-\u2c2e\u2c30-\u2c5e\u2c60-\u2c70\u2c74-\u2c77\u2c79-\u2c7a\u2c7c-\u2c7d\u2c80-\u2cf3\u2cf9-\u2cff\u2d30-\u2d67\u2d6f-\u2d70\u2d7f-\u2d96\u2da0-\u2da6\u2da8-\u2dae\u2db0-\u2db6\u2db8-\u2dbe\u2dc0-\u2dc6\u2dc8-\u2dce\u2dd0-\u2dd6\u2dd8-\u2dde\u2de0-\u2e18\u2e1c-\u2e1d\u2e2e\u2e30-\u2e31\u3000-\u3003\u3005-\u301f\u3021-\u3029\u3030\u303d\u3041-\u3094\u3099-\u309e\u30a0-\u30f6\u30fb-\u30fe\u3105-\u3129\u3131-\u318e\u3200-\u321c\u3220-\u3229\u3231-\u3232\u3239\u3260-\u327b\u327f\u3297\u3299\u32a3-\u32a8\u3303\u330d\u3314\u3318\u3322-\u3323\u3326-\u3327\u332b\u3336\u333b\u3349-\u334a\u334d\u3351\u3357\u337b-\u337e\u3380-\u3384\u3388-\u33ca\u33cd-\u33d3\u33d5-\u33d6\u33d8\u33db-\u33dd\u3400-\u4db5\u4e00-\u9fa5\ua000-\ua48c\ua490-\ua4c6\ua4d0-\ua62b\ua640-\ua69d\ua69f-\ua6f7\ua700-\ua721\ua727\ua789-\ua78c\ua792\ua7a4\ua800-\ua82b\ua830-\ua839\ua840-\ua877\ua880-\ua8c4\ua8ce-\ua8d9\ua900-\ua953\ua95f\ua980-\ua9cd\ua9cf-\ua9d9\ua9de-\ua9df\uaa00-\uaa36\uaa40-\uaa4d\uaa50-\uaa59\uaa5c-\uaa5f\uaa80-\uaac2\uaadb-\uaaf6\uab01-\uab06\uab09-\uab0e\uab11-\uab16\uab20-\uab26\uab28-\uab2e\uabc0-\uabed\uabf0-\uabf9\uac00-\ud7a3\uf900-\ufa2d\ufb00-\ufb06\ufb1d-\ufb36\ufb38-\ufb3c\ufb3e\ufb40-\ufb41\ufb43-\ufb44\ufb46-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd92-\ufdc7\ufdf0-\ufdfd\ufe00\ufe10-\ufe19\ufe20-\ufe26\ufe30-\ufe31\ufe33-\ufe46\ufe49-\ufe52\ufe54-\ufe57\ufe59-\ufe66\ufe68-\ufe6b\ufe70-\ufe74\ufe76-\ufefc\ufeff\uff01-\uff5e\uff61-\uff9f\uffe0-\uffe6\ufffc-\ufffd\U00010000-\U0001000b\U0001000d-\U00010026\U00010028-\U0001003a\U0001003c-\U0001003d\U0001003f-\U0001004d\U00010050-\U0001005d\U00010080-\U000100fa\U00010100-\U00010102\U00010107-\U00010133\U00010137-\U0001013f\U00010280-\U0001029c\U000102a0-\U000102d0\U00010300-\U0001031e\U00010320-\U00010323\U00010330-\U0001034a\U00010380-\U0001039d\U0001039f-\U000103c3\U000103c8-\U000103d5\U00010400-\U0001049d\U000104a0-\U000104a9\U00010800-\U00010805\U00010808\U0001080a-\U00010835\U00010837-\U00010838\U0001083c\U0001083f-\U00010855\U00010857-\U0001085f\U00010900-\U0001091b\U0001091f-\U00010939\U0001093f\U00010a00-\U00010a03\U00010a05-\U00010a06\U00010a0c-\U00010a13\U00010a15-\U00010a17\U00010a19-\U00010a33\U00010a38-\U00010a3a\U00010a3f-\U00010a47\U00010a50-\U00010a58\U00010a60-\U00010a7f\U00010b00-\U00010b35\U00010b39-\U00010b55\U00010b58-\U00010b72\U00010b78-\U00010b7f\U00010c00-\U00010c48\U00011000-\U0001104d\U00011052-\U0001106f\U00011080-\U000110c1\U00012000-\U0001236e\U00012400-\U00012462\U00012470-\U00012473\U00013000-\U0001342e\U00016800-\U00016a38\U0001d173-\U0001d17a\U0001d400-\U0001d454\U0001d456-\U0001d49c\U0001d49e-\U0001d49f\U0001d4a2\U0001d4a5-\U0001d4a6\U0001d4a9-\U0001d4ac\U0001d4ae-\U0001d4b9\U0001d4bb\U0001d4bd-\U0001d4c3\U0001d4c5-\U0001d505\U0001d507-\U0001d50a\U0001d50d-\U0001d514\U0001d516-\U0001d51c\U0001d51e-\U0001d539\U0001d53b-\U0001d53e\U0001d540-\U0001d544\U0001d546\U0001d54a-\U0001d550\U0001d552-\U0001d6a5\U0001d6a8-\U0001d7c9\U0001d7ce-\U0001d7ff\U0001f004\U0001f0cf\U0001f170-\U0001f171\U0001f17e-\U0001f17f\U0001f18e\U0001f191-\U0001f19a\U0001f1e6-\U0001f1ff\U0001f201-\U0001f202\U0001f21a\U0001f22f\U0001f232-\U0001f23a\U0001f250-\U0001f251\U0001f300-\U0001f321\U0001f324-\U0001f393\U0001f396-\U0001f397\U0001f399-\U0001f39b\U0001f39e-\U0001f3f0\U0001f3f3-\U0001f3f5\U0001f3f7-\U0001f4fd\U0001f4ff-\U0001f53d\U0001f549-\U0001f54e\U0001f550-\U0001f567\U0001f56f-\U0001f570\U0001f573-\U0001f57a\U0001f587\U0001f58a-\U0001f58d\U0001f590\U0001f595-\U0001f596\U0001f5a4-\U0001f5a5\U0001f5a8\U0001f5b1-\U0001f5b2\U0001f5bc\U0001f5c2-\U0001f5c4\U0001f5d1-\U0001f5d3\U0001f5dc-\U0001f5de\U0001f5e1\U0001f5e3\U0001f5e8\U0001f5ef\U0001f5f3\U0001f5fa-\U0001f64f\U0001f680-\U0001f6c5\U0001f6cb-\U0001f6d2\U0001f6e0-\U0001f6e5\U0001f6e9\U0001f6eb-\U0001f6ec\U0001f6f0\U0001f6f3-\U0001f6f6\U0001f910-\U0001f91e\U0001f920-\U0001f927\U0001f930\U0001f933-\U0001f93a\U0001f93c-\U0001f93e\U0001f940-\U0001f945\U0001f947-\U0001f94b\U0001f950-\U0001f95e\U0001f980-\U0001f991\U0001f9c0\U000e0030-\U000e0039\U000e0061-\U000e007a\U000e007f]')

unicode_min, unicode_max = 0, 0x10ffff
unicode_cat_blacklist = ['Mn', 'Mc', 'Me', 'Cc', 'Cf', 'Cs', 'Co', 'Cn']

profile = {}

with open('profile.properties', encoding='utf-8') as infile:
    for line in infile:
        key, value = line.strip().split('=')
        profile[key] = value

adjectives = []
people = []


def load_words(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read().splitlines()
    else:
        print(filename + ' not found. Generate it.')
        sys.exit(1)

adjectives = load_words('adjectives.txt')


def _character():
    while True:
        i = randint(unicode_min, unicode_max)
        c = unichr(i)
        if unicodedata.category(c) not in unicode_cat_blacklist \
           and mobile_safe_pattern.match(c):
            return c


def _enclosing_character():
    enclosing = [unichr(i) for i in xrange(unicode_min, unicode_max)
                 if unicodedata.category(unichr(i)) == 'Me']
    return choice(enclosing)


def _indefinite_adjective():
    adj = _adjective()
    article = 'an' if adj.lower()[0] in 'aeiou' else 'a'
    return '%s %s' % (article, adj)


def _adjective():
    return choice(adjectives)


def _fix_capitalization(text, location):
    return text[0].upper() + text[1:] if location == 0 else text


def _dispatch(match):
    res = globals()['_%s' % match.group('token')]()
    return _fix_capitalization(res, match.start())


def randomize(text):
    return replacement_pattern.sub(_dispatch, text) if text else ''


def randomized_profile():
    return {key: randomize(value) for key, value in profile.iteritems()}


def main():
    print('\n'.join(['%s=%s' % (k, v) for k, v in randomized_profile().iteritems()]))


if __name__ == '__main__':
    import sys
    if '-v' in sys.argv:
        logging.getLogger().setLevel(logging.DEBUG)
    main()
