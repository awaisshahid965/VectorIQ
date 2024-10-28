from app.vector_stores.qdrant_vector_store import QdrantVectoreStore

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, status, HTTPException

from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

router = APIRouter()

qdrant_vector_store = QdrantVectoreStore(dataset_name="stealth")
model = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0,
)

retrieval_qa_chat_prompt = ChatPromptTemplate.from_messages([
  ("system", "Answer any user questions based solely on the context below. Format each of your responses in Markdown, and for each line break, use `<br>` at the end of the line. Ensure that all bullet points, sections, and paragraphs are properly separated with `<br>` for clearer formatting:\n<context>\n{context}\n</context>"),
  ("placeholder", "{chat_history}"),
  ("human", "{input}"),
])

combine_docs_chain = create_stuff_documents_chain(model, retrieval_qa_chat_prompt)

rag_chain = create_retrieval_chain(qdrant_vector_store.get_retriever(), combine_docs_chain)

def answer_stream(query: str):
    try:
        for chunk in rag_chain.stream({"input": query}):
            if answer_chunk := chunk.get("answer"):
                yield f"{answer_chunk}\n\n"
    except Exception as e:
        raise RuntimeError(f"Error while streaming: {str(e)}")

@router.get("/assistant")
def query_endpoint(query: str):

    if not query:
        raise HTTPException(status_code=400, detail="Query not provided")

    try:
        return StreamingResponse(
            content=answer_stream(query),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
            status_code=status.HTTP_200_OK,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
