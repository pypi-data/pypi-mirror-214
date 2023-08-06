from ssg_sea.extract_skills import extract_skills

test_text = "You will learn how to use python for data analytics and sql to query relational databases, " \
            "appliants who are familiar with other programming languages (R, Perl, Java) will be able to " \
            "easily transfer their prior knowledge while learning python for data analytics in this course. " \
            "Additional tips on data visualisation and data story-telling will also be taught. "


def test_extract_skills(text=test_text):
    skills_extraction = extract_skills(test_text)

    assert isinstance(skills_extraction, dict)
    assert len(skills_extraction) == 1