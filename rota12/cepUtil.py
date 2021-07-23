import re, requests, json

"""Verifica se o CEP é Valido"""
def valida_cep(cep):
    return True if re.search(r'^(\d{5}-\d{3}|\d{8})$', cep) else False

"""Consulta CEP no site VIACEP"""
def consulta(cep):
    cep = cep.replace("-", "")

    url = f'https://viacep.com.br/ws/{cep}/json/'
    headers = {'User-Agent': 'Autociencia/1.0'}
    resposta = requests.request('GET', url, headers=headers)
    conteudo = resposta.content.decode('utf-8')
    resposta.close()
    endereco = json.loads(conteudo)

    return endereco