def user_schema(user):
    return {"_id":str(user["_id"]),
            "username":user["username"],
            "contrasena":user["contrasena"]
            }
    
def users_schema(users):
    return [user_schema(user) for user in users]