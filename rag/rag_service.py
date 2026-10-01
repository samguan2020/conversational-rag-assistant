import os

from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from common.lc_modules import getEmbeddings, saveDocToVectorStore

TEMP_FOLDER = "./temp"

if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

embeddings = getEmbeddings()


async def do_embedding(file: UploadFile, channel: str):
    file_path = os.path.join(TEMP_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    documents = []

    if file.filename.lower().endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
    elif file.filename.lower().endswith('.txt'):
        loader = TextLoader(file_path)
        documents = loader.load()

    if not len(documents):
        return {"message": "document is empty"}

    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)

    saveDocToVectorStore(docs, embeddings, channel)
    # vectorStore = getVectorStore(embeddings, channel)
    #
    # vectorStore.add_documents(docs)

    return {"message": "done."}
