from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings


class DocumentAssistant:
    def __init__(self, persist_dir="db_docs", model="mistral"):
        self.model = model
        self.embeddings = OllamaEmbeddings(model=model)
        self.persist_dir = persist_dir
        self.db = None

    def load_pdf(self, filepath):
        loader = PyPDFLoader(filepath)
        docs = loader.load()

        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        self.db = Chroma.from_documents(
            chunks,
            self.embeddings,
            persist_directory=self.persist_dir
        )

    def query(self, question, k=3):
        if not self.db:
            return "Nenhum documento carregado ainda."
        docs = self.db.similarity_search(question, k=k)
        return "\n".join([d.page_content for d in docs])
