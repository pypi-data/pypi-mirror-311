#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides several utility functions.
"""

# Utils
import logging
import re
from itertools import groupby
import pandas as pd
import unidecode

# Paralex
from paralex import read_table

log = logging.getLogger()


def parse_cell(cell, feature_sorter):
    def sort_func(val):
        r = feature_sorter.get(val)
        if r is None:
            log.warning("Err at:", val)
            log.warning("sorter is:", feature_sorter)
            return float("inf")
        return r

    features = sorted(cell.split("."), key=sort_func)
    groups = groupby(features, sort_func)
    return pd.Series({k: ".".join(g) for k, g in groups}, index=["tables", "rows", "cols"])


def slug(string):
    """ Get slug from string """
    slug = unidecode.unidecode(str(string))
    return re.sub(r'[\W]+', '-', slug)


def read_pandas(name, package, **kwargs):
    """ Wrapper to Paralex built-in read_table."""
    data = read_table(name,
                      package,
                      na_values=['', 'NaN'],
                      keep_default_na=False,
                      **kwargs).fillna("")
    return data
