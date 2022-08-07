import pymongo



def get_database():
    connection_string = "mongodb+srv://donut:DBPassword5017@cluster0.wj65o.mongodb.net/?retryWrites=true&w=majority"
    cluster = pymongo.MongoClient(connection_string)
    db = cluster["mock_remote_data"]
    collection = db['content']
    # collection.insert_one({"user_name": "Soumi",'test':'test'})
    return collection
    # print(list)


def insert_database(data):
    collection = get_database()
    collection.insert_one(data)


# if __name__ == '__main__':
#     get_database()
