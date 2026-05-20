from load_pdf import pdfloader
from chunkers import chunk_pages
from embedder import embed_model
from vectordb import pinecone_upsert

pdf_path = 'C:/Users/snave/OneDrive/Desktop/my python/Gen AI/RAG/resources/HRPolicy.pdf'


def run():

    pages = pdfloader(pdf_path)

    chunks = chunk_pages(pages, chunk_size=900, chunk_overlap=150)

    embeddings = embed_model(chunks)

    pinecone_upsert(chunks, embeddings, namespace=" ")


if __name__ == "__main__":
    run()
