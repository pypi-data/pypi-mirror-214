# module doc string
"""
This module extracts skills from free text and output them in accordance to SST skill terms
author: - Lois Ji
        - Leo Li
date: Mar 1, 2022
"""
import pickle
import yaml
import pandas as pd
from tqdm import tqdm
from ssg_sea.utils import *
from ssg_sea.config.core import CONFIG_FILE_PATH, PICKLE_FILE_PATH

import warnings
warnings.filterwarnings("ignore")

from flashtext import KeywordProcessor

params = yaml.safe_load(open(CONFIG_FILE_PATH))
pickle_input = PICKLE_FILE_PATH

# Load data artefacts
file = open(pickle_input, 'rb')
stem_flashtext_dict = pickle.load(file)
stemsDict = pickle.load(file)
context_flashtext_dict = pickle.load(file)
contextsDict = pickle.load(file)
stemToSkillDict = pickle.load(file)
skillToContextDict = pickle.load(file)
skillSetIndptContext = pickle.load(file)
ccs_flashtext_dict = pickle.load(file)
app_tool_flashtext_dict = pickle.load(file)
skill_to_id_mapping_dict = pickle.load(file)
skill_to_sfs_mapping_dict = pickle.load(file)
file.close()

# Load KeywordProcessors
context_keyword_processor = KeywordProcessor()
context_keyword_processor.add_keywords_from_dict(context_flashtext_dict)
stem_keyword_processor = KeywordProcessor()
stem_keyword_processor.add_keywords_from_dict(stem_flashtext_dict)
app_keyword_processor = KeywordProcessor()
app_keyword_processor.add_keywords_from_dict(app_tool_flashtext_dict)
ccs_keyword_processor = KeywordProcessor()
ccs_keyword_processor.add_keywords_from_dict(ccs_flashtext_dict)


def extract_skills(text):
    """
    output the extraction results of the skills extraction algorithm
    :param text: input text for skills extraction
    :return:
        output_list: list of skills with weight and type
    """
    context_list = extractionFrTxt(text, flashProcessor=context_keyword_processor,
                                   usedDict=contextsDict)
    stem_list = extractionFrTxt(text, flashProcessor=stem_keyword_processor,
                                usedDict=stemsDict)
    app_word_list = extractionFrTxt(text, flashProcessor=app_keyword_processor,
                                    usedDict="noDict")
    ccs_word_list = extractionFrTxt(text, flashProcessor=ccs_keyword_processor,
                                    usedDict="noDict")

    tsc_list = extractTSC(context_list=context_list, stem_list=stem_list,
                          skill_to_context_dict=skillToContextDict, stem_to_skill_dict=stemToSkillDict,
                          skill_indpt_context_set=skillSetIndptContext)
    app_list = extractAPP(app_word_list)
    ccs_list = extractCCS(ccs_word_list)

    tsc_output = getSkillWeight(skillExtractionList=tsc_list, id_mapping_dict=skill_to_id_mapping_dict, sfs_mapping_dict=skill_to_sfs_mapping_dict, skillType="TSC")
    app_output = getSkillWeight(skillExtractionList=app_list, id_mapping_dict=skill_to_id_mapping_dict, sfs_mapping_dict=skill_to_sfs_mapping_dict, skillType="App/Tools")
    ccs_output = getSkillWeight(skillExtractionList=ccs_list, id_mapping_dict=skill_to_id_mapping_dict, sfs_mapping_dict=skill_to_sfs_mapping_dict, skillType="CCS")

    output_list = tsc_output + ccs_output + app_output

    results = {}
    _list = []
    keys = range(len(output_list))

    for tuple in output_list:
        results[tuple[0]] = {
            "skill_title": tuple[1],
            "skill_type": tuple[3],
            "skill_source": "sfw", # Default to "sfw" for SEA v1
            "proficiency_lvl": "Not Applicable",
            "confidence_score": 1.0, # Default value of 1.0 for rule-based version
            "skill_occurrence": tuple[2], # Change to reflect absolute skills count
            "skill_tags": tuple[4], # Change to skill_tag as a list
        }

    if len(results) == 0:
        output = {}
    else:
        output = {
            "extractions": results
        }

    return output

def batch_extract_skills(df, text_cols_list, id_col=None):
    """
    This is a batch processing function for the SEA
    :df: The dataframe which contains the target text for skills extraction
    :text_cols_list: Expect a list of column names that contain the text information to be parsed through SEA
    :id_col: Optional arg, if no column is provided, the function will take the first text column in the 'text_col_list' and use it as a key for the output json
    :return:
        output_df: Dataframe of extracted skills and corresponding skill types, with one skill per row. Input text with multiple skills extracted will have multiple rows of records
    """
    df['input_text'] = df[text_cols_list].apply(lambda row: ' | '.join(row.values.astype(str)), axis=1)
    
    if id_col is None:
        df['text_id'] = df[text_cols_list[0]]
    else:
        df['text_id'] = df[id_col]
    
    text_id_ls = []
    input_text_ls = []
    skill_id_ls = []
    skill_title_ls = []
    skill_type_ls = []
    skill_source_ls = []
    skill_proficiency_lvl_ls = []
    confidence_score_ls = []
    skill_occurrence_ls = []
    skill_tags_ls = []
    for j in tqdm(range(df.shape[0])):
        text = df.input_text[j]
        _id = df.text_id[j]
        skill_json = extract_skills(text=text)
        if len(skill_json) > 0:
            for key, val in skill_json['extractions'].items():
                skill_id = key
                skill_title = val['skill_title']
                skill_type = val['skill_type']
                skill_source = val['skill_source']
                skill_proficiency_lvl = val['proficiency_lvl']
                skill_confidence_score = val['confidence_score']
                skill_occurrence = val['skill_occurrence']
                skill_tags = val['skill_tags']
                text_id_ls.append(_id)
                input_text_ls.append(text)
                skill_id_ls.append(skill_id)
                skill_title_ls.append(skill_title)
                skill_type_ls.append(skill_type)
                skill_source_ls.append(skill_source)
                skill_proficiency_lvl_ls.append(skill_proficiency_lvl)
                confidence_score_ls.append(skill_confidence_score)
                skill_occurrence_ls.append(skill_occurrence)
                skill_tags_ls.append(skill_tags)
        else:
            text_id_ls.append(_id)
            input_text_ls.append(text)
            skill_id_ls.append("no skill extracted")
            skill_title_ls.append("no skill extracted")
            skill_type_ls.append("no skill extracted")
            skill_source_ls.append("no skill extracted")
            skill_proficiency_lvl_ls.append("no skill extracted")
            confidence_score_ls.append("no skill extracted")
            skill_occurrence_ls.append("no skill extracted")
            skill_tags_ls.append("no skill extracted")
    
    output_df = pd.DataFrame(None)
    output_df['text_id'] = text_id_ls
    output_df['skill_id'] = skill_id_ls
    output_df['input_text'] = input_text_ls
    output_df['skill_title'] = skill_title_ls
    output_df['skill_type'] = skill_type_ls
    output_df['skill_source'] = skill_source_ls
    output_df['skill_prof_lvl'] = skill_proficiency_lvl_ls
    output_df['confidence_score'] = confidence_score_ls
    output_df['skill_occurrence'] = skill_occurrence_ls
    output_df['skill_tags'] = skill_tags_ls

    return output_df

    # # JSON output format for skills grouped by skill types
    # output = {}
    # for _id, text in zip(df.text_id, df.input_text):
    #     skill_json = extract_skills(text=text)
    #     temp_dict = {'TSC': [], 'CCS': [], 'Apps/Tools': []}
    #     if len(skill_json)>0:
    #         for key, val in skill_json['extractions'].items():
    #             temp_dict[val['skill_type']].append(val['skill_title'])
    #         text_id = _id
    #         if text_id not in output:
    #             output[text_id] = {}
    #             output[text_id] = temp_dict
    #         else:
    #             output[text_id] = temp_dict
    #     else:
    #         text_id = _id
    #         output[text_id] = temp_dict
            
    # return output
