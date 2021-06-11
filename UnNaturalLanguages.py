import wand
import json
import wand.image
import hashlib
from cldfcatalog import Catalog
import pyglottolog
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import collections
from pathlib import Path


# There is actually NO WRITTEN INFO on the size of the speaker population in
# the publically accessible Ethnologue data. The only visible value is in the
# *content* of the graph plotted on the ‘size and vitality’ pages. Luckily,
# there are only 10 different graph images, with the following sha1 hashes.
by_image_hash = {
    b"\xfe-\r\x0e/\xf9u'D\xe1\xf9\xc4M\xec\xd8\xab\xd7\x9a\xb8{": (
        "small",
        "endangered",
    ),
    b"\x11\x00\xab?\xbc'\x83\xec)VJC5\xb0)lj\xd6&Y": ("mid", "stable"),
    b"BBn\xf4U\x87\xf5\xc1V\xf5\xe3\xb8\x8b\x03\xf9\xb3\xa4$\x1c\x13": (
        "small",
        "stable",
    ),
    b"\\\x0b\x9f@\xdc\xf9Pvne\xc5+\x9e\x99\x10\xc5\x19:\xb4\xf7": (
        "extinct",
        "extinct",
    ),
    b"\x0b\xfe\x03\x8e?\xf5\xf5\xde\x8f?7\x08\xafI\x0f\xc9\xd1\x11\xc99": (
        "mid",
        "institutional",
    ),
    b"\xe3\x19\x08\xdf\x9eF\xd9\x81U\xf6\xcaC\x8fsV2\x16\x0c&k": ("mid", "endangered"),
    b"[\x81\xb3\x08\xb4pZ\xc5\xc9\xcf\x98R\xb8XJ\x1e\xcf\xb1z5": ("large", "stable"),
    b".\x18\x80*\x1a\xf8\x98\xc4\xc6O\xf5\x91_\x99\x16A\x0c\x16bt": (
        "large",
        "institutional",
    ),
    b"\x1eT\xaa\xdfX\xcdr\xac\xab\xa1\x1b\xd2Z\x87B\xafy\xd2\x10\x1b": (
        "large",
        "endangered",
    ),
    b"2\x0c\x10 \xab\xfa\x05rX?\xde1\xed\xbes\x10\x11\xfe\x98[": (
        "small",
        "institutional",
    ),
}


try:
    language_sizes = json.load(Path("data/lects.json").open())
    ethnolog_data_loaded = True
except FileNotFoundError:
    language_sizes = collections.defaultdict(list)
    ethnolog_data_loaded = False

with Catalog.from_config("glottolog", tag="v4.3") as glottolog_repo:
    glottolog = pyglottolog.Glottolog(glottolog_repo.dir)

    non_extinct = 0
    for lang in glottolog.languoids():
        if not ethnolog_data_loaded and lang.iso_code:
            try:
                image_url = f"https://www.ethnologue.com/sites/default/files/styles/large/public/graphs/24/lang-open-{lang.iso_code}.png"
                req = Request(url=image_url, headers={"User-Agent": "python3.9"})
                handler = urlopen(req)
                hasher = hashlib.sha1()
                hasher.update(handler.read())
                sha1 = hasher.digest()
                size, endangerment = by_image_hash[sha1]
                language_sizes[size].append(lang)
            except HTTPError:
                pass
        if lang.level.id == "language":
            if lang.endangerment and lang.endangerment.status.id != "extinct":
                print(lang, lang.endangerment.status.id)
                non_extinct += 1
        if len(language_sizes) > 20:
            break

if not ethnolog_data_loaded:
    json.dump(language_sizes, Path("data/lects.json").open("w"))
    ethnolog_data_loaded = True

print(non_extinct)
