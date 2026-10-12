from pymongo import MongoClient
uri = "mongodb+srv://Projeto1995:<db_password>@cluster0.cnj4eyx.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)
