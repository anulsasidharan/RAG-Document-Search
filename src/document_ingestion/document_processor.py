"""Document processing module for loading and splitting documents"""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


from typing import List, Union
from pathlib import Path
from langchain_community.document_loaders import (
    WebBaseLoader,
    PyPDFLoader,
    TextLoader,
    PyPDFDirectoryLoader
)

class DocumentProcessor:
    """Handles document loading and processing"""
    
    def __init__(self, chunk_size: int=500, chunk_overlap:int=50):
        """
        Initilize document processor

        Args:
            chunk_size: Size of the text chunks. Defaults to 500.
            chunk_overlap: Overlap between chunks. Defaults to 50.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
    def load_from_url(self, url:str) -> List[Document]:
        """Load Documents form URL"""
        loader = WebBaseLoader(url)
        return loader.load()
    
    def load_from_pdf_dir(self, directory:Union[str, Path]) -> List[Document]:
        """Load documents form all PDFs inside a directory"""
        loader = PyPDFDirectoryLoader(str(directory))
        return loader.load()
    
    def load_from_text(self, file_path:Union[str,Path]) -> List[Document]:
        """Load documents form TXT file"""
        loader = TextLoader(str(file_path), encoding="utf-8")
        return loader.load()
    
    def load_from_pdf(self, file_path:Union[str, Path]) -> List[Document]:
        """Load documents from PDF file"""
        loader = PyPDFDirectoryLoader(str("data"))
        return loader.load()
    
    def load_documents(self, sources: list[str])->List[Document]:
        """
        Load documents from URLs, PDF directories, or TXT files.

        Args:
            source : List of URL's, PDF directories, or TXT files

        Returns:
            List of loaded documents
        """
        docs: List[Document] = []
        for src in sources:
            if src.startswith("http://") or src.startswith("https://"):
                docs.extend(self.load_from_url(src))
                
            path= Path("data")
            if path.is_dir(): # PDF directory
                docs.extend(self.load_from_pdf_dir(path))
            elif path.suffix.lower() == ".txt":
                docs.extend(self.load_from_text(path))
            else:
                raise ValueError(
                    f"Unsupported source type: {src}."
                    "Use URL, .txt file or PDF directory"
                )
        return docs
    
    def split_documents(self, documents: List[Document])->List[Document]:
        """
        Split documents into chunks

        Args:
            documents :List of documents

        Returns:
            List of split documents
        """
        return self.splitter.split_documents(documents)
    
    def process_urls(self, urls:List[str]) -> List[Document]:
        """
        Complete pipeline to load and split documents

        Args:
            urls : List of urls to process

        Returns:
            List of processed document chunks
        """
        docs = self.load_documents(urls)
        return self.split_documents(docs)