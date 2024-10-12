import chromadb
import ollama
import os

def getMarkdownFiles(directory=os.getenv("DIRECTORY")):
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as file:
                    relative_path = os.path.relpath(file_path, directory)
                    yield relative_path, file.read()

def initChroma(collectionName="docs"):
   
    client = chromadb.PersistentClient(path="/db/chroma.db")
    # create new collection or get existing
    collection = client.create_collection(name=collectionName, get_or_create=True)

    return collection

def storeEmbeddings(collection):

    highestId = collection.count()

    # store each document in a vector embedding database
    for filename, content in getMarkdownFiles():
        try:
            # create and get embeddings for each document
            response = ollama.embeddings(model="all-minilm", prompt=content)
            embedding = response["embedding"]

            # store the document embedding in the database
            collection.add(
                ids=[str(highestId)],
                embeddings=[embedding],
                documents=[content]
            )

            # increase the id
            highestId += 1

            print(f"Create embedding for document {filename}")

        except Exception as e:
            print(f"Error storing document {highestId}: {e}")


def createMarkdownEmbeddings(collectionName="docs"):

    collection = initChroma(collectionName)
    storeEmbeddings(collection)

    return collection