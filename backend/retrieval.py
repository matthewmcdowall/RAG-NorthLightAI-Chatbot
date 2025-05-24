from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph

# Import your vector store and LLM here
# from backend.llm import llm  # You should define and initialize it in another file or here
# from backend.vectorstore import vector_store  # Supabase vector store or FAISS, etc.

# Define your prompt template
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use five sentences maximum and keep the answer as concise as possible.
Always start the answer with a sentence like "Thanks for asking question about North Light AI!"; but be innovative and each time use a similar welcoming message.

{context}

Question: {question}

Helpful Answer:"""
prompt = PromptTemplate.from_template(template)

# Define your RAG state type
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

# Define retrieval node
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

# Define generation node
def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

# Build the graph
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

# Wrapper to use in app.py
def get_answer(query: str) -> str:
    state = graph.invoke({"question": query})
    return state["answer"]
