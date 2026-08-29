from langchain_community.document_loaders import UnstructuredMarkdownLoader

# Initialize the loader
file_path = "app/uploads/Global_Employee_Policy_Manual.md"
loader = UnstructuredMarkdownLoader(file_path, mode="single")

# Load data into a list of Document objects
docs = loader.load()

# Access the text
print(docs[0].page_content)
