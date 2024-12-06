#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides functions to convert Paralex data to HTML tables.
"""

# Utils
import gzip
import minify_html
from pathlib import Path

# Mkdocs
from jinja2 import Environment, PackageLoader

# Our modules
from .utils import slug, read_pandas


env = Environment(loader=PackageLoader("mkdocs_paralex_plugin"))


def paradigm_to_html(paradigm, out_dir, sorter, lexemes, pbar):
    """
    Renders a long table paradigm as a pretty HTML table.

    Arguments:
        paradigm (pandas.DataFrame): long table representation of the paradigm to render.
        out_dir (str): Directory where generated files will be stored.
        sorter (dict[Str, Int]): information to sort the paradigm rows/columns.
        lexemes (pandas.DataFrale): table of lexemes
        pbar: tqdm progress bar.

    Returns:
        filename(str): name of the file where the HTML paradigm was saved.
    """

    table_dict = paradigm_to_json(paradigm, sorter)
    lexeme = paradigm.name
    # Load jinja template
    template = env.get_template("paradigm.md")

    table = template.render(tables=table_dict,
                            lexeme=lexeme,
                            lexeme_info=lexemes.loc[lexeme, :].to_dict()
                            )
    table = minify_html.minify(table)

    filename = f"details/{slug(lexeme)}.txt"
    table_out = Path(out_dir) / filename
    with table_out.open("w", encoding="utf-8") as f:
        f.write(table)
    pbar.update(1)
    return filename


def paradigm_to_json(paradigm, sorter):
    """Go from long form to a json dict

    tables: [ # list of tables (dict)
                { # A table
                    headers: [] # list of headers (str)
                    indexes:  [] # list of indexes (str)
                    rows: [ # list of content rows
                            [ # one row is a list
                                { # One original form entry, multiple can be at the same coordinates
                                    phon_form: xyz # col/vals from original df
                                }
                        ]
                    ]
                },

                {} # another table...
            ]

    Arguments:
        paradigm (pandas.DataFrame): long table representation of the paradigm to render.
        sorter (dict[Str, Int]): information to sort the paradigm rows/columns.

    Returns:
        list: JSON representation of the paradigm.
    """

    def one_paradigm_to_json(table):
        table_data = {"headers": table.cols.unique().tolist(),
                      "indexes": [],
                      "rows": [],
                      "name": table.name
                      }
        col_to_i = {c: i for i, c in enumerate(table_data["headers"])}
        row_list = []
        for idx, data in table.groupby("rows"):  # groupby doesn't respect row order !
            idx_hr = []
            if idx:
                idx_hr.append(idx)
            r = [None for _ in col_to_i]
            for col, entries in data.groupby("cols"):
                r[col_to_i[col]] = entries.to_dict('records')
            row_list.append((idx, ".".join(idx_hr), r))

        # Sort the row order
        row_list = sorted(row_list, key=lambda x: sorter[x[0]])
        table_data["indexes"] = [x[1] for x in row_list]
        table_data["rows"] = [x[2] for x in row_list]
        return table_data

    ts = paradigm.sort_values(by=["tables", "rows", "cols"],
                              key=lambda x: x.map(sorter)) \
        .fillna("") \
        .groupby("tables").apply(one_paradigm_to_json, include_groups=False).to_list()
    ts = sorted(ts, key=lambda t: sorter[t["name"]])
    return ts


def table_to_json(name, package, sample, infos=None, with_paradigms=False):
    """
    Converts a Paralex table to JSON format.

    Arguments:
        name (str): name of the table
        package (frictionless.Package): Paralex package data
        sample (set): set of lexemes for which a paradigm should be rendered.
        infos: ?
        with_paradigms (bool): whether paradigms should be rendered or not

    Returns:
        table_dict (dict): JSON representation of the current Paralex table.
    """

    def _get_id(name):
        return "id_" + slug(name)

    # If paradigm tables, add links to tables from lexeme...
    schema = package.get_resource(name).schema

    df = read_pandas(name, package)
    table_dict = {}
    fields = {f.name: f.to_dict() for f in schema.fields}
    pkey = set(getattr(schema, 'primary_key', {})).pop()

    # Add styling classes
    for f in fields:
        field_name = fields[f]['name']
        fields[f]['classes'] = [slug(field_name)]
        if field_name == pkey:
            fields[f]['classes'].append("table_id")

    # Prepare foreign key URL
    rels = {}

    for relation in getattr(schema, "foreign_keys", []):
        fs = relation["fields"][0]
        table = relation["reference"]["resource"]
        id_col = relation["reference"]["fields"][0]
        if id_col.endswith("_id"):
            rels[fs] = f"{table}.html#" + "{}"

    table_dict["columns"] = [fields.get(col, {"name": col}) for col in df.columns]
    table_dict["columns"] = [c if isinstance(c, dict) else c.to_dict() for c in table_dict["columns"]]

    # Prepare rows
    table_dict["rows"] = []
    for id, row in df.iterrows():
        row_data = {col: cell for col, cell in zip(df.columns, row)}
        table_dict["rows"].append(row_data)
        if pkey:
            row_data["DT_RowId"] = _get_id(row_data[pkey])
        for col, url in rels.items():
            row_data[col] = f"<a href={url.format(_get_id(row_data[col]))}>{row_data[col]}</a>"

    table_dict["infos"] = infos

    if name == "lexemes":
        for row in table_dict["rows"]:
            if sample and row['lexeme_id'] in sample:
                row["details"] = "details/" + slug(row["lexeme_id"]) + ".txt"
                row['style'] = "hasParadigm"
    return table_dict


def write_json_table(path, content, compressed=False):
    """
    Write an JSON table and compress it if necessary.

    Arguments:
        path (str): where the file should be stored
        content: the content to write
        compressed (bool): whether an efficient compress strategy should be applied
            to reduce the assets size. It may not render correctly on older browsers.
    """
    # Touch (tricks gitlab into serving gziped file)
    files = []
    files.append(path.name)
    if compressed:
        with path.open("w", encoding="utf-8") as f:
            pass

        # Write gziped file
        gziped = path.with_suffix(path.suffix + ".gz")
        with gzip.open(gziped, mode="wt", encoding="utf-8") as f:
            f.write(content)
        files.append(gziped.name)
    else:
        with path.open("w", encoding="utf-8") as f:
            f.write(content)

    return files
