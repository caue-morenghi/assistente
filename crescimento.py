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
    "peitoral": first_row[6],
    "braco_esquerdo": first_row[7],
    "braco_direito": first_row[8],
    "antebraco_esquerdo": first_row[9],
    "antebraco_direito": first_row[10]
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
    "peitoral": last_row[6],
    "braco_esquerdo": last_row[7],
    "braco_direito": last_row[8],
    "antebraco_esquerdo": last_row[9],
    "antebraco_direito": last_row[10]
}

medidas_atuais = {
    "panturrilha_esquerda": 31,
    "panturrilha_direita": 31,
    "perna_esquerda": 49,
    "perna_direita": 51.5,
    "abdomen": 78.5,
    "peitoral": 113.5,
    "braco_esquerdo": 30.79,
    "braco_direito": 30.79,
    "antebraco_esquerdo": 24,
    "antebraco_direito": 25
}

metas = {
    "panturrilha_esquerda": 36.3,
    "panturrilha_direita": 36.3,
    "perna_esquerda": 54.6,
    "perna_direita": 54.6,
    "abdomen": 78.5,
    "peitoral": 130.1,
    "braco_esquerdo": 36.3,
    "braco_direito": 36.3,
    "antebraco_esquerdo": 30.3,
    "antebraco_direito": 30.3
}

def calcular_crescimento_mensal(primeira_medida, metas, meses):
    crescimento_mensal = {}
    for (key1, value1), (key2, value2) in zip(primeira_medida.items(), metas.items()):
        if key1 == key2:
            crescimento_mensal[key1] = round((float(value2) - float(value1)) / meses, 2)
        else:
            print(f"Chaves não correspondem: {key1} != {key2}")
    return crescimento_mensal

def comparar_medidas(ultima_medida, medidas_atuais):
    comparacao = {}
    for (key1, value1), (key2, value2) in zip(ultima_medida.items(), medidas_atuais.items()):
        if key1 == key2:
            comparacao[key1] = round(float(value2) - float(value1), 2)
        else:
            print(f"Chaves não correspondem: {key1} != {key2}")
    return comparacao

def formatar_resultados(crescimento_mensal, comparacao_medidas, ultima_medida, medidas_atuais):
    resultados = []
    for key in crescimento_mensal.keys():
        crescimento_esperado = crescimento_mensal[key]
        crescimento_real = comparacao_medidas[key]
        ultima = ultima_medida[key]
        atual = medidas_atuais[key]
        if crescimento_esperado != 0:
            percentual_atingido = (crescimento_real / crescimento_esperado) * 100
        else:
            percentual_atingido = 0
        resultados.append(f"{key.replace('_', ' ').capitalize()}: última medida foi {ultima} e a nova medida é {atual}. Deveria crescer {crescimento_esperado}, cresceu {crescimento_real}. Meta mensal atingida em {percentual_atingido:.2f}%")
    return "\n".join(resultados)

meses = 8
crescimento_mensal = calcular_crescimento_mensal(ultima_medida, metas, meses)
comparacao_medidas = comparar_medidas(ultima_medida, medidas_atuais)

resultados_formatados = formatar_resultados(crescimento_mensal, comparacao_medidas, ultima_medida, medidas_atuais)

formatacao = "Panturrilha esquerda: cresceu como deveria.\nPanturrilha direita: cresceu menos do que devia\nAnálise das panturrilhas: deve-se treinar mais a panturrilha direita (desproporção)\n\nPerna esquerda: cresceu como deveria\nPerna direita: cresceu como deveria\nAnálise das pernas: deve-se manter o cronograma (resultados esperados obtidos).\n\nAbdomen: deve-se manter o cronograma (resultados esperados obtidos)\n\nPeitoral: cresceu mais do que deveria.\nAnálise do peitoral: deve-se fazer uma pausa (resultados esperados ultrapassados)\n\nBraço esquerdo: não cresceu como deveria\nBraço direito: não cresceu como deveria\nAnálise dos braços: deve-se refatorar o treinamento (resultados esperados não obtidos)\n\nAntebraco esquerdo: cresceu como deveria\nAntebraco direito: cresceu como deveria\nAnálise dos antebraços: deve-se manter o cronograma (resultados esperados obtidos)"

prompt = f"Gemini, você fará uma análise do crescimento de medidas de um corpo. Para isso, você irá comparar as medidas antigas de uma área com as novas, ou seja, a antiga medida do peitoral deve ser comparada com a nova medida do peitoral, a antiga medida do braço esquerdo deve ser comparada à nova medida do braço esquerdo, e assim por diante. Faça um breve resumo, dos pontos a melhorar, dos pontos que cresceram mais do que deveriam, e dos pontos a manter. Aja como um profissional, mas não dê detalhes, seja direto ao ponto. Siga a seguinte formatação: '{formatacao}'. Para ser um 'resultado esperado obtido', a meta mensal atingida deve ser próxima de 100%, com um erro máximo de 10%, exemplo: 90% e 110% são resultados esperados obtidos. No entanto, 85% ou 120% já não são resultados esperados obtidos, são abaixo e acima do esperao, respectivamente. Leve em conta, principalmente, a porcentagem de meta mensal atingida. Se há uma diferença de mais de 0.5cm entre membros esquerdos e direitos, a análise deve adicionar: 'deve-se treinar mais a panturrilha/perna/etc esquerda/direita (desproporção)', além da análise já existente. Não escreva mais do que pede a formatação. ANALISE:\n\n{resultados_formatados}"

response = model.generate_content(prompt)

print(response.candidates[0].content.parts[0].text)