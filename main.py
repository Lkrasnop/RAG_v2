import os
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pdf_to_text import pdf_to_txt
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

current_dir = os.getcwd()
files_path = os.path.join(current_dir, "text")
input_path = os.path.join(current_dir, "pdf")
file_path = os.path.join(current_dir, "text", "test.txt")
persist_dir = os.path.join(current_dir, "db", "chroma_db_meta")

texts_dir = os.path.join(current_dir, "text")
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db_with_metadata")

input_folder = input_path
output_folder = files_path

def initialize_chroma_db():
    if not os.path.exists(persistent_directory):
        print("Persistent directory does not exist. Initializing vector store...")

        if not os.path.exists(files_path):
            raise FileNotFoundError(
                f"The directory {files_path} does not exist. Please check the path."
            )

        book_files = [f for f in os.listdir(files_path) if f.endswith(".txt")]

        documents = []
        for book_file in book_files:
            file_path = os.path.join(files_path, book_file)
            loader = TextLoader(file_path)
            book_docs = loader.load()
            for doc in book_docs:
                doc.metadata = {"source": book_file}
                documents.append(doc)

        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=10)
        docs = text_splitter.split_documents(documents)

        print("\n--- Document Chunks Information ---")
        print(f"Number of document chunks: {len(docs)}")

        print("\n--- Creating embeddings ---")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        print("\n--- Finished creating embeddings ---")

        print("\n--- Creating and persisting vector store ---")
        db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
        print("\n--- Finished creating and persisting vector store ---")
    else:
        print("Vector store already exists. No need to initialize.")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
    
    return db

def process_query(query):
    db = initialize_chroma_db()
    
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.5},
    )
    relevant_docs = retriever.invoke(query)

    relevant_content = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    combined_input = f"""Here are some documents that might help answer the question: {query}

Relevant Documents:
{relevant_content}

Please provide an answer based only on the provided documents. If the answer is not found in the documents, respond with "I'm not sure"."""

    model = ChatOpenAI(model="gpt-4o")
    messages = [
        SystemMessage(content="You are a helpful assistant and professional in ml engineer with 10 years of experience."),
        HumanMessage(content=combined_input),
    ]

    result = model.invoke(messages)
    return result.content

def main():
    pdf_to_txt(input_folder, output_folder)
    
    if not os.path.exists(files_path):
        raise FileNotFoundError(f"file {files_path} does not exist, please check the path")
    
    loader = TextLoader(file_path)
    documents = loader.load()
    text_split = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    docs = text_split.split_documents(documents)

    db = initialize_chroma_db()
    
    query = "How will AI impact the future of insurance by 2030?"
    response = process_query(query)
    
    print("\n--- Generated Response ---")
    print("Content only:")
    print(response)

if __name__ == "__main__":
    main()