from main import GerenciadorPrincipal
import mysql.connector
import google.generativeai as genai

API_KEY = "AIzaSyDAhEn0-2evZ2JiL9j2saNhvDnwwuOq1CA"
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
genai.configure(api_key=API_KEY)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="caue2005",
    database="assistente",
    auth_plugin='mysql_native_password'

)
mycursor = mydb.cursor()

query = "SELECT * FROM medidas where id = 1"
mycursor.execute(query)
first_row = mycursor.fetchone()