from .app import db

user_pwd = db["Webmaster"]
print(str((user_pwd).find_one({"username": "admin1"})))