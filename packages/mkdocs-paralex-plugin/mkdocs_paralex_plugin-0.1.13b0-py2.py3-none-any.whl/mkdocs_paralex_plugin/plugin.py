#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the Mkdocs plugin.
"""

# Utils
from pathlib import Path
from tempfile import TemporaryDirectory
from collections import defaultdict
from tqdm import tqdm
import logging
import json
import minify_html

# Pybtex resources
from pybtex.database import parse_file
from pybtex.backends.markdown import Backend as MarkdownBackend
from pybtex.style.formatting.plain import Style as PlainStyle

# Mkdocs tools
from jinja2 import Environment, PackageLoader
from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File

# Paralex standard
import frictionless
from paralex import to_markdown

# Our modules
from . import utils
from . import convert

env = Environment(loader=PackageLoader("mkdocs_paralex_plugin"))
log = logging.getLogger()


class ParalexConfig(Config):
    paralex_package_path = c.Optional(c.File(exists=True))
    paradigm_pages = c.Type(bool, default=True)
    layout_rows = c.ListOfItems(c.Type(str), default=[])
    layout_columns = c.ListOfItems(c.Type(str), default=[])
    layout_tables = c.ListOfItems(c.Type(str), default=[])
    frequency_sample = c.Type(bool, default=True)
    sample_size = c.Type(int, default=-1)
    compress = c.Type(bool, default=False)


class ParalexSite(BasePlugin[ParalexConfig]):

    def on_config(self, config):
        """
        Note:
            the config argument contains mkdocs global config
            self.config contains the config for this plugin

        """
        self.dir = Path(config.get("config_file_path")).parent
        try:
            self.package_path = self.config.get("paralex_package_path") or next(Path(self.dir).glob("*.package.json"))
        except StopIteration:
            raise ValueError("Can not find your .package.json file."
                             "Please either put it in the same  directory as the config file, "
                             "or specify a path with the config option paralex_package_path.")

        # Get layouts
        self.layout_rows = self.config.get("layout_rows")
        self.layout_columns = self.config.get("layout_columns")
        self.layout_tables = self.config.get("layout_tables")

        # Ensure that layouts do not conflict
        assert (self.layout_rows or not self.layout_columns) and \
               (self.layout_rows or not self.layout_tables)

        # Other paradigm rendering options
        self.frequency_sample = self.config.get("frequency_sample")
        self.sample_size = self.config.get("sample_size")
        self.sampled = False
        self.paradigm_pages = self.config.get("paradigm_pages")
        self.do_compress = self.config.get("compress")

        # Package properties and resources
        self.p = frictionless.Package(self.package_path)
        self.tables = [name for name in self.p.resource_names
                       if self.p.get_resource(name).type == "table"]

        # Files management
        self.doc_dir = Path(config.get("docs_dir"))
        self.site_dir = Path(config.get("site_dir"))
        self.tmp_dir = TemporaryDirectory("data_tmp_")

        # Clean-up
        self.cleaners = []
        self.cleaners.append(self.tmp_dir.cleanup)

        # Add any css / js / etc.
        # Our CSS has lower priority than user files.
        config["extra_css"] = [
            "css/paralex_styles.css",
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
            "https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css",
            ] + config["extra_css"]

        if not config.get("copyright", None):
            footer = ""
            if self.p.has_defined('contributors'):
                footer += "by " + ", ".join([auth['title'] for auth in self.p.contributors]) + "."
            if self.p.has_defined('licences'):
                footer += " licenses: " + ", ".join(
                    [f"<a href='{ls['path']}'>{ls['name']}</a>" for ls in self.p.licences]) + ". "
            config["copyright"] = footer
        config[
            "copyright"] += "This lexicon follows the <a href='https://www.paralex-standard.org/'>paralex</a> standard."

        if "theme" in config and "logo" not in config["theme"]:
            config["theme"]["logo"] = "paralex.png"
            self.add_paralex_logo = True

        if not config.get('nav', None):
            about = ['data_sheet.md', 'metadata.md']
            if self.p.has_resource('sources'):
                about += ["references.md"]
            nav = ['index.md', {'About': about}]
            nav.extend([name + ".md" for name in self.tables])
            config['nav'] = nav

    def on_pre_build(self, *args, config):
        # Symlink readme to index if there is no index in the docs directory
        if self.p.has_resource('readme'):
            readme = self.p.get_resource('readme').path
        else:
            log.warning('Deprecation - Trying to fetch README.md. Please move to Paralex v2.0.8 and set it in the JSON')
            readmes = list((self.dir.glob("[Rr][eE][aA][dD][mM][eE].md")))
            readme = readmes[0] if readmes else None

        index = (self.doc_dir / "index.md")
        if readme is None:
            log.warning("Couldn't find any readme file.")
        elif not index.exists():
            index.symlink_to(Path(readme).resolve(self.p.basepath))
            self.cleaners.append(index.unlink)

        # Symlink data_sheet.md to the docs directory
        if self.p.has_resource('data_sheet'):
            datasheet = self.p.get_resource('data_sheet').path
            docs_datasheet = (self.doc_dir / "data_sheet.md")
            if Path(datasheet).resolve(Path()) != docs_datasheet:
                docs_datasheet.symlink_to(Path(datasheet).resolve(self.p.basepath))
                self.cleaners.append(docs_datasheet.unlink)
        else:
            log.warning('Deprecation - Assuming data_sheet.md is in /docs. Please move to Paralex v2.0.8 and set it in the JSON')

    def on_files(self, files, *, config):
        """
        Generates the pages and the assets,
        store them in a temporary directory and provide the paths.
        """

        here = Path(__file__).parent
        files.append(File("paralex_styles.css", here / "css", self.site_dir / "css/", False))
        tables = {"forms": None,
                  "lexemes": None,
                  "features-values": None}

        def _add_tmp_file(names):
            """
            Utility to register a temporary file

            Arguments:
                names (list or str): name of the paths to save.
            """
            if not isinstance(names, list):
                names = [names]
            for name in names:
                files.append(File(name, self.tmp_dir.name, self.site_dir, False))

        for name in self.tables:
            resource = self.p.get_resource(name)
            if name in tables:
                tables[name] = resource

        if self.paradigm_pages:
            _add_tmp_file(self.generate_paradigms(tables))

        for name in self.tables:
            _add_tmp_file(self.generate_table(name))

        if self.p.has_resource('sources'):
            _add_tmp_file(self.generate_sources())

        if self.add_paralex_logo:
            _add_tmp_file(self.generate_logo())

        _add_tmp_file(self.generate_metadata())

        return files

    def on_post_build(self, *, config):
        for clean_action in self.cleaners:
            clean_action()

    def generate_paradigms(self, tables):
        """
        Generates HTML representations from paradigms.

        Arguments:
            tables (dict): dictionary of Paralex tables.

        Returns:
            List[str]: name of the file
        """

        if tables["features-values"] is None:
            raise ValueError("Can not generate paradigms tables if there is no features table.")

        if tables["lexemes"] is None:
            raise ValueError("Can not generate paradigm tables if there is no lexemes table.")

        (Path(self.tmp_dir.name) / "details").mkdir(exist_ok=True)

        forms_df = utils.read_pandas("forms", self.p)
        features = utils.read_pandas("features-values", self.p, index_col=0)
        lexemes = utils.read_pandas("lexemes", self.p)

        # Restrict to a sample of lexemes
        if self.sample_size > 0:  # Using -1 as a sentinel value, as None isn't a valid default for mkdocs
            if self.frequency_sample and "frequency" in lexemes.columns:
                lexemes = lexemes.sort_values("frequency", ascending=False)[:self.sample_size]
            else:
                lexemes = lexemes.sample(self.sample_size)

        self.sampled = set(lexemes.lexeme_id)
        forms_df = forms_df[forms_df.lexeme.isin(self.sampled)]

        # Separate cells features according to layout
        if not self.layout_rows:
            self.layout_rows = features.index.tolist()

        dim_to_f = defaultdict(list)
        for i, f in features.feature.items():
            dim_to_f[f].append(i)
        feature_grouper = dict(**{v: "tables" for f in self.layout_tables for v in dim_to_f[f]},
                               **{v: "rows" for f in self.layout_rows for v in dim_to_f[f]},
                               **{v: "cols" for f in self.layout_columns for v in dim_to_f[f]},
                                )

        used_dimensions = set(dim_to_f)
        known_dimensions = set(self.layout_rows + self.layout_tables + self.layout_columns)
        undef_dimensions = used_dimensions - known_dimensions
        if undef_dimensions:
            raise ValueError("Undefined features found. "
                             "Edit your config file to add "
                             "these to tables, rows or cols: {}".format(", ".join(undef_dimensions)))

        cells = {cell: utils.parse_cell(cell, feature_grouper) for cell in forms_df.cell.unique()}
        forms_df.loc[:, ["tables", "rows", "cols"]] = forms_df.cell.apply(lambda x: cells[x])

        def cell_order(cell, order):
            return tuple(order.get(f, default=0) for f in cell.split("."))

        if "canonical_order" in features.columns:
            cell_sorter = {elt: cell_order(elt, features.canonical_order)
                           for c in cells for _, elt in cells[c].fillna("").items()}
        else:
            # TODO: default to something sensible here...
            cell_sorter = {elt: 0 for c in cells for _, elt in cells[c].fillna("").items()}

        # Generate HTML paradigms
        files = []
        with tqdm(total=lexemes.shape[0]) as pbar:
            p_files = forms_df.groupby("lexeme") \
                .apply(convert.paradigm_to_html,
                       self.tmp_dir.name,
                       cell_sorter,
                       lexemes.set_index("lexeme_id"),
                       pbar,
                       include_groups=False)
            files.extend(p_files.to_list())
        return files

    def generate_sources(self):
        """
        Generates a markdown representation from a sources.bib file.

        Returns:
            str: name of the file
        """
        path = Path(self.p.basepath) / self.p.get_resource('sources').path
        bibdata = parse_file(path).entries

        # Code adapted from the mkdocs-bibtex plugin
        style = PlainStyle()
        backend = MarkdownBackend()
        citations = {}
        for key, entry in bibdata.items():
            formatted_entry = style.format_entry("", entry)
            entry_text = formatted_entry.text.render(backend)
            entry_text = entry_text.replace("\n", " ")
            citations[key] = entry_text.replace("\\(", "(").replace("\\)", ")").replace("\\.", ".")

        md = "".join([f"\n\n* [**{key}**]  \n{cit}" for key, cit in citations.items()])
        bib_out = Path(self.tmp_dir.name) / "references.md"
        with open(bib_out, 'w') as file:
            file.write(md)
        return "references.md"

    def generate_table(self, name):
        """
        Generates a markdown representation from a Paralex table.

        Arguments:
            name (str): name of the table to handle

        Returns:
            str: name of the file
        """

        template = env.get_template("table.md")

        # Produce JSON representation
        table_data = convert.table_to_json(name, self.p, self.sampled, with_paradigms=self.paradigm_pages)
        json_content = json.dumps({"data": table_data["rows"]},
                                  indent=None,
                                  separators=(',', ':'))
        json_out = Path(self.tmp_dir.name) / (name + ".json")
        new_files = convert.write_json_table(json_out, json_content, compressed=self.do_compress)

        # Produce HTML representation
        table = template.render(columns=table_data["columns"],
                                current_page=name,
                                json_src=json_out.name
                                )
        limit = table.find('<')
        table = table[0:limit] + minify_html.minify(table[limit:])
        table_out = Path(self.tmp_dir.name) / (name + ".md")

        with table_out.open("w", encoding="utf-8") as f:
            f.write(table)

        return [table_out.name] + new_files

    def generate_metadata(self):
        """
        Generates a markdown representation from Paralex metadata.

        Returns:
            str: name of the file
        """
        package_out = Path(self.tmp_dir.name) / "metadata.md"
        to_markdown(self.p, package_out, title="Metadata")
        return 'metadata.md'

    def generate_logo(self):
        """
        Writes the Paralex logo in the right place.

        Returns:
            str: name of the file
        """
        dest = Path(self.tmp_dir.name) / "paralex.png"
        src = Path(__file__).parent / "paralex.png"
        dest.write_bytes(src.read_bytes())
        # breakpoint()
        return dest.name
