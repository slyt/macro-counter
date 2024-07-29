# Python script to test out Langchain via the quickstart tutorial: https://python.langchain.com/v0.1/docs/get_started/quickstart/

from dotenv import load_dotenv
load_dotenv()

# LLM
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# RAG
from langchain_community.document_loaders import WebBaseLoader              # Scrape web
from langchain_openai import OpenAIEmbeddings                               # Create embeddings
from langchain_community.vectorstores import FAISS                          # Store in vector DB
from langchain_text_splitters import RecursiveCharacterTextSplitter         # Split text into docs
from langchain.chains.combine_documents import create_stuff_documents_chain # Send docs to LLM
from langchain.chains import create_retrieval_chain # Let the retriever find the relevant docs from the vector DB

# Chat history
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatOpenAI()
embeddings = OpenAIEmbeddings()

# Simple
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
print(chain.invoke({"input":"how can langsmith help with testing?"}))

# RAG
loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
                                          
<context>
{context}
</context>

Question: {input}""")

# take incoming questions, look up relevant docs, and pass those docs and 
# the question to the LLM and ask it to anser the origin question.
document_chain = create_stuff_documents_chain(llm, prompt)
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({"input": "How can I use Langsmith for testing?"})
print(response)
print("\n\n#####\n\n")
print(response["answer"])

# Chat history
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
chat_history = [
    HumanMessage(content="Can LangSmith help test my LLM applications?"), 
    AIMessage(content="Yes!")
    ]
response = retriever_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})



print("\n\n### CHAT HISTORY ###\n\n")
print(response)
print("\n\n#####\n\n")
print(response[1]["answer"])