import io
import csv
import logging
import pycldf
import zipfile
import pyglottolog
import typing as t
import urllib.request
from tqdm import tqdm
from pathlib import Path
from cldfcatalog import Catalog
from collections import Counter, defaultdict
from pyglottolog.fts import build_langs_index, search_langs

Language_ID = str

data = Path("data/wals/")
data.mkdir(exist_ok=True)

print("Downloading WALS…")
if not (data / "wals.zip").exists():
    urllib.request.urlretrieve(
        "https://zenodo.org/record/3731125/files/cldf-datasets/wals-v2020.zip?download=1",
        data / "wals.zip"
    )

with zipfile.ZipFile(data / "wals.zip", "r") as walszip:
    for file in walszip.namelist():
        if "/cldf/" in file:
            target = (data / Path(file).name)
            if target.exists():
                continue
            with target.open("wb") as output:
                output.write(walszip.open(file).read())

print("Loading WALS…")
wals = pycldf.StructureDataset.from_metadata(data / "StructureDataset-metadata.json")

coding: t.Dict[int, str] = {}
for code in wals["CodeTable"]:
    if code["Parameter_ID"] != "81A":
        continue
    coding[code["ID"]] = code["Name"]


print("Accessing Glottolog…")
languoids: t.Dict[Language_ID, t.Optional[pyglottolog.languoids.Languoid]] = {}
# Activate a specific version of Glottolog
with Catalog.from_config("glottolog", tag="v4.3") as glottolog_repo:
    glottolog = pyglottolog.Glottolog(glottolog_repo.dir)
    build_langs_index(glottolog, logging)
    languoids_by_code = glottolog.languoids_by_code()

    print("Getting macroareas from WALS supplemented by Glottolog…")
    for language in tqdm(wals["LanguageTable"], total=wals["LanguageTable"].common_props["dc:extent"]):
        languoids[language["ID"]] = None
        if language["Glottocode"]:
            try:
                languoids[language["ID"]] = languoids_by_code.get(language["Glottocode"])
            except (AttributeError, IndexError):
                pass
        if languoids[language["ID"]] is None:
            n, langs = search_langs(glottolog, language["Name"])
            if n >= 1:
                print(language["ID"], langs[0], end="\n\n")
                languoids[language["ID"]] = languoids_by_code.get(langs[0].id)
                continue
        if languoids[language["ID"]] is None:
            n, langs = search_langs(glottolog, language["Genus"])
            if n == 1:
                print(language["ID"], langs[0], end="\n\n")
                languoids[language["ID"]] = languoids_by_code.get(langs[0].id)
                continue
        if languoids[language["ID"]] is None:
            n, langs = search_langs(glottolog, language["Family"])
            if n == 1:
                print(language["ID"], langs[0], end="\n\n")
                languoids[language["ID"]] = languoids_by_code.get(langs[0].id)
                continue

print("Counting frequencies…")
counts: t.DefaultDict[str, t.Counter[str]] = defaultdict(Counter)
for value in wals["ValueTable"]:
    if value["Parameter_ID"] != "81A":
        continue
    lang = languoids[value["Language_ID"]]
    if lang is not None:
        try:
            family = lang.family.id
        except AttributeError:
            family = lang.id
        counts[family][coding[value["Code_ID"]]] += 1
        if set(m.id for m in lang.macroareas) & {"northamerica", "southamerica"}:
            counts[""][coding[value["Code_ID"]]] += 1

print(counts[''].most_common())
