# Useful functions and constants from
# https://www.kaggle.com/ajrwhite/covid-19-thematic-tagging-with-regular-expressions/notebook

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
import os
from IPython.core.display import display, HTML

# Fix DOI links
def doi_url(d):
    if d.startswith('http'):
        return d
    elif d.startswith('doi.org'):
        return f'http://{d}'
    else:
        return f'http://doi.org/{d}'
    
# Turn authors list into '<surname>' or '<surname> et al'
def shorten_authors(authors):
    if isinstance(authors, str):
        authors = authors.split(';')
        if len(authors) == 1:
            return authors[0].split(',')[0]
        else:
            return f'{authors[0].split(",")[0]} et al'
    else:
        return authors

def load_metadata(metadata_file):
    df = pd.read_csv(metadata_file,
                 dtype={'Microsoft Academic Paper ID': str,
                        'pubmed_id': str},
                 low_memory=False)
    df.doi = df.doi.fillna('').apply(doi_url)
    df['authors_short'] = df.authors.apply(shorten_authors)
    df['sorting_date'] = pd.to_datetime(df.publish_time)
    print(f'loaded DataFrame with {len(df)} records')
    return df.sort_values('sorting_date', ascending=False)

def abstract_title_filter(df, search_string):
    return (df.abstract.str.lower().str.replace('-', ' ')
            .str.contains(search_string, na=False) |
            df.title.str.lower().str.replace('-', ' ')
            .str.contains(search_string, na=False))

# Helper function which counts synonyms and adds tag column to DF
def count_and_tag(df: pd.DataFrame,
                  synonym_list: list,
                  tag_suffix: str) -> (pd.DataFrame, pd.Series):
    counts = {}
    df[f'tag_{tag_suffix}'] = False
    for s in synonym_list:
        synonym_filter = abstract_title_filter(df, s)
        counts[s] = sum(synonym_filter)
        df.loc[synonym_filter, f'tag_{tag_suffix}'] = True
    print(f'Added tag_{tag_suffix} to DataFrame')
    return df, pd.Series(counts)

# Function for printing out key passage of abstract based on key terms
def print_key_phrases(df, key_terms, n=5, chars=300):
    for ind, item in enumerate(df[:n].itertuples()):
        print(f'{ind+1} of {len(df)}')
        print(item.title)
        print('[ ' + item.doi + ' ]')
        try:
            i = len(item.abstract)
            for kt in key_terms:
                kt = kt.replace(r'\b', '')
                term_loc = item.abstract.lower().find(kt)
                if term_loc != -1:
                    i = min(i, term_loc)
            if i < len(item.abstract):
                print('    "' + item.abstract[i-30:i+chars-30] + '"')
            else:
                print('    "' + item.abstract[:chars] + '"')
        except:
            print('NO ABSTRACT')
        print('---')
        
def add_tag_covid19(df):
    # Customised approach to include more complicated logic
    df, covid19_counts = count_and_tag(df, COVID19_SYNONYMS, 'disease_covid19')
    novel_corona_filter = (abstract_title_filter(df, 'novel corona') &
                           df.publish_time.str.startswith('2020', na=False))
    df.loc[novel_corona_filter, 'tag_disease_covid19'] = True
    covid19_counts = covid19_counts.append(pd.Series(index=['novel corona'],
                                                     data=[novel_corona_filter.sum()]))
    return df, covid19_counts


def load_full_text(df, data_folder):
    json_list = []
    # Adding code to handle PDF vs. XML parse
    for row in df[df.has_pdf_parse].itertuples():
        filename = f'{row.sha}.json'
        sources = ['biorxiv_medrxiv', 'comm_use_subset',
                   'custom_license', 'noncomm_use_subset']
        for source in sources:
            if filename in os.listdir(os.path.join(data_folder, source, source, 'pdf_json')):
                with open(os.path.join(data_folder, source, source, 'pdf_json', filename), 'rb') as f:
                    json_list.append(json.load(f))
    for row in df[df.has_pmc_xml_parse].itertuples():
        filename = f'{row.sha}.json'
        sources = ['comm_use_subset',
                   'custom_license', 'noncomm_use_subset']
        for source in sources:
            if filename in os.listdir(os.path.join(data_folder, source, source, 'pmc_json')):
                with open(os.path.join(data_folder, source, source, 'pmc_json', filename), 'rb') as f:
                    json_list.append(json.load(f))
    print(f'Found {len(json_list)} full texts for {len(df)} records')
    return json_list


def display_dataframe(df, title):
    text = f'<h2>{title}</h2><table><tr>'
    text += ''.join([f'<td><b>{col}</b></td>' for col in df.columns.values]) + '</tr>'
    for row in df.itertuples():
        text +=  '<tr>' + ''.join([f'<td valign="top">{v}</td>' for v in row[1:]]) + '</tr>'
    text += '</table>'
    display(HTML(text))
    

# CONSTANTS

COVID19_SYNONYMS = [
                    'covid',
                    'coronavirus disease 19',
                    'sars cov 2', # Note that search function replaces '-' with ' '
                    '2019 ncov',
                    '2019ncov',
                    r'2019 n cov\b',
                    r'2019n cov\b',
                    'ncov 2019',
                    r'\bn cov 2019',
                    'coronavirus 2019',
                    'wuhan pneumonia',
                    'wuhan virus',
                    'wuhan coronavirus',
                    r'coronavirus 2\b'
]

#Add terms that will pick up all memebers of the Coronaviridae family
#https://en.wikipedia.org/wiki/Coronaviridae
# 'corona' and 'cov' will not pick up these viruses
#Data from International Committee on Taxonomy of Viruses and National Center for Biotechnology Information

CORONAVIRIDAE_SYMNONYMS = ['corona', r'\bcov\b', 'avian infectious bronchitis virus',
                            'feline infectious peritonitis virus',
                            'glaucous-winged gull cir-66002',
                            'infectious bronchitis virus',
                            'murine hepatitis virus',
                            'porcine epidemic diarrhea virus',
                            'porcine hemagglutinating encephalomyelitis virus',
                            'transmissible gastroenteritis virus',
                            'prcv isu-1',
                            'sialodacryoadenitis virus',
                            'tgev miller m6',
                            'tgev miller m60',
                            'tgev purdue p115',
                            'tgev virulent purdue']

AGE_SYNONYMS = ['median age',
                'mean age',
                'average age',
                'elderly',
                r'\baged\b',
                r'\bold',
                'young',
                'teenager',
                'adult',
                'child'
               ]

SEX_SYNONYMS = ['sex',
                'gender',
                r'\bmale\b',
                r'\bfemale\b',
                r'\bmales\b',
                r'\bfemales\b',
                r'\bmen\b',
                r'\bwomen\b'
               ]

BODYWEIGHT_SYNONYMS = [
    'overweight',
    'over weight',
    'obese',
    'obesity',
    'bodyweight',
    'body weight',
    r'\bbmi\b',
    'body mass',
    'body fat',
    'bodyfat',
    'kilograms',
    r'\bkg\b', # e.g. 70 kg
    r'\dkg\b'  # e.g. 70kg
]

SMOKING_SYNONYMS = ['smoking',
                    'smoke',
                    'cigar', # this picks up cigar, cigarette, e-cigarette, etc.
                    'nicotine',
                    'cannabis',
                    'marijuana']

DIABETES_SYNONYMS = [
    'diabet', # picks up diabetes, diabetic, etc.
    'insulin', # any paper mentioning insulin likely to be relevant
    'blood sugar',
    'blood glucose',
    'ketoacidosis',
    'hyperglycemi', # picks up hyperglycemia and hyperglycemic
]

HYPERTENSION_SYNONYMS = [
    'hypertension',
    'blood pressure',
    r'\bhbp\b', # HBP = high blood pressure
    r'\bhtn\b' # HTN = hypertension
]

IMMUNODEFICIENCY_SYNONYMS = [
    'immune deficiency',
    'immunodeficiency',
    r'\bhiv\b',
    r'\baids\b'
    'granulocyte deficiency',
    'hypogammaglobulinemia',
    'asplenia',
    'dysfunction of the spleen',
    'spleen dysfunction',
    'complement deficiency',
    'neutropenia',
    'neutropaenia', # alternate spelling
    'cell deficiency' # e.g. T cell deficiency, B cell deficiency
]

CANCER_SYNONYMS = [
    'cancer',
    'malignant tumour',
    'malignant tumor',
    'melanoma',
    'leukemia',
    'leukaemia',
    'chemotherapy',
    'radiotherapy',
    'radiation therapy',
    'lymphoma',
    'sarcoma',
    'carcinoma',
    'blastoma',
    'oncolog'
]

CHRONICRESP_SYNONYMS = [
    'chronic respiratory disease',
    'asthma',
    'chronic obstructive pulmonary disease',
    r'\bcopd',
    'chronic bronchitis',
    'emphysema'
]

IMMUNITY_SYNONYMS = [
    'immunity',
    r'\bvaccin',
    'innoculat'
]

CLIMATE_SYNONYMS = [
    'climate',
    'weather',
    'humid',
    'sunlight',
    'air temperature',
    'meteorolog', # picks up meteorology, meteorological, meteorologist
    'climatolog', # as above
    'dry environment',
    'damp environment',
    'moist environment',
    'wet environment',
    'hot environment',
    'cold environment',
    'cool environment'
]

TRANSMISSION_SYNONYMS = [
    'transmiss', # Picks up 'transmission' and 'transmissibility'
    'transmitted',
    'incubation',
    'environmental stability',
    'airborne',
    'via contact',
    'human to human',
    'through droplets',
    'through secretions',
    r'\broute',
    'exportation'
]

REPR_SYNONYMS = [
    r'reproduction \(r\)',
    'reproduction rate',
    'reproductive rate',
    '{r}_0',
    r'\br0\b',
    r'\br_0',
    '{r_0}',
    r'\b{r}',
    r'\br naught',
    r'\br zero'
]

INCUBATION_SYNONYMS = [
    'incubation period',
    'period of incubation',
    'latent period',
    'latency period',
    'period of latency',
    'window period'
]

PERSISTENCE_SYNONYMS = ['persistence',
                        # r'(?<!viral )surface[s]?\b', # THIS DOESN'T WORK
                        'survival surface',
                        'persistence surface',
                        'survival on a surface',
                        'persistence on a surface',
                        'carrier test',
                        'suspension test',
                        'fomite',
                        # 'survival time',
                        'environmental surface',
                        'environmental stability',
                        'environmental reservoirs',
                        'environmental survival',
                        'pathogens in the environment',
                        'environmental pathogen',
                        'contaminated',
                        'contamination',
                        'surface stability',
                        'surface swab',
                        'inanimate surface',
                        'surface disinfection'
                       ]

