from databaseConnect import getUser, connectDB

supabase = connectDB()
result = getUser(supabase, "xd")
print(len(result.data))