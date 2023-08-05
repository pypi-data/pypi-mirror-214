from lollms.personality import APScript, AIPersonality
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter 
from langchain.embeddings.llamacpp import LlamaCppEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

class Processor(APScript):
    """
    A class that processes model inputs and outputs.

    Inherits from APScript.
    """

    def __init__(self, personality: AIPersonality, model = None) -> None:
        super().__init__()
        self.personality = personality
        self.model = model
        self.vector_store = None
    
    def build_db(self):
        self.pdf =  PdfReader(self.personality._processor_cfg["pdf_file_path"])
        text = ""
        for page in self.pdf.pages:
            text += page.extract_text()

        self.text_splitter = CharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=0,
            length_function=len
        )
        self.chunks = self.text_splitter.split_text(text)
        print("Vectorizing document")
        self.emb = LlamaCppEmbeddings(model_path="models/llama_cpp_official/Wizard-Vicuna-7B-Uncensored.ggmlv2.q4_0.bin", n_ctx=2048)
        
        self.vector_store = FAISS.from_texts(self.chunks, embedding=self.emb)
        print("Vectorization done successfully")

   

    def run_workflow(self, prompt, previous_discussion_text="", callback=None):
        """
        Runs the workflow for processing the model input and output.

        This method should be called to execute the processing workflow.

        Args:
            generate_fn (function): A function that generates model output based on the input prompt.
                The function should take a single argument (prompt) and return the generated text.
            prompt (str): The input prompt for the model.
            previous_discussion_text (str, optional): The text of the previous discussion. Default is an empty string.

        Returns:
            None
        """
        output =""
        if self.vector_store is None:
            self.build_db()

        docs = self.vector_store.similarity_search(prompt, k=3)
        chain = load_qa_chain(llm=self.personality.model, chain_type="stuff")
        response = chain.run(input_documents=docs, question=prompt)
        print(f"response: {response}")


        return output



