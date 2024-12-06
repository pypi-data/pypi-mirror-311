#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module generates standard files & documentation.
"""
import io
import json
import re
import tempfile
import zipfile
from itertools import chain
from pathlib import Path
from types import SimpleNamespace

import frictionless as fl
import pandas as pd
import requests
from met_brewer import met_brew

from . import VERSION
from .markdown import to_markdown
from .meta import package_from_kwargs, gen_metadata
from .paths import docs_path, standard_path
from .validate import paralex_validation

unknown = "*unknown*"


def _make_standard_package(*args, **kwargs):
    with (standard_path / "package_spec.json").open('r', encoding="utf-8") as flow:
        package_infos = json.load(flow)
        package_infos["version"] = VERSION

    with (standard_path / "columns_spec.json").open('r', encoding="utf-8") as flow:
        columns = json.load(flow)

    with (standard_path / "files_spec.json").open('r', encoding="utf-8") as flow:
        resources = json.load(flow)["resources"]

    new_resources = []
    for res in resources:
        # replace column names by their full definition
        if res["path"].endswith(".csv"):
            res["schema"]["fields"] = [dict(columns[f]) for f in res["schema"]["fields"]]

        if res["name"] == "forms":
            for col in res["schema"]["fields"]:
                if col["name"] in ["lexeme", "cell"]:
                    col["constraints"] = {"required": True}

        new_resources.append(fl.Resource(res))

    package = package_from_kwargs(resources=new_resources, **package_infos)

    package.to_json(str(standard_path / "paralex.package.json"))


def _get_glottocode():
    glottolog_langs = "https://raw.githubusercontent.com/glottolog/glottolog-cldf/refs/tags/v5.1/cldf/languages.csv"
    glottocode = pd.read_csv(io.BytesIO(requests.get(glottolog_langs).content))
    return glottocode


def _get_previous_data():
    ######### HACK TO GET LOCAL FILE
    # url = "http://localhost:8000/paralex/known-datasets.csv"
    url = "https://paralex-standard.org/known-datasets.csv"
    try:
        df = pd.read_csv(url, index_col=1)
        return df
    except:
        return None


def _save_record_files(record, directory):
    expected_files = {".csv", ".json", ".md"}
    files = []
    for file in requests.get(record["links"]["files"]).json()["entries"]:
        file_name = file["key"]
        file_link = file["links"]["content"]
        if file_name.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(requests.get(file_link).content)) as zfile:
                zfile.extractall(directory)
                files.extend([f.filename for f in zfile.infolist()])
        elif any(file_name.endswith(e) for e in expected_files):
            with (directory / file_name).open("wb") as f:
                f.write(requests.get(file_link).content)
                files.append(file_name)
    return files


def _gather_dataset_info(glottolog_data):
    old = _get_previous_data()
    response = requests.get('https://zenodo.org/api/records',
                            params={'communities': 'paralex'})
    data = []
    fields = ['name', 'lang', 'paralex_version', 'contributors', 'title', 'doi', 'comment']
    for record in response.json()["hits"]["hits"]:
        doi = record["links"]["doi"]
        if old is None or not (doi in old.doi.values):
            package_infos = _get_package_infos(record)

            ######### TEMPORARY HACK TO FAKE UPDATED DATASETS
            tmp_replacer = {"PrinParLat": ["lat"], "LatInfLexi": ["lat"], "LeFFI": ["ita"]}
            package_infos["lang"] = tmp_replacer.get(package_infos["name"], package_infos["lang"])
            ######### END TEMPORARY HACK TO FAKE UPDATED DATASETS

            data.append(package_infos)
        else:
            package_infos = old[old.doi == doi].reset_index().iloc[0].to_dict()
            package_infos = {key: value for key, value in package_infos.items() if key in fields}
            package_infos['lang'] = [package_infos['lang']]
            data.append(package_infos)

    data = pd.DataFrame(data).explode("lang").fillna(unknown)

    isonames = glottolog_data.set_index("ISO639P3code").Name.to_dict()
    res = data.join(glottolog_data.set_index("ISO639P3code").loc[:, ["Latitude", "Longitude", "Family_ID"]], "lang",
                    how="left")
    res['lang_name'] = res.lang.map(isonames)
    lang_labels = dict(glottolog_data.loc[:, ["ID", "Name"]].to_records(index=False))
    res["Family"] = res["Family_ID"].map(lang_labels)
    res.to_csv(docs_path / "known-datasets.csv")


def _get_package_file(record):
    def load_json(filepath):
        try:
            with filepath.open(encoding="utf-8") as fp:
                return json.load(fp)
        except Exception as e:
            print(f"{e} occured at {doi}, {title}")
        return {}

    def is_package_file(json):
        return json.get("profile", None) == "data-package"

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)
        _save_record_files(record, tempdir)  # Save all files to temp dir, unpacking zips

        # Search for json files
        files = list(tempdir.glob("*package.json"))
        if len(files) == 0:
            files = list(tempdir.glob("**/*.json"))

        # Find the package
        for file in files:
            md = load_json(file)
            if is_package_file(md):
                return md
    return None


def _get_package_infos(record):
    doi = record["links"]["doi"]
    title = record["title"]
    json_data = _get_package_file(record)
    if json_data is not None:
        return {"title": title,
                "doi": doi,
                "name": json_data.get("name", json_data.get("title", unknown)),
                "lang": json_data.get("languages_iso639", unknown),
                "paralex_version": json_data.get("paralex-version", unknown),
                "contributors": ";".join(c["title"] for c in json_data["contributors"]),
                }

    return {"title": title,
            "doi": doi,
            "comment": "no valid metadata found"
            }


def _build_stats(df, glottocode_data):
    include_path = docs_path / "includes"
    include_path.mkdir(parents=True, exist_ok=True)

    stats = {"summary_pie.md": _summary_family_pie,
             "summary_wanted_fam.md": _summary_wanted_fam,
             "summary_wanted_50.md": _summary_wanted_50,
             "summary_contributors.md": _summary_contributors,
             }

    for name, func in stats.items():
        md = func(df, glottocode_data)
        with (include_path / name).open("w") as f:
            f.write(md)


def _summary_contributors(df, *args, **kwargs):
    def sorter(word):
        word = word.strip()
        m = re.match(r"^.+? [A-Z][^.]", word)
        if not m:
            return word
        return word[m.span()[1] - 2:]

    authors = set(chain(*(c.split(";") for c in df["contributors"])))
    authors - {unknown}
    return "**Dataset contributors: **" + ", ".join(sorted(authors, key=sorter))


def _summary_wanted_50(df, glottolog_data):
    stats = pd.read_csv(docs_path / "language_stats.csv")
    stats_gl = glottolog_data[glottolog_data.Name.isin(stats.Language)].set_index('Name')[
        'Closest_ISO369P3code'].to_dict()
    stats['ISO 693'] = stats.Language.map(stats_gl)
    missing = stats[~stats['ISO 693'].isin(df.lang)].iloc[0:5]
    return missing.set_index("ISO 693").to_markdown()


def _summary_wanted_fam(df, glottolog_data):
    covered = df.Family_ID.unique()
    lang_labels = dict(glottolog_data.loc[:, ["ID", "Name"]].to_records(index=False))
    fams = glottolog_data.groupby('Family_ID').size().sort_values(ascending=False)
    fams = fams[~fams.index.isin(covered)].iloc[0:5]
    fams.index = fams.index.map(lang_labels)
    fams.index.name = "Language family"
    fams.name = "Number of languages in Glottolog"
    md = fams.to_markdown()
    return md


def _summary_family_pie(df, glottocode_data):
    """Family distribution pie"""
    fams = df.groupby(['color', 'Family']).apply(len)
    fams.name = "nb"
    fams = fams.to_frame().reset_index()
    idx = fams.Family.to_list()
    values = fams.nb.to_list()
    color = fams.color.to_list()
    mermaid = """
<div style="height: 300px;">
  <canvas id="myChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: """ + str(idx) + """,
      datasets: [{
        backgroundColor: """ + str(color) + """,
        label: 'Number of datasets',
        data: """ + str(values) + """,
      }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
  });
</script>

"""
    # for key, value in family_pct.items():
    #     mermaid += f'\n    "{key}": {value}'
    return mermaid


def _build_json(df):
    geojson = {"type": "FeatureCollection", "features": []}

    for _, row in df.dropna(subset=['Longitude', 'Latitude']).iterrows():
        feature = {"type": "Feature",
                   "geometry": {"type": "Point",
                                "coordinates": [row['Longitude'], row['Latitude']]
                                }
                   }

        feature['properties'] = {key: row[key] for key in row.index.values[1:]
                                 if key not in ['Longitude', 'Latitude']}
        geojson['features'].append(feature)

    with (docs_path / 'result.geojson').open('w') as fp:
        json.dump(geojson, fp)


def _build_summaries(glottocode_data):
    """Builds all the summaries from the dataframe of datasets."""
    df = pd.read_csv(docs_path / 'known-datasets.csv')
    # Assign a color to each family
    nitems = df['Family_ID'].nunique()
    col = met_brew(name="Isfahan2", n=nitems)
    df['color'] = df.groupby(by='Family_ID').ngroup().apply(lambda x: col[int(x)] if not pd.isna(x) else None)

    _build_json(df)
    _build_stats(df, glottocode_data)


def _write_doc(*args, **kwargs):
    to_markdown(fl.Package(standard_path / "paralex.package.json"),
                docs_path / "specs.md")

    # generate json files for examples
    examples_dir = docs_path / "examples"
    for directory in examples_dir.glob("*/"):
        gen_metadata(SimpleNamespace(config=directory / "paralex-infos.yml", basepath=directory))
    glottocode_data = _get_glottocode()
    _gather_dataset_info(glottocode_data)
    _build_summaries(glottocode_data)
