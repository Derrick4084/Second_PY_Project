# %%
import spacy  # nlp(natural language processor)
import pdfminer  # for pdf2txt
import re  # regex
import os  # file manipulation
import pandas as pd  # csv - tabular

# %%
import pdf2txt  # pdf2txt file downloaded from github

# %%
def convert_pdf_to_text(filename):
    output_filename = os.path.basename(os.path.splitext(filename)[0]) + ".txt"
    output_filepath = os.path.join("Output/txt/", output_filename)
    pdf2txt.main(args=[filename, "--outfile", output_filepath])  # converts pdf to txt
    print(output_filepath + " saved successfully!!!")
    return open(output_filepath).read()


# %%
nlp = spacy.load("en_core_web_sm")

# %%
result_dict = {"name": [], "phone": [], "email": [], "skills": []}
names = []
phones = []
emails = []
skills = []

# %%
def parse_content(text):
    skillset = re.compile("python|java|sql|hadoop|tableau")
    phone_num = re.compile(
        "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    )
    doc = nlp(text)
    name = [entity.text for entity in doc.ents if entity.label_ == "PERSON"][0]
    print(name)
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset, text.lower())
    unique_skills_list = str(set(skills_list))
    names.append(name)
    skills.append(unique_skills_list)
    phones.append(phone)
    emails.append(email)
    print("Extraction completed successfully!!!")


# %%
for file in os.listdir("Resumes/"):
    if file.endswith(".pdf"):
        print("Reading....." + file)
        txt = convert_pdf_to_text(os.path.join("Resumes/", file))
        parse_content(txt)

# %%
result_dict["email"] = emails
result_dict["name"] = names
result_dict["phone"] = phones
result_dict["skills"] = skills

# %%
result_df = pd.DataFrame(result_dict)
# result_df

# %%
result_df.to_csv("Output/csv/parsed_resumes.csv")
