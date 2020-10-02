# In theory, this script would query the PyPI JSON API for Python packages that were
# found in the Kaggle notebook and were not present in Anaconda's package list.
# 
# In the interest of avoiding sending hundreds of web requests to pypi.org, these
# web requests were done in a separate script at a rate of rougly 8 requests per minute.
#
# reference: https://warehouse.readthedocs.io/api-reference/#rate-limiting
#
# Like any good cooking show, we'll take these web results out of the oven already baked.

import numpy as np
import pandas as pd

descriptions = [
    ('Babel', 'Internationalization utilities', 'BSD'),
    ('Baker', 'Easy, powerful access to Python functions from the command line', 'Apache 2.0'),
    ('Boruta', 'Python Implementation of Boruta Feature Selection', 'BSD 3 clause'),
    ('Bottleneck', 'Fast NumPy array functions written in C', 'Simplified BSD'),
    ('CVXcanon', 'A low-level library to perform the matrix building step in cvxpy, a convex optimization modeling software.', 'GPLv3'),
    ('CairoSVG', 'A Simple SVG Converter based on Cairo', 'LGPLv3+'),
    ('Cartopy', 'A cartographic python library with Matplotlib support for visualisation', 'LGPLv3'),
    ('Click', 'Composable command line interface toolkit', 'BSD'),
    ('ConfigArgParse', 'A drop-in replacement for argparse that allows options to also be set via config files and/or environment variables.', 'MIT'),
    ('Cython', 'The Cython compiler for writing C extensions for the Python language.', 'Apache'),
    ('Delorean', 'library for manipulating datetimes with ease and clarity', 'MIT license'),
    ('Deprecated', 'Python @deprecated decorator to deprecate old python classes, functions or methods.', 'MIT'),
    ('Fiona', 'Fiona reads and writes spatial data files', 'BSD'),
    ('Flask', 'A simple framework for building complex web applications.', 'BSD-3-Clause'),
    ('Flask-Cors', 'A Flask extension adding a decorator for CORS support', 'MIT'),
    ('Geohash', 'Module to decode/encode Geohashes to/from latitude and longitude.', 'GNU Affero GPL.'),
    ('ImageHash', 'Image Hashing library', 'BSD 2-clause (see LICENSE file)'),
    ('Janome', 'Japanese morphological analysis engine.', 'AL2'),
    ('Jinja2', 'A small but fast and easy to use stand-alone template engine written in pure python.', 'BSD'),
    ('Keras', 'Deep Learning for humans', 'MIT'),
    ('Keras-Applications', 'Reference implementations of popular deep learning models', 'MIT'),
    ('Keras-Preprocessing', 'Easy data preprocessing and data augmentation for deep learning models', 'MIT'),
    ('Lasagne', 'A lightweight library to build and train neural networks in Theano', 'MIT'),
    ('Mako', 'A super-fast templating language that borrows the  best ideas from the existing templating languages.', 'MIT'),
    ('Markdown', 'Python implementation of Markdown.', 'BSD License'),
    ('MarkupSafe', 'Safely add untrusted strings to HTML/XML markup.', 'BSD-3-Clause'),
    ('PDPbox', 'python partial dependence plot toolbox', 'MIT'),
    ('Pillow', 'Python Imaging Library (Fork)', np.nan),
    ('PyArabic', 'Arabic text tools for Python', 'GPL'),
    ('PyAstronomy', 'A collection of astronomy related tools for Python.', np.nan),
    ('PyBrain', 'PyBrain is the Swiss army knife for neural networking.', 'BSD'),
    ('PyOpenGL', 'Standard OpenGL bindings for Python', 'BSD'),
    ('PyPrind', 'Python Progress Bar and Percent Indicator Utility', 'BSD 3-Clause'),
    ('PySocks', 'A Python SOCKS client module. See https://github.com/Anorov/PySocks for more information.', 'BSD'),
    ('PyUpSet', 'Python implementation of the UpSet visualisation suite by Lex et al.', 'MIT'),
    ('PyWavelets', 'PyWavelets, wavelet transform module', 'MIT'),
    ('PyYAML', 'YAML parser and emitter for Python', 'MIT'),
    ('Pygments', 'Pygments is a syntax highlighting package written in Python.', 'BSD License'),
    ('Pympler', 'A development tool to measure, monitor and analyze the memory behavior of Python objects.', 'Apache License, Version 2.0'),
    ('Pyphen', 'Pure Python module to hyphenate text', np.nan),
    ('QtAwesome', 'FontAwesome icons in PyQt and PySide applications', 'MIT'),
    ('QtPy', 'Provides an abstraction layer on top of the various Qt bindings (PyQt5, PyQt4 and PySide) and additional custom QWidgets.', 'MIT'),
    ('Rtree', 'R-Tree spatial index for Python GIS', 'LGPL'),
    ('SQLAlchemy', 'Database Abstraction Library', 'MIT'),
    ('SecretStorage', 'Python bindings to FreeDesktop.org Secret Service API', 'BSD 3-Clause License'),
    ('Send2Trash', 'Send file to trash natively under Mac OS X, Windows and Linux.', 'BSD License'),
    ('Shapely', 'Geometric objects, predicates, and operations', 'BSD'),
    ('SimpleITK', 'SimpleITK is a simplified interface to the Insight Toolkit (ITK) for image registration and segmentation', 'Apache'),
    ('SoundFile', 'An audio library based on libsndfile, CFFI and NumPy', 'BSD 3-Clause License'),
    ('Sphinx', 'Python documentation generator', 'BSD'),
    ('TPOT', 'Tree-based Pipeline Optimization Tool', 'GNU/LGPLv3'),
    ('Theano', 'Optimizing compiler for evaluating mathematical expressions on CPUs and GPUs.', 'BSD'),
    ('Unidecode', 'ASCII transliterations of Unicode text', 'GPL'),
    ('Wand', 'Ctypes-based simple MagickWand API binding for Python', 'MIT License'),
    ('Werkzeug', 'The comprehensive WSGI web application library.', 'BSD-3-Clause'),
    ('Wordbatch', 'Python library for distributed AI processing pipelines, using swappable scheduler backends', 'GNU GPL 2.0'),
    ('XlsxWriter', 'A Python module for creating Excel XLSX files.', 'BSD'),
    ('absl-py', 'Abseil Python Common Libraries, see https://github.com/abseil/abseil-py.', 'Apache 2.0'),
    ('albumentations', 'Fast image augmentation library and easy to use wrapper around other libraries', 'MIT'),
    ('allennlp', 'An open-source NLP research library, built on PyTorch.', 'Apache'),
    ('altair', 'Altair: A declarative statistical visualization library for Python.', 'BSD 3-clause'),
    ('annoy', 'Approximate Nearest Neighbors in C++/Python optimized for memory usage and loading/saving to disk.', 'Apache License 2.0'),
    ('astor', 'Read/rewrite/write Python ASTs', 'BSD-3-Clause'),
    ('audioread', 'multi-library, cross-platform audio decoding', 'MIT'),
    ('backports.functools-lru-cache', 'backports.functools_lru_cache', np.nan),
    ('backports.shutil-get-terminal-size', "A backport of the get_terminal_size function from Python 3.3's shutil.", 'MIT'),
    ('backports.tempfile', "Backport of new features in Python's tempfile module", 'Python Software Foundation License'),
    ('bayesian-optimization', 'Bayesian Optimization package', np.nan),
    ('bayespy', 'Variational Bayesian inference tools for Python', np.nan),
    ('blis', 'The Blis BLAS-like linear algebra library, as a self-contained C-extension.', 'BSD'),
    ('branca', 'Generate complex HTML+JS pages with Python', 'Copyright (C) 2013, Martin Journois'),
    ('brewer2mpl', 'Connect colorbrewer2.org color maps to Python and matplotlib', 'UNKNOWN'),
    ('cachetools', 'Extensible memoizing collections and decorators', 'MIT'),
    ('cairocffi', 'cffi-based cairo bindings for Python', 'BSD'),
    ('catboost', 'Catboost Python Package', 'Apache License, Version 2.0'),
    ('category-encoders', 'A collection sklearn transformers to encode categorical variables as numeric', 'BSD'),
    ('cesium', 'Machine Learning Time-Series Platform', 'Modified BSD'),
    ('chainercv', np.nan, np.nan),
    ('cleverhans', np.nan, 'MIT'),
    ('cliff', 'Command Line Interface Formulation Framework', np.nan),
    ('cmd2', 'cmd2 - quickly build feature-rich and user-friendly interactive command line applications in Python', 'MIT'),
    ('cmudict', 'A versioned python wrapper package for The CMU Pronouncing Dictionary data files.', 'GPL-3.0'),
    ('colorlog', 'Log formatting with colors!', 'MIT License'),
    ('colorlover', 'Color scales for IPython notebook', np.nan),
    ('confuse', 'painless YAML configuration', 'MIT'),
    ('conllu', 'CoNLL-U Parser parses a CoNLL-U formatted string into a nested python dictionary', np.nan),
    ('convertdate', "Converts between Gregorian dates and other calendar systems.", 'MIT'),
    ('conx', 'On-Ramp to Deep Learning. Built on Keras', np.nan),
    ('cssselect2', 'CSS selectors for Python ElementTree', 'BSD'),
    ('cufflinks', 'Productivity Tools for Plotly + Pandas', 'MIT'),
    ('cvxpy', 'A domain-specific language for modeling convex optimization problems in Python.', 'Apache License, Version 2.0'),
    ('cymem', 'Manage calls to calloc/free through Cython', 'MIT'),
    ('cysignals', 'Interrupt and signal handling for Cython', 'GNU Lesser General Public License, version 3 or later'),
    ('dask-xgboost', 'Interactions between Dask and XGBoost', 'BSD'),
    ('dataclasses', 'A backport of the dataclasses module for Python 3.6', 'Apache'),
    ('deap', 'Distributed Evolutionary Algorithms in Python', 'LGPL'),
    ('deepdish', 'Deep Learning experiments from University of Chicago.', 'BSD'),
    ('descartes', 'Use geometric objects as matplotlib paths and patches', 'BSD'),
    ('dipy', 'Diffusion MRI utilities in python', 'BSD license'),
    ('dora', 'Exploratory data analysis toolkit for Python', 'MIT'),
    ('editdistance', 'Fast implementation of the edit distance(Levenshtein distance)', np.nan),
    ('edward', 'A library for probabilistic modeling, inference, and criticism', 'Apache License 2.0'),
    ('eli5', 'Debug machine learning classifiers and explain their predictions', 'MIT license'),
    ('emoji', 'Emoji for Python', 'New BSD'),
    ('essentia', 'Library for audio and music analysis, description and synthesis', 'AGPLv3'),
    ('et-xmlfile', 'An implementation of lxml.xmlfile for the standard library', 'MIT'),
    ('ethnicolr', 'Predict Race/Ethnicity Based on Name', 'MIT'),
    ('fancyimpute', 'Matrix completion and feature imputation algorithms', 'http://www.apache.org/licenses/LICENSE-2.0.html'),
    ('fastFM', np.nan, 'BSD'),
    ('fastai', 'fastai makes deep learning with PyTorch faster, more accurate, and easier', 'Apache Software License 2.0'),
    ('fasteners', 'A python package that provides useful locks.', 'ASL 2.0'),
    ('fastprogress', 'A nested progress with plotting options for fastai', 'Apache License 2.0'),
    ('fasttext', 'fasttext Python bindings', 'MIT'),
    ('fbpca', 'Fast computations of PCA/SVD/eigendecompositions via randomized methods', 'BSD License'),
    ('fbprophet', 'Automatic Forecasting Procedure', 'BSD'),
    ('feather-format', 'Simple wrapper library to the Apache Arrow-based Feather File Format', 'Apache License, Version 2.0'),
    ('featuretools', 'a framework for automated feature engineering', 'BSD 3-clause'),
    ('fitter', 'A tool to fit data to many distributions and best one(s)', 'GPL'),
    ('flashtext', 'Extract/Replaces keywords in sentences.', np.nan),
    ('folium', 'Make beautiful maps with Leaflet.js & Python', 'MIT'),
    ('fsspec', 'File-system specification', 'BSD'),
    ('ftfy', 'Fixes some problems with Unicode text after the fact', 'MIT'),
    ('funcsigs', 'Python function signatures from PEP362 for Python 2.6, 2.7 and 3.2+', 'ASL'),
    ('funcy', 'A fancy and practical functional tools', 'BSD'),
    ('fury', 'Free Unified Rendering in Python', 'BSD (3-clause)'),
    ('fuzzywuzzy', 'Fuzzy string matching in python', 'GPL'),
    ('gast', 'Python AST that abstracts the underlying Python version', 'BSD 3-Clause'),
    ('gatspy', 'General tools for Astronomical Time Series in Python', 'BSD 3-clause'),
    ('gdbn', 'Pre-trained deep neural networks', 'MIT (see license.txt)'),
    ('geographiclib', 'The geodesic routines from GeographicLib', 'MIT'),
    ('geojson', 'Python bindings and utilities for GeoJSON', 'BSD'),
    ('geopandas', 'Geographic pandas extensions', 'BSD'),
    ('geoplot', 'High-level geospatial plotting for Python.', np.nan),
    ('geopy', 'Python Geocoding Toolbox', 'MIT'),
    ('geoviews', 'GeoViews is a Python library that makes it easy to explore and visualize geographical datasets.', 'BSD 3-Clause'),
    ('ggplot', 'ggplot for python', 'BSD'),
    ('glmnet-py', 'Python version of glmnet, originally from Stanford University, modified by Han Fang', 'GPL-2'),
    ('gluoncv', 'MXNet Gluon CV Toolkit', 'Apache-2.0'),
    ('gluonnlp', 'MXNet Gluon NLP Toolkit', 'Apache-2.0'),
    ('gnumpy', "Almost identical to numpy, but does its computations on your computer's  GPU, using Cudamat.", 'BSD-derived (see LICENSE.txt)'),
    ('google-api-core', 'Google API client core library', 'Apache 2.0'),
    ('google-api-python-client', 'Google API Client Library for Python', 'Apache 2.0'),
    ('google-auth', 'Google Authentication Library', 'Apache 2.0'),
    ('google-auth-httplib2', 'Google Authentication Library: httplib2 transport', 'Apache 2.0'),
    ('google-cloud-automl', 'Cloud AutoML API client library', 'Apache 2.0'),
    ('google-cloud-bigquery', 'Google BigQuery API client library', 'Apache 2.0'),
    ('google-cloud-core', 'Google Cloud API client core library', 'Apache 2.0'),
    ('google-cloud-storage', 'Google Cloud Storage API client library', 'Apache 2.0'),
    ('google-pasta', 'pasta is an AST-based Python refactoring library', 'Apache 2.0'),
    ('google-resumable-media', 'Utilities for Google Media Downloads and Resumable Uploads', 'Apache 2.0'),
    ('googleapis-common-protos', 'Common protobufs used in Google APIs', 'Apache-2.0'),
    ('gplearn', 'Genetic Programming in Python, with a scikit-learn inspired API', 'new BSD'),
    ('gpxpy', 'GPX file parser and GPS track manipulation library', 'Apache License, Version 2.0'),
    ('grpcio', 'HTTP/2-based RPC framework', 'Apache License 2.0'),
    ('gym', 'The OpenAI Gym: A toolkit for developing and comparing your reinforcement learning agents.', np.nan),
    ('haversine', 'Calculate the distance between 2 points on Earth.', "['MIT']"),
    ('heamy', 'A set of useful tools for competitive data science.', 'MIT'),
    ('hep-ml', 'Machine Learning for High Energy Physics', 'Apache 2.0'),
    ('hmmlearn', np.nan, 'new BSD'),
    ('holidays', 'Generate and work with holidays in Python', 'MIT'),
    ('hpsklearn', 'Hyperparameter Optimization for sklearn', 'BSD'),
    ('htmlmin', 'An HTML Minifier', 'BSD'),
    ('httplib2', 'A comprehensive HTTP client library.', 'MIT'),
    ('hunspell', 'Module for the Hunspell spellchecker engine', 'LGPLv3'),
    ('husl', 'Human-friendly HSL', 'MIT'),
    ('hyperopt', 'Distributed Asynchronous Hyperparameter Optimization', 'BSD'),
    ('hypertools', 'A python package for visualizing and manipulating high-dimensional data', 'MIT'),
    ('hypothesis', 'A library for property based testing', 'MPL v2'),
    ('ijson', 'Iterative JSON parser with a standard Python iterator interface', 'BSD'),
    ('imbalanced-learn', 'Toolbox for imbalanced dataset in machine learning.', 'MIT'),
    ('imgaug', 'Image augmentation library for deep neural networks', 'MIT'),
    ('implicit', 'Collaborative Filtering for Implicit Datasets', 'MIT'),
    ('importlib-metadata', 'Read metadata from Python packages', 'Apache Software License'),
    ('ipython-genutils', 'Vestigial utilities from IPython', 'BSD'),
    ('iso3166', 'Self-contained ISO 3166-1 country definitions.', 'MIT'),
    ('isoweek', 'Objects representing a week', 'BSD'),
    ('jieba', 'Chinese Words Segementation Utilities', 'MIT'),
    ('jmespath', 'JSON Matching Expressions', 'MIT'),
    ('jsonnet', 'Python bindings for Jsonnet - The data templating language', np.nan),
    ('jsonpickle', 'Python library for serializing any arbitrary object graph into JSON', 'BSD'),
    ('jupyter-client', 'Jupyter protocol implementation and client libraries', 'BSD'),
    ('jupyter-console', 'Jupyter terminal console', 'BSD'),
    ('jupyter-core', 'Jupyter core package. A base package on which Jupyter projects rely.', 'BSD'),
    ('jupyter-tensorboard', 'Start tensorboard in Jupyter! Jupyter notebook integration for tensorboard.', 'MIT License'),
    ('jupyterlab-server', 'JupyterLab Server', 'BSD'),
    ('keras-rcnn', np.nan, 'MIT'),
    ('keras-resnet', np.nan, 'MIT'),
    ('keras-rl', 'Deep Reinforcement Learning for Keras', 'MIT'),
    ('keras-tqdm', 'Keras models with TQDM progress bars in Jupyter notebooks', 'MIT'),
    ('kmapper', 'Python implementation of Mapper algorithm for Topological Data Analysis.', 'MIT'),
    ('kmeans-smote', 'Oversampling for imbalanced learning based on k-means and SMOTE', 'MIT'),
    ('kmodes', 'Python implementations of the k-modes and k-prototypes clustering algorithms for clustering categorical data.', 'MIT'),
    ('knnimpute', 'k-Nearest Neighbor imputation', 'http://www.apache.org/licenses/LICENSE-2.0.html'),
    ('ktext', 'Pre-processing text in parallel for Keras in python.', 'MIT'),
    ('langdetect', "Language detection library ported from Google's language-detection.", 'Copyright 2014-2015 Michal "Mimino" Danilak, Apache License, Version 2.0'),
    ('langid', 'langid.py is a standalone Language Identification (LangID) tool.', 'BSD'),
    ('leven', 'Levenshtein edit distance library', 'UNKNOWN'),
    ('libarchive-c', 'Python interface to libarchive', 'CC0'),
    ('librosa', 'Python module for audio and music processing', 'ISC'),
    ('lief', 'LIEF is a library to instrument executable formats', 'Apache 2.0'),
    ('lightfm', 'LightFM recommendation model', 'MIT'),
    ('lightgbm', 'LightGBM Python Package', 'The MIT License (Microsoft)'),
    ('lime', 'Local Interpretable Model-Agnostic Explanations for machine learning classifiers', 'BSD'),
    ('line-profiler', 'Line-by-line profiler.', 'BSD'),
    ('lml', 'Load me later. A lazy plugin management system.', 'New BSD'),
    ('lunardate', 'A Chinese Calendar Library in Pure Python', 'GPLv3'),
    ('marisa-trie', 'Static memory-efficient and fast Trie-like structures for Python.', 'MIT'),
    ('markovify', 'A simple, extensible Markov chain generator. Uses include generating random semi-plausible sentences based on an existing text.', 'MIT'),
    ('matplotlib-venn', 'Functions for plotting area-proportional two- and three-way Venn diagrams in matplotlib.', 'MIT'),
    ('memory-profiler', 'A module for monitoring memory usage of a python program', 'BSD'),
    ('missingno', 'Missing data visualization module for Python.', np.nan),
    ('mizani', 'Scales for Python', 'BSD (3-clause)'),
    ('mkl-fft', 'MKL-based FFT transforms for NumPy arrays', 'Proprietary - Intel'),
    ('mkl-random', 'NumPy-based implementation of random number generation sampling using Intel (R) Math Kernel Library.', 'Proprietary - Intel'),
    ('ml-metrics', 'Machine Learning Evaluation Metrics', np.nan),
    ('mlcrate', 'A collection of handy python tools and functions, mainly for ML and Kaggle.', 'MIT'),
    ('mlens', 'Machine Learning Ensemble Library', 'MIT'),
    ('mlxtend', 'Machine Learning Library Extensions', 'BSD 3-Clause'),
    ('mmh3', 'Python wrapper for MurmurHash (MurmurHash3), a set of fast and robust hash functions.', 'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'),
    ('mne', 'MNE python project for MEG and EEG data analysis.', 'BSD (3-clause)'),
    ('mnist', 'Python utilities to download and parse the MNIST dataset', 'BSD'),
    ('monotonic', 'An implementation of time.monotonic() for Python 2 & < 3.3', 'Apache'),
    ('mplleaflet', 'Convert Matplotlib plots into Leaflet web maps', 'BSD 3-clause'),
    ('msgpack', 'MessagePack (de)serializer.', 'Apache 2.0'),
    ('msgpack-numpy', 'Numpy data serialization using msgpack', 'BSD'),
    ('multiprocess', 'better multiprocessing and multithreading in python', 'BSD'),
    ('murmurhash', 'Cython bindings for MurmurHash', 'MIT'),
    ('mxnet', 'MXNet is an ultra-scalable deep learning framework. This version uses openblas.', 'Apache 2.0'),
    ('nervananeon', "Intel's deep learning framework", 'License :: OSI Approved :: Apache Software License'),
    ('nibabel', 'Access a multitude of neuroimaging data formats', 'MIT License'),
    ('nilearn', 'Statistical learning for neuroimaging in Python', 'new BSD'),
    ('nolearn', 'scikit-learn compatible neural network library', 'MIT'),
    ('numdifftools', 'Solves automatic numerical differentiation problems in one or more variables.', 'new BSD'),
    ('nvidia-ml-py3', 'Python Bindings for the NVIDIA Management Library', 'BSD'),
    ('odfpy', 'Python API and tools to manipulate OpenDocument files', np.nan),
    ('onnx', 'Open Neural Network Exchange', np.nan),
    ('opencv-python', 'Wrapper package for OpenCV python bindings.', 'MIT'),
    ('opencv-python-headless', 'Wrapper package for OpenCV python bindings.', 'MIT'),
    ('optuna', 'A hyperparameter optimization framework', np.nan),
    ('orderedmultidict', 'Ordered Multivalue Dictionary', 'Unlicense'),
    ('ortools', 'Google OR-Tools python libraries and modules', 'Apache 2.0'),
    ('osmnx', 'Retrieve, model, analyze, and visualize OpenStreetMap street networks and other spatial data', 'MIT'),
    ('osqp', 'OSQP: The Operator Splitting QP Solver', 'Apache 2.0'),
    ('overrides', 'A decorator to automatically detect mismatch when overriding a method.', 'Apache License, Version 2.0'),
    ('palettable', 'Color palettes for Python', np.nan),
    ('pandas-summary', 'An extension to pandas describe function.', 'MIT'),
    ('paramnb', 'Generate ipywidgets from Parameterized objects in the notebook', 'BSD 3-Clause License'),
    ('parsimonious', '(Soon to be) the fastest pure-Python PEG parser I could muster', 'MIT'),
    ('pathos', 'parallel graph management and execution in heterogeneous computing', '3-clause BSD'),
    ('pbr', 'Python Build Reasonableness', np.nan),
    ('pdf2image', 'A wrapper around the pdftoppm and pdftocairo command line tools to convert PDF to a PIL Image list.', 'MIT'),
    ('phik', 'Phi_K correlation analyzer library', np.nan),
    ('plotly-express', 'Plotly Express - a high level wrapper for Plotly.py', 'MIT'),
    ('plotnine', 'A grammar of graphics for python', 'GPL-2'),
    ('polyglot', 'Polyglot is a natural language pipeline that supports massive multilingual applications.', 'GPLv3'),
    ('posix-ipc', 'POSIX IPC primitives (semaphores, shared memory and message queues) for Python', 'http://creativecommons.org/licenses/BSD/'),
    ('pox', 'utilities for filesystem exploration and automated builds', '3-clause BSD'),
    ('ppca', 'Probabilistic PCA', np.nan),
    ('ppft', 'distributed and parallel python', 'BSD-like'),
    ('preprocessing', 'pre-processing package for text strings', 'MIT'),
    ('preshed', 'Cython hash table that trusts the keys are pre-hashed', 'MIT'),
    ('prettytable', 'A simple Python library for easily displaying tabular data in a visually appealing ASCII table format.', 'BSD'),
    ('progressbar2', 'A Python Progressbar library to provide visual (yet text based) progress to long running operations.', 'BSD'),
    ('prometheus-client', 'Python client for the Prometheus monitoring system.', 'Apache Software License 2.0'),
    ('prompt-toolkit', 'Library for building powerful interactive command lines in Python', 'BSD-3-Clause'),
    ('pronouncing', 'A simple interface for the CMU pronouncing dictionary', 'BSD'),
    ('pudb', 'A full-screen, console-based Python debugger', np.nan),
    ('py-cpuinfo', 'Get CPU info with pure Python 2 & 3', 'MIT'),
    ('py-lz4framed', 'LZ4Frame library for Python (via C bindings)', 'Apache License 2.0'),
    ('py-stringmatching', 'Python library for string matching.', 'BSD'),
    ('py-stringsimjoin', 'Python library for performing string similarity joins.', 'BSD'),
    ('pyLDAvis', 'Interactive topic model visualization. Port of the R package.', 'MIT'),
    ('pyOpenSSL', 'Python wrapper module around the OpenSSL library', 'Apache License, Version 2.0'),
    ('pyPdf', 'PDF toolkit', 'UNKNOWN'),
    ('pyahocorasick', 'pyahocorasick is a fast and memory efficient library for exact or approximate multi-pattern string search.', ' BSD-3-Clause and Public-Domain'),
    ('pyarrow', 'Python library for Apache Arrow', 'Apache License, Version 2.0'),
    ('pybind11', 'Seamless operability between C++11 and Python', 'BSD'),
    ('pycairo', 'Python interface for cairo', np.nan),
    ('pycountry', 'ISO country, subdivision, language, currency and script definitions and their translations', 'LGPL 2.1'),
    ('pyct', 'python package common tasks for users (e.g. copy examples, fetch data, ...)', 'BSD 3-Clause License'),
    ('pydash', 'The kitchen sink of Python utility libraries for doing "stuff" in a functional way. Based on the Lo-Dash Javascript library.', 'MIT License'),
    ('pydicom', 'Pure python package for DICOM medical file reading and writing', 'MIT'),
    ('pyexcel-io', 'A python library to read and write structured data in csv, zipped csvformat and to/from databases', 'New BSD'),
    ('pyexcel-ods', 'A wrapper library to read, manipulate and write data in ods format', 'New BSD'),
    ('pyfasttext', 'Yet another Python binding for fastText', 'GPLv3'),
    ('pyflux', 'PyFlux: A time-series analysis library for Python', 'BSD'),
    ('pyglet', 'Cross-platform windowing and multimedia library', 'BSD'),
    ('pykalman', 'An implementation of the Kalman Filter, Kalman Smoother, and EM algorithm in Python', 'BSD'),
    ('pykoko', 'KOKO is an easy-to-use entity extraction tool', 'Apache Software License 2.0'),
    ('pymagnitude', 'A fast, efficient universal vector embedding utility package.', 'MIT'),
    ('pyocr', 'A Python wrapper for OCR engines (Tesseract, Cuneiform, etc)', 'GPLv3+'),
    ('pypandoc', 'Thin wrapper for pandoc.', 'MIT'),
    ('pyperclip', 'A cross-platform clipboard module for Python. (Only handles plain text for now.)', 'BSD'),
    ('pytagcloud', 'Create beautiful tag clouds as images or HTML', 'BSD'),
    ('pytesseract', "Python-tesseract is a python wrapper for Google's Tesseract-OCR", 'GPLv3'),
    ('pytest-pylint', 'pytest plugin to check source code with pylint', 'MIT'),
    ('pytext-nlp', 'pytorch modeling framework and model zoo for text models', 'BSD'),
    ('python-Levenshtein', 'Python extension for computing string edit distances and similarities.', 'GPL'),
    ('python-igraph', 'High performance graph data structures and algorithms', 'GNU General Public License (GPL)'),
    ('python-louvain', 'Louvain algorithm for community detection', 'BSD'),
    ('pytorch-ignite', 'A lightweight library to help with training neural networks in PyTorch.', 'BSD'),
    ('pytorch-pretrained-bert', 'PyTorch version of Google AI BERT model with script to load Google pre-trained models', 'Apache'),
    ('pyviz-comms', 'Bidirectional communication for the PyViz ecosystem.', 'BSD'),
    ('raccoon', 'Python DataFrame with fast insert and appends', 'MIT'),
    ('randomgen', 'Random generator supporting multiple PRNGs', 'NCSA'),
    ('ray', 'A system for parallel and distributed Python that unifies the ML ecosystem.', 'Apache 2.0'),
    ('resampy', 'Efficient signal resampling', 'ISC'),
    ('retrying', 'Retrying', 'Apache 2.0'),
    ('revrand', 'A library of scalable Bayesian generalized linear models with fancy features', 'Apache Software License 2.0'),
    ('rf-perm-feat-import', 'Random Forest Permutate Feature Importance', 'MIT'),
    ('rgf-python', 'Scikit-learn Wrapper for Regularized Greedy Forest', 'MIT License'),
    ('rsa', 'Pure-Python RSA implementation', 'ASL 2'),
    ('ruamel-yaml', 'ruamel.yaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order', 'MIT license'),
    ('s2sphere', 'Python implementation of the S2 Geometry Library', 'MIT'),
    ('s3transfer', 'An Amazon S3 Transfer Manager', 'Apache License 2.0'),
    ('sacred', 'Facilitates automated and reproducible experimental research', np.nan),
    ('scattertext', 'An NLP package to visualize interesting terms in text.', 'Apache 2.0'),
    ('scikit-multilearn', 'Scikit-multilearn is a BSD-licensed library for multi-label classification that is built on top of the well-known scikit-learn ecosystem.', 'BSD'),
    ('scikit-optimize', 'Sequential model-based optimization toolbox.', 'BSD'),
    ('scikit-plot', 'An intuitive library to add plotting functionality to scikit-learn objects.', 'MIT License'),
    ('scikit-surprise', 'An easy-to-use library for recommender systems.', 'GPLv3+'),
    ('scs', 'scs: splitting conic solver', 'MIT'),
    ('sentencepiece', 'SentencePiece python wrapper', 'Apache'),
    ('setuptools-git', 'Setuptools revision control system plugin for Git', 'BSD'),
    ('shap', 'A unified approach to explain the output of any machine learning model.', 'MIT'),
    ('sklearn', 'A set of python modules for machine learning and data mining', 'UNKNOWN'),
    ('sklearn-contrib-lightning', 'Large-scale sparse linear classification, regression and ranking in Python', 'new BSD'),
    ('sklearn-contrib-py-earth', "A Python implementation of Jerome Friedman's Multivariate Adaptive Regression Splines.", 'LICENSE.txt'),
    ('sklearn-pandas', 'Pandas integration with sklearn', np.nan),
    ('smart-open', 'Utils for streaming large files (S3, HDFS, gzip, bz2...)', 'MIT'),
    ('smhasher', 'Python extension for smhasher hash functions', 'UNKNOWN'),
    ('spectral', 'Spectral Python (SPy) is a Python module for hyperspectral image processing.', 'GPL'),
    ('speedml', 'Speedml Machine Learning Speed Start', 'MIT'),
    ('sphinx-rtd-theme', 'Read the Docs theme for Sphinx', 'MIT'),
    ('squarify', 'Pure Python implementation of the squarify treemap layout algorithm', 'Apache v2'),
    ('srsly', 'Modern high-performance serialization utilities for Python', 'MIT'),
    ('stemming', np.nan, np.nan),
    ('stevedore', 'Manage dynamic plugins for Python applications', np.nan),
    ('stop-words', 'Get list of common stop words in various languages in Python', 'Copyright (c) 2014, Alireza Savand, Contributors'),
    ('stopit', 'Timeout control decorator and context managers, raise any exception in another thread', 'GPLv3'),
    ('svgwrite', 'A Python library to create SVG drawings.', 'MIT License'),
    ('tables', 'Hierarchical datasets for Python', 'BSD 2-Clause'),
    ('tabulate', 'Pretty-print tabular data', 'MIT'),
    ('tensorboard', 'TensorBoard lets you watch Tensors Flow', 'Apache 2.0'),
    ('tensorboardX', 'TensorBoardX lets you watch Tensors Flow without Tensorflow', 'MIT license'),
    ('tensorflow-estimator', 'TensorFlow Estimator.', 'Apache 2.0'),
    ('tensorflow-hub', 'TensorFlow Hub is a library to foster the publication, discovery, and consumption of reusable parts of machine learning models.', 'Apache 2.0'),
    ('tensorflow-probability', 'Probabilistic modeling and statistical inference in TensorFlow', 'Apache 2.0'),
    ('tensorforce', 'Reinforcement learning for TensorFlow', 'Apache 2.0'),
    ('tensorpack', 'A Neural Network Training Interface on TensorFlow', 'Apache'),
    ('terminalplot', 'Plot points in terminal', 'GPL'),
    ('textacy', 'NLP, before and after spaCy', 'Apache'),
    ('textblob', 'Simple, Pythonic text processing. Sentiment analysis, part-of-speech tagging, noun phrase parsing, and more.', 'MIT'),
    ('tflearn', 'Deep Learning Library featuring a higher-level API for TensorFlow', 'MIT'),
    ('thinc', 'Practical Machine Learning for NLP', 'MIT'),
    ('tifffile', 'Read and write TIFF(r) files', 'BSD'),
    ('tinycss2', 'Low-level CSS parser for Python', 'BSD'),
    ('torch', 'Tensors and Dynamic neural networks in Python with strong GPU acceleration', 'BSD-3'),
    ('torchaudio', 'An audio package for PyTorch', np.nan),
    ('torchtext', 'Text utilities and datasets for PyTorch', 'BSD'),
    ('trackml', 'An opinionated, minimal cookiecutter template for Python packages', np.nan),
    ('trueskill', 'The video game rating system', 'BSD'),
    ('tsfresh', 'tsfresh extracts relevant characteristics from time series', 'MIT'),
    ('typing-extensions', 'Backported and Experimental Type Hints for Python 3.5+', 'PSF'),
    ('tzlocal', 'tzinfo object for the local timezone', 'MIT'),
    ('umap-learn', 'Uniform Manifold Approximation and Projection', 'BSD'),
    ('update-checker', 'A python module that will check for package updates.', 'Simplified BSD License'),
    ('uritemplate', 'URI templates', 'BSD 3-Clause License or Apache License, Version 2.0'),
    ('urwid', 'A full-featured console (xterm et al.) user interface library', 'LGPL'),
    ('vecstack', 'Python package for stacking (machine learning technique)', 'MIT'),
    ('vega3', 'Deprecated: please use vega', 'BSD 3-clause'),
    ('vida', 'Python binding for Vida data visualizations', 'UNKNOWN'),
    ('vowpalwabbit', 'Vowpal Wabbit Python package', 'BSD 3-Clause License'),
    ('vtk', 'VTK is an open-source toolkit for 3D computer graphics, image processing, and visualization', 'BSD'),
    ('wasabi', 'A lightweight console printing and formatting toolkit', 'MIT'),
    ('wavio', 'A Python module for reading and writing WAV files using numpy arrays.', 'BSD'),
    ('websocket-client', 'WebSocket client for Python. hybi13 is supported.', 'BSD'),
    ('wfdb', 'The WFDB Python Toolbox', 'MIT'),
    ('word2number', 'Convert number words eg. three hundred and forty two to numbers (342).', 'MIT'),
    ('wordcloud', 'A little word cloud generator', 'MIT'),
    ('wordsegment', 'English word segmentation.', 'Apache 2.0'),
    ('xgboost', 'XGBoost Python Package', 'Apache-2.0'),
    ('xvfbwrapper', 'run headless display inside X virtual framebuffer (Xvfb)', 'MIT'),
    ('xxhash', 'Python binding for xxHash', 'BSD'),
    ('yellowbrick', 'A suite of visual analysis and diagnostic tools for machine learning.', 'Apache 2'),
]

pypi_metadata = pd.DataFrame(
    descriptions,
    columns=['package_name', 'summary', 'license']
)
pypi_metadata.set_index('package_name', inplace=True)
pypi_metadata.to_csv('pypi-package-metadata.csv', header=True)
