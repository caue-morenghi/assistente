from main import GerenciadorPrincipal
import mysql.connector
import google.generativeai as genai

gerenciador = GerenciadorPrincipal()

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

primeira_medida = {
    "panturrilha_esquerda": first_row[1],
    "panturrilha_direita": first_row[2],
    "perna_esquerda": first_row[3],
    "perna_direita": first_row[4],
    "abdomen": first_row[5],
    "costas": first_row[6],
    "peitoral": first_row[7],
    "ombros": first_row[8],
    "braco_esquerdo": first_row[9],
    "braco_direito": first_row[10],
    "antebraco_esquerdo": first_row[11],
    "antebraco_direito": first_row[12]
}

query = "SELECT * FROM medidas ORDER BY created_at DESC LIMIT 1"
mycursor.execute(query)
last_row = mycursor.fetchone()

ultima_medida = {
    "panturrilha_esquerda": last_row[1],
    "panturrilha_direita": last_row[2],
    "perna_esquerda": last_row[3],
    "perna_direita": last_row[4],
    "abdomen": last_row[5],
    "costas": last_row[6],
    "peitoral": last_row[7],
    "ombros": last_row[8],
    "braco_esquerdo": last_row[9],
    "braco_direito": last_row[10],
    "antebraco_esquerdo": last_row[11],
    "antebraco_direito": last_row[12]
}

medidas_atuais = {
    "panturrilha_esquerda": 31,
    "panturrilha_direita": 31,
    "perna_esquerda": 30,
    "perna_direita": 30,
    "abdomen": 32,
    "costas": 50,
    "peitoral": 35,
    "ombros": 31,
    "braco_esquerdo": 25,
    "braco_direito": 27,
    "antebraco_esquerdo": 32,
    "antebraco_direito": 32
}

metas = {
    "panturrilha_esquerda": 40,
    "panturrilha_direita": 40,
    "perna_esquerda": 45,
    "perna_direita": 45,
    "abdomen": 40,
    "costas": 50,
    "peitoral": 60,
    "ombros": 40,
    "braco_esquerdo": 35,
    "braco_direito": 35,
    "antebraco_esquerdo": 32,
    "antebraco_direito": 32
}

def calcular_crescimento_mensal(primeira_medida, metas, meses):
    crescimento_mensal = {}
    for (key1, value1), (key2, value2) in zip(primeira_medida.items(), metas.items()):
        if key1 == key2:
            crescimento_mensal[key1] = round((value2 - value1) / meses, 2)
        else:
            print(f"Chaves não correspondem: {key1} != {key2}")
    return crescimento_mensal

def comparar_medidas(ultima_medida, medidas_atuais):
    comparacao = {}
    for (key1, value1), (key2, value2) in zip(ultima_medida.items(), medidas_atuais.items()):
        if key1 == key2:
            comparacao[key1] = round(value2 - value1, 2)
        else:
            print(f"Chaves não correspondem: {key1} != {key2}")
    return comparacao

def formatar_resultados(crescimento_mensal, comparacao_medidas):
    resultados = []
    for key in crescimento_mensal.keys():
        resultados.append(f"{key.replace('_', ' ')}: deveria crescer {crescimento_mensal[key]}, cresceu {comparacao_medidas[key]}")
    return "\n".join(resultados)

meses = 6
crescimento_mensal = calcular_crescimento_mensal(ultima_medida, metas, meses)
comparacao_medidas = comparar_medidas(ultima_medida, medidas_atuais)

resultados_formatados = formatar_resultados(crescimento_mensal, comparacao_medidas)

print(resultados_formatados)

prompt = f"Gemini, você fará uma análise do crescimento de medidas de um corpo. Para isso, você irá comparar as medidas antigas de uma área com as novas, ou seja, a antiga medida do peitoral deve ser comparada com a nova medida do peitoral, e assim por diante. Faça um breve resumo, dos pontos a melhorar (deve-se melhorar quando uma área não atingiu a meta ou há desproporção entre um lado e outro da mesma área), dos pontos que cresceram mais do que deveriam (quando se obteve um resultado mais de 0,5cm da meta) aja como um profissional, mas não dê detalhes, seja direto ao ponto. Siga a seguinte formatação: 'Perna direita e esquerda não cresceram como deveria, deve-se focar mais nesses músculos. Há desproporção entre o braço esquerdo e direito, deve-se focar mais no braço direito com exercícios unilaterais, abdomen cresceu mais do que deveria, deve-se dar uma pausa nessa área, braços direito e esquerdo estão de acordo com a meta (está de acordo com a meta quando a medida está mais ou menos 0,5cm da meta, exemplo: se a meta é 2cm, e o braço esquerdo cresceu 3cm, portanto está acima da meta, no entanto, se cresceu 1,5cm ou 2,5cm, está dentro da meta e está certo, deve-se continuar treinando normalmente essa área)'. Não escreva mais do que isso. ANALISE:\n\n{resultados_formatados}"

# response = model.generate_content(prompt)

# print(response.candidates[0].content.parts[0].text)
