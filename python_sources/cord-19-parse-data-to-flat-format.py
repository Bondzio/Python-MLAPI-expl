#!/usr/bin/env python
# coding: utf-8

# # CORD-19: Parse Data to Flat Format
# ## Data Structure
# Parsed data is a `pd.DataFrame` with the ff. format:  
#   
# | column | type | description |
# |---------------|------|---------------------------------------------------|
# | paper_id | str |  |
# | supsec_order | int | supersection order (as it appears in the paper) |
# | supersection | str | values = {"title", "abstract", "body_text", "back_matter"} |
# | section_order | int | section order (as it appears in the paper) |
# | section | str | based on provided "section" value |
# | text | str | parsed text of the section |  
# <br>  
# 
# **Notes**
# * Supersection and Section are captured 
#     * *I think text in certain sections may need to be given more weight for a better model?*
# * Supersection and Section order are also captured
#     * count starts from 0 (excluding title)
#     * Proxy for "section" when unavailable?
# * The following information are ignored: Author, Citations, References
#     * *I don't think this will be needed for the tasks, but I might be wrong...*
#     * Please see [this helpful notebook](https://www.kaggle.com/xhlulu/cord-19-eda-parse-json-and-generate-clean-csv) for parsing these attributes 
# * Title is encoded as a row
#     * supersection and section = `"title"`, with \*\_order = `None`
# 

# ***Optional***: Use `ujson` instead of stdlib `json`

# In[ ]:


get_ipython().system('pip install ujson')


# ## Imports and Functions
#   
# Helper functions to parse data. Please use `help` for more info.
# * `parse_paper_json` : parses JSON data into a `pd.DataFrame`
# * `parse_section` : parses individual sections found in "abstract", "body_text", and "back_matter"
# * `remove_span_text`: remove spans based on "\*_span" keys in each section
# 

# In[ ]:


import logging
import gc
import glob
import multiprocessing as mp
import os
from typing import Tuple

import numpy as np
import pandas as pd
from tqdm.notebook import tqdm

try:
    import ujson as json
except ImportError:
    import json


def remove_span_text(text: str, spans: list, validate: bool = False) -> str:
    """Remove 'cite/ref/eqn/..._span' from 'text'
    
    Parameters
    ----------
    text : str
    spans: list of dict
        list of `span` JSONs
    validate: bool, optional
        Check if span extracted are the same as specified; defaults to `False`
    
    Returns
    -------
    str
        text without spans
    """
    if spans:
        # TODO: vectorize...?
        chars = np.array(list(text))
        span_df = pd.DataFrame(spans)
        if validate:
            assert (
                span_df["text"]
                == span_df.apply(
                    lambda row: "".join(chars[row["start"] : row["end"]]), axis=1
                )
            ).all(), "Extracted text from `spans` is not the same!"

        mask = np.full_like(chars, True, dtype=bool)
        for _, row in span_df.iterrows():
            mask[row["start"] : row["end"]] = False

        return "".join(chars[mask])
    else:
        return text
    

def parse_section(
    section: str, text: str, remove_spans: bool = True, **kwargs
) -> Tuple[str, str]:
    """
    Parse 'abstract' and 'body_text' sections 
    
    Parameters
    ----------
    **section data
    remove_spans: bool, optional
        Remove cite/ref/eqn/... span strings; defaults to `True`

    Returns
    -------
    tuple[str, str]
        (section, cleaned text)
    """
    spans = []
    for key, val in kwargs.items():
        if key.endswith("_spans"):
            spans.extend(val)
        else:
            logging.warning("unexpected field: `%s`", key)

    clean_str = remove_span_text(text, spans) if remove_spans else text
    return (section, clean_str)


def parse_paper_json(json_data, sup_secs: list = None) -> pd.DataFrame:
    """Parse Paper in JSON format
    
    Parameters
    ----------
    json_data:
        if not a `dict` will set as `json.load(open(json_data))`
    sup_secs: list[str], optional
        supersections to parse; defaults to `["abstract", "body_text", "back_matter"]`

    Returns
    -------
    pd.DataFrame
    """
    if not isinstance(json_data, dict):
        json_data = json.load(open(json_data))
    
    sup_secs = ["abstract", "body_text", "back_matter"]
    title_info = {
        "supsec_order": np.nan,
        "supersection": "title",
        "section_order": np.nan,
        "section": "title",
        "text": json_data["metadata"]["title"],
    }
    dfs = [pd.DataFrame([title_info])]
    for ss_idx, sup_sec in enumerate(sup_secs):
        df = pd.DataFrame(
            [parse_section(**section) for section in json_data[sup_sec]],
            columns=["section", "text"],
        )
        df.insert(0, "section_order", df.index)
        df.insert(0, "supersection", sup_sec)
        df.insert(0, "supsec_order", ss_idx)
        dfs.append(df)

    res_df = pd.concat(dfs, axis=0).reset_index(drop=True)
    res_df.insert(0, "paper_id", json_data["paper_id"])

    return res_df


# ## Parameters

# In[ ]:


# source directory; most likely = "/kaggle/input"
SOURCE_DIR = "/kaggle/input"

# source name : source path mapping
SOURCES = {
    "biorxiv": "./CORD-19-research-challenge/biorxiv_medrxiv/biorxiv_medrxiv",
    "comm_use": "./CORD-19-research-challenge/comm_use_subset/comm_use_subset",
    "noncomm_use": "./CORD-19-research-challenge/noncomm_use_subset/noncomm_use_subset",
    "custom_license": "./CORD-19-research-challenge/custom_license/custom_license",
}


# ## Processing

# In[ ]:


# Process JSON data and Export as csv
for source, path in tqdm(SOURCES.items(), desc="sources"):
    with mp.Pool() as pool:
        files = list(glob.glob(os.path.join(SOURCE_DIR, path, "*.json")))
        src_dfs = list(
            tqdm(
                pool.imap(parse_paper_json, files),
                total=len(files),
                desc="{} files".format(source),
            )
        )

    src_df = pd.concat(src_dfs).reset_index(drop=True)
    src_df["source"] = source
    
    src_df.to_csv("{}-parsed.csv.gz".format(source), index=False, compression='gzip')

