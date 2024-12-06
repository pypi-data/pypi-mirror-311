from collections import Counter
import re
import pandas as pd
import pyperclip as pc


def count_words(text):
    # Normalize text to lowercase and find all words
    words = re.findall(r'\w+', text.lower())
    # Count words using Counter, which is efficient for object counting
    word_count = Counter(words)
    return word_count
def count_words_sections(text):
    # This function takes a dictionary with section names as keys and text as values
    # It returns a dictionary with section names as keys and word count as values
    word_counts = {section: len(content.split()) for section, content in text.items()}
    return word_counts
def count_words_in_string(text):
    # Split by spaces to count words
    return len(text.split())

##########

def extract_sections(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    content = clean_tex(content)

    # Use non-greedy matching to avoid issues with nested sections
    sections = re.findall(r'\\section\{(.+?)\}(.*?)(?=\\section|\Z)', content, re.DOTALL)

    sections_dict = {}
    for title, body in sections:
        # Create a key by converting title to lowercase and replacing spaces with underscores
        key = title.lower().replace(' ', '_')
        sections_dict[key] = body.strip()
    df = pd.Series(sections_dict, index=sections_dict.keys())
    #display(df)
    return sections_dict, content

def clip_tex(tex_content):
    # Keep content between \section{introduction} and \section{conclusion}
    match = re.search(r'\\section{Introduction}(.*?)\\section{Conclusion}', tex_content, flags=re.DOTALL)
    if match:
        # Return only the text between introduction and conclusion
        return match.group(1)
    else:
        # Return the original content if sections are not found
        return tex_content



def clean_tex(tex_content):
    # Remove content in \begin{figure} ... \end{figure}
    tex_content = re.sub(r'\\begin{figure.*?\\end{figure', '', tex_content, flags=re.DOTALL)
    # Remove content in \begin{table} ... \end{table}
    tex_content = re.sub(r'\\begin{table.*?\\end{table', '', tex_content, flags=re.DOTALL)
    # Remove content in \begin{comment} ... \end{comment}
    tex_content = re.sub(r'\\begin{comment}.*?\\end{comment}', '', tex_content, flags=re.DOTALL)

    tex_content = re.sub(r'\\begin{tcolorbox}.*?\\end{tcolorbox}', '', tex_content, flags=re.DOTALL)

    # Remove lines starting with '%'
    #tex_content = '\n'.join([line for line in tex_content.split('\n') if not line.strip().startswith('%')])
    #tex_content = re.sub(r'^%.*$', '', tex_content, flags=re.MULTILINE)
    tex_content = re.sub(r'^\s*%.*$', '', tex_content, flags=re.MULTILINE)
    return tex_content


def reload_paper(file_path):
    global sections_dict, full_paper
    sections_dict, full_paper = extract_sections(file_path)

from mychatgpt import GPT
###
class Writers:
    def __init__(self,
                 gpt = GPT(),
                 tex_file = None,
                 context = None,
                 format = 'latex',
                 model = GPT().model):
        self.gpt = gpt
        self.model = model
        self.context = context
        self.tex_file = tex_file
        self.gpt.format = format
        if self.context:
            gpt.add_system(context)
        if tex_file:
            self.sections_dict, self.content = extract_sections(tex_file)
            display(pd.Series(self.sections_dict, index=self.sections_dict.keys()))

        self.table_template = table_template

    def reload_paper(self):
        self.sections_dict, full_paper = self.extract_sections(self.tex_file)



    def add_info_set(self, sections, clear = True):
        if clear: self.gpt.clear_chat()

        for section in sections:
            section_clean = clean_tex(self.sections_dict[section])
            self.gpt.expand_chat('\nThis is the '+section+' section of my new paper:\n'+section_clean, 'user')

    def enhancer(self, section = None,
                 instructions = None,
                 task = None):
        if not section:
            section = pc.paste()

        if not instructions:
            instructions= f"""The Paper I have written needs to be revised. It must use current and correct terminology of the “Infomatics Engineering” domain. Methods should be described accurately, consistently and precisely with the correct current computer science terminology. Make also the text more fluent."""

            """
            Understand the context: construction of a Dataset by joining different sources, for targeted retrieval based on queries built with MeSH terms (Nutrigenetics field).
            """

        if not task:
            task = f"""Apply this criteria to this section below (in english) more concise and clear:
            write better this section 
            
            """

        self.gpt.c(instructions+task+"["+section+"]", gpt=self.model)

    def table_maker(self,
                    template= None,
                    task= None,
                    data = None,
                    instructions = None
                    ):
        if not template:
            template = self.table_template
        if not instructions:
            instructions = ''
        if not task:
            task = """
Using this table provided as a template, make a table out of this data:

"""
        if not data:
            data = pc.paste()

        self.gpt.expand_chat(template)
        self.gpt.c(instructions+task+"\n\nData:"+data, gpt=self.model)


    def ask_paper(self,
                  sections: list = [],
                    template= None,
                    task= None,
                    data = None,
                    instructions = None,
                    clear = True
                    ):
        if not template:
            template = self.table_template
        if not instructions:
            instructions = ''
        if not task:
            task = ""
        if data:
            data = "\n\nData:"+data
        else:
            data = ''
        self.add_info_set(sections, clear=clear)
        if template: self.gpt.expand_chat(template)
        self.gpt.c(instructions+task+data, gpt=self.model)

#### TEMPLATES ###
table_template = r"""template table :
\begin{table*}[htbp]
    \centering
    \caption{Data Sources for Interaction Maps}
    \label{tab:data_sources}
    \small
    %\resizebox{\textwidth}{!}{ 
    \begin{tabular}{ll}
        \toprule
        
        \textbf{Category} & \textbf{Data Sources} \\
        \hline
        Protein-Protein Interaction (PPI) & Biogrid, STRING \\
        Transcription Factors (TF) & TF2DNA, TRRUST v2 \\
        MicroRNA & mirdb, miRBase, miRnet \\
        RNA Binding Proteins (RNAbp) & RBP2GO \\
        Biological Process, Molecular Function & Gene Ontology (GO) \\
        Metabolomics & KEGG, Reactome, CHEBI \\
        Drugs & DrugBank \\
        \bottomrule
    \end{tabular}
    %}
\end{table*}
"""