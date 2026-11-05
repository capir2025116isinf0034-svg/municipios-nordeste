# Importando o Flask e as ferramentas que vamos utilizar
from flask import Flask, request, jsonify

# Criando nossa aplicação
app = Flask(__name__)

# Dicionário inicial com os dados dos municípios
municipios_nordeste_dataset = {
    "metadados": {
        "regiao": "Nordeste",
        "pais": "Brasil",
        "total_municipios": 30,
        "fonte_dados_populacao": "IBGE"
    },

    "municipios": {
        "Fortaleza": {
            "id_ibge": 2304400,
            "estado": "Ceará",
            "sigla_uf": "CE",
            "capital": True,
            "populacao_estimada": 2582360
        },

        "Salvador": {
            "id_ibge": 2927408,
            "estado": "Bahia",
            "sigla_uf": "BA",
            "capital": True,
            "populacao_estimada": 2559945
        }
    }
}
# Rota para listar todos os municípios ou filtrar por estado
@app.route('/municipios', methods=['GET'])
def listar_municipios():

    # Pegando o estado informado na URL
    uf = request.args.get('uf')

    # Pegando o dicionário que contém os municípios
    municipios = municipios_nordeste_dataset["municipios"]

    # Se o usuário informou uma UF, fazemos o filtro
    if uf:

        # Criando um novo dicionário vazio
        filtrados = {}

        # Percorrendo todos os municípios
        for nome, dados in municipios.items():

            # Verificando se a sigla do estado é igual à informada
            if dados["sigla_uf"] == uf.upper():

                # Adicionando o município ao resultado
                filtrados[nome] = dados

        # Retornando somente os municípios encontrados
        return jsonify(filtrados)

    # Se não informou UF, retorna todos os municípios
    return jsonify(municipios)
# Rota para consultar um município pelo nome
@app.route('/municipios/<nome>', methods=['GET'])
def consultar_municipio(nome):

    # Procurando o município no dicionário
    municipio = municipios_nordeste_dataset["municipios"].get(nome)

    # Se o município não existir, retorna erro 404
    if municipio is None:
        return jsonify({"erro": "Município não encontrado"}), 404

    # Se existir, retorna os dados do município
    return jsonify(municipio)
  # Rota para cadastrar um novo município
@app.route('/municipios', methods=['POST'])
def cadastrar_municipio():

    # Recebendo os dados enviados em JSON
    dados = request.get_json()

    # Pegando o nome do município
    nome = dados.get("nome")

    # Verificando se o nome foi informado
    if not nome:
        return jsonify({"erro": "O nome é obrigatório"}), 400

    # Pegando o dicionário de municípios
    municipios = municipios_nordeste_dataset["municipios"]

    # Verificando se o município já está cadastrado
    if nome in municipios:
        return jsonify({"erro": "Município já cadastrado"}), 409

    # Removendo o nome dos dados para guardar apenas as informações
    dados.pop("nome")

    # Cadastrando o município no dicionário
    municipios[nome] = dados

    # Retornando uma mensagem de sucesso
    return jsonify({
        "mensagem": "Município cadastrado com sucesso",
        "municipio": municipios[nome]
    }), 201
# Rota para atualizar um município
@app.route('/municipios/<nome>', methods=['PATCH'])
def atualizar_municipio(nome):

    # Recebendo os dados enviados
    dados = request.get_json()

    # Procurando o município
    municipios = municipios_nordeste_dataset["municipios"]

    # Verificando se ele existe
    if nome not in municipios:
        return jsonify({"erro": "Município não encontrado"}), 404

    # Atualizando somente as informações recebidas
    municipios[nome].update(dados)

    # Retornando os dados atualizados
    return jsonify({
        "mensagem": "Município atualizado com sucesso",
        "municipio": municipios[nome]
    })
  # Rota para excluir um município
@app.route('/municipios/<nome>', methods=['DELETE'])
def excluir_municipio(nome):

    # Pegando o dicionário de municípios
    municipios = municipios_nordeste_dataset["municipios"]

    # Verificando se o município existe
    if nome not in municipios:
        return jsonify({"erro": "Município não encontrado"}), 404

    # Removendo o município do dicionário
    del municipios[nome]

    # Retornando uma mensagem de sucesso
    return jsonify({
        "mensagem": "Município excluído com sucesso"
    })
  # Executando a aplicação
if __name__ == '__main__':
    app.run(debug=True)
