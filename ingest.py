import os

from llama_index import download_loader

# Use the GithubRepositoryReader to load documents from a Github repository
download_loader("GithubRepositoryReader")

from llama_index.readers.llamahub_modules.github_repo import (
    GithubRepositoryReader,
    GithubClient,
)

github_client = GithubClient(os.getenv("GITHUB_TOKEN"))

# Create a loader
loader = GithubRepositoryReader(
    github_client,
    owner="soderalohastrom",
    repo="ki-small",
    # filter_directories=(
    #     ["llama_index", "docs"],
    #     GithubRepositoryReader.FilterType.INCLUDE,
    # ),
    # filter_file_extensions=([".py"], GithubRepositoryReader.FilterType.INCLUDE),
    verbose=True,
    concurrent_requests=10,
)

# 1. Load documents
docs = loader.load_data(branch="main")

# 2. Parse the docs into nodes
from llama_index.node_parser import SimpleNodeParser
parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents(docs)

# 3. Build an index
from llama_index import GPTVectorStoreIndex
index = GPTVectorStoreIndex(nodes)

# 4. Store the index
index.storage_context.persist(persist_dir="index")
