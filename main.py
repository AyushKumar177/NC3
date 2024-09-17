from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.schema import Document
import json
import os


def load_json_data(file_path):
    documents = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            text = f"title: {data['title']}\nabstract: {data['abstract']}"
            doc = Document(page_content=text)
            documents.append(doc)
    return documents

def vector_database(data_location, file_location):
    documents = load_json_data(data_location)
    embeddings = HuggingFaceInstructEmbeddings()
    vectordb = FAISS.from_documents(documents, embedding=embeddings)
    vectordb.save_local(file_location)
    return embeddings

def get_llm():
    GOOGLE_API_KEY = '___PUT YOUR API KEY___'  
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.1)
    return llm

def get_prompt():
    prompt_template = """
    Given the following context and a question, generate an answer based on the context only.
    In the answer try to provide as much text as possible from the "response" section in the source document.


    CONTEXT: {context}

    QUESTION: {question}
    """
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    return prompt

def get_chain(file_location):
    llm = get_llm()
    embeddings = HuggingFaceInstructEmbeddings()
    vectordb = FAISS.load_local(file_location, embeddings, allow_dangerous_deserialization=True)
    retriever = vectordb.as_retriever()
    prompt = get_prompt()
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="question",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    
    return chain

if __name__ == "__main__":
    data_location = 'data/filtered.json'
    file_location = 'vectorDB'
    vector_database(data_location, file_location)
    chain = get_chain(file_location)


file_location="vectorDB/"
chain = get_chain(file_location)

def info(query):
    try:
        query=query+"Give all information about it"
        response = chain({"question": query})
        return response['result']
    except Exception as e:
        print("Error:", e)

def summary(query):
    query=query+"Summarise it in 50 words"
    try:
        response = chain({"question": query})
        return response['result']
    except Exception as e:
        print("Error:", e)

def explaination(query):
    query=query+"Explain it in detail"
    try:
        response = chain({"question": query})
        return response['result']
    except Exception as e:
        print("Error:", e)




