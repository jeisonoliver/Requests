import requests
import logging
from bs4 import BeautifulSoup

def consulta_processo(tipo_pesquisa, termo_pesquisa):
    """Realiza uma consulta de processo judicial no site."""

    # Configura o logging
    logging.basicConfig(level=logging.INFO)

    # Verifica se o termo de pesquisa é válido
    if tipo_pesquisa == "processo" and not termo_pesquisa.strip():
        logging.error("Número de processo inválido.")
        return
    elif tipo_pesquisa == "cpf_cnpj" and (not termo_pesquisa.strip() or not termo_pesquisa.isnumeric()):
        logging.error("CPF/CNPJ inválido.")
        return

    # Define o URL da consulta com base no tipo de pesquisa
    if tipo_pesquisa == "processo":
        url = f"https://tjpi.pje.jus.br/1g/ConsultaPublica/listView.seam?numeroProcesso={termo_pesquisa}"
    elif tipo_pesquisa == "cpf_cnpj":
        url = f"https://tjpi.pje.jus.br/1g/ConsultaPublica/listView.seam?documento={termo_pesquisa}"
    else:
        logging.error("Tipo de pesquisa inválido.")
        return

    # Realiza a consulta
    response = requests.get(url)

    # Verifica o status da resposta
    if response.status_code != 200:
        logging.error(f"Erro na consulta: {response.status_code}")
        return

    # Extrai as informações do processo
    partes = ""
    status = ""
    movimentacoes = ""

    soup = BeautifulSoup(response.text, 'html.parser')

    partes_element = soup.find('div', {'id': 'divPartesPrincipais'})
    if partes_element:
        partes = partes_element.get_text()

    status_element = soup.find('div', {'id': 'divAndamentoProcesso'})
    if status_element:
        status = status_element.get_text()

    movimentacoes_element = soup.find('div', {'id': 'divMovimentacoes'})
    if movimentacoes_element:
        movimentacoes = movimentacoes_element.get_text()

    # Cria um dicionário com as informações do processo
    informacoes_do_processo = {
        "tipo_pesquisa": tipo_pesquisa,
        "termo_pesquisa": termo_pesquisa,
        "partes": partes,
        "status": status,
        "movimentacoes": movimentacoes,
    }

    # Salva as informações em um arquivo local
    with open("informacoes_processo.txt", "w") as arquivo:
        for chave, valor in informacoes_do_processo.items():
            arquivo.write(f"{chave}: {valor}\n")

    return informacoes_do_processo

if __name__ == "__main__":
    # Menu de opções
    print("Escolha o tipo de pesquisa:")
    print("1. Número de processo")
    print("2. CPF/CNPJ")
    
    escolha = input("Opção: ")

    if escolha == "1":
        tipo_pesquisa = "processo"
        termo_pesquisa = input("Número de processo: ")
    elif escolha == "2":
        tipo_pesquisa = "cpf_cnpj"
        termo_pesquisa = input("CPF/CNPJ: ")
    else:
        print("Escolha inválida.")
        exit()

    # Realiza a consulta
    informacoes_do_processo = consulta_processo(tipo_pesquisa, termo_pesquisa)

    if informacoes_do_processo:
        # Imprime as informações do processo
        print(informacoes_do_processo)
        print("Informações do processo foram salvas em 'informacoes_processo.txt'.")
