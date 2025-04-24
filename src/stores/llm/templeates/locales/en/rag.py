
from string import Template
# RagPrompts

system_prompt = Template("\n".join(["you are an assistant for the user",
                                    "you will provided by a set of documents associated with the user's query "]
                                   )
                         )
document_prompt = Template("\n".join([

    "## Document No:$doc_num",
    "### content:$chunk_text"
]))


footer_prompt = Template("\n".join([

    "Based on the above documents generate answer for the user",
    "## Answer:"
]))
