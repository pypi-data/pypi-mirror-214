import pandas as pd
from tqdm import tqdm
from ssg_sea.extract_skills import batch_extract_skills

dataframe = pd.DataFrame(None)
dataframe['title'] = ['physics','mathematics','macro-economics','geography']
dataframe['content'] = ['physics concept applications','statistical calculationa and data modelling','just theories','the world we live in']

def test_batch_extract_skills(df=dataframe, text_cols_list=['title','content']):
    skills_extraction = batch_extract_skills(dataframe, ['title','content'])

    assert isinstance(skills_extraction, pd.DataFrame)
    assert len(skills_extraction) == 4
    assert len(skills_extraction.columns) == 10