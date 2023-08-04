from langchain.llms import HuggingFacePipeline, HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator


def sample_execute():
    question = """Question: Using cached dotenv-0.0.5.tar.gz (2.4 kB)
      Using cached dotenv-0.0.5.tar.gz (2.4 kB)
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error"""
    template = """Question: Give extensive advice and severity rating for this log: {question}.
    
    Answer: Severity followed by advice is: """

    prompt = PromptTemplate(template=template, input_variables=["question"])

    repo_id = "google/flan-t5-xxl"
    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 128}
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    print(llm_chain.run(question))


def blog_post_sample_exec():
    repo_id = "google/flan-t5-xxl"
    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 128}
    )

    loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
    index1 = VectorstoreIndexCreator()
    # index = index1.from_loaders([loader])
    # print(index.query("What is Task Decomposition?", llm))
