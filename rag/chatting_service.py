from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

from common.lc_modules import getVectorStore, getEmbeddings, getLlm, getMemory

llm = getLlm()
embeddings = getEmbeddings()


def do_chat(question: str, channel: str = 'default', sessionId: str = ''):
    # Given the following conversation and a follow up question, answer the question.
    condense_question_prompt = ChatPromptTemplate.from_template('''
        Chat History: {{chat_history}}

        Question: {question}
    ''')
    # Answer the question using only the retrieved context and the conversation
    # so far. If the answer isn't in the context, say so instead of guessing.
    combine_docs_custom_prompt = PromptTemplate.from_template('''
        You are a customer support assistant. Answer using only the context below.

        Context: {context}

        {question}

        Answer:
    ''')

    memory = getMemory(sessionId)
    retriever = getVectorStore(embeddings, channel).as_retriever(search_type="similarity", search_kwargs={
        "distance_threshold": 5})

    qa = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory,
                                               condense_question_prompt=condense_question_prompt,
                                               combine_docs_chain_kwargs=dict(prompt=combine_docs_custom_prompt),
                                               verbose=False)
    result = qa.run({"question": question})
    return result


if __name__ == "__main__":
    print(do_chat('What is in the knowledge base for this channel?'))
    print('=============================')
    print(do_chat('Can you summarize the last document I uploaded?'))
