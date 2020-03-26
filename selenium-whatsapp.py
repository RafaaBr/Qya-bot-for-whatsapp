import os
import requests
import json
import time 
import oauth2   # Login tt
import urllib.parse #tt

from selenium import webdriver  # Importa tudo o que e necessario para o funcionamento do navegador (firefox, chrome)
from selenium.webdriver.chrome.options import Options  # Importa para salvar cookies do navegador(evitar ficar fazendo logins)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot = ChatBot('bot')
trainerer = ListTrainer(chatbot)

diretorio_drive = os.getcwd()  # serve para ir na pasta do arquivo .py
chrome_options = Options()  # variavel para armazenar as opções do navegador
chrome_options.add_argument("--user-data-dir=chrome-data")  # Aqui adiciona ao webdriver as opções do seu navegador normal, evitando ficar fazendo logins, salvando sessões
driver = webdriver.Chrome(diretorio_drive + '/chromedriver.exe', options=chrome_options)  # Lugar onde está o webdriver
chrome_options.add_argument("user-data-dir=chrome-data")  # Atualiza as opções
driver.get('https://web.whatsapp.com/')  # Abre a pagina desejada
driver.implicitly_wait(15)  # Espera 15 segundos para começar o codigo principal

ListaCadastrados = ['Meu', 'Qya']

def msgCadastrados():
    try:
    	for contato in ListaCadastrados:
	        nome = driver.find_element_by_xpath('(//span[@title="'+ str(contato) +'"])[1]')
	        nome.click()
	        envia_mensagem(msgParaCadastrados)
	        pass
    except Exception as e:
        print('Erro ao enviar msgCadastrados', e)
        pass
        


def novoCadastro():
	novoC = driver.find_element_by_xpath("//div[@class='_19vo_']//span[1]").text
	ListaCadastrados.append(novoC)
	envia_mensagem("Você foi adicionado a transmissão de novidades")
	print("adicionado a lista>", novoC)
	menu = '1'



def acha_nova_mensagem():
    try:
        novamensagem = driver.find_element_by_xpath("(//span[@class='P6z4j'])")
        novamensagem.click()
        novamensagem.click()
        pass
    except Exception as e:
        print("erro nova mensagem>", e)
        pass



def pegaConversa():
    try:
        ultimaMensagemRecebida = driver.find_elements_by_class_name('_12pGw')
        ultimo = len(ultimaMensagemRecebida) - 1
        texto = ultimaMensagemRecebida[ultimo].find_element_by_css_selector('span.selectable-text').text
        return texto
    except Exception as e:
        print("erro ao pegar mensagem>", e)
        pass



def envia_mensagem(mensagem):  # Função envia mensagem
    try:  # tente
        localiza_chat = driver.find_element_by_class_name('_3u328')  # Acha na pagina o elemento chat
        valor = "*Qya:* " + str(mensagem)
        for parte in valor.split('\n'):
           for espaco in parte.split('+'):
              localiza_chat.send_keys(espaco)  # Escreve no chat a mensagem
              ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()
        localiza_enviar = driver.find_element_by_class_name('_3M-N-')  # Acha na pagina o elemento botão enviar
        localiza_enviar.click()  # Clica no botão
    except Exception as o:  # Caso de exceção
        print('erro no bloco envia_mensagem: ', o)
        pass  # Continua o codigo



def treinar(mensagem):
    resposta = 'Como respondo isso? utilize ";' + str(mensagem) + '"'
    envia_mensagem(resposta)
    novo = []
    try:
        while True:
            ultima = pegaConversa()
            if ultima == "!":
                envia_mensagem("Você pulou meu aprendizado.")
                break
            elif ultima.replace(';', '') != '' and ultima != mensagem and ultima[0] == ";":
                print(mensagem.lower().strip())
                print(ultima.replace(';', '').lower().strip())
                novo.append(mensagem)
                novo.append(ultima.replace(';', ''))
                trainerer.train(novo)
                envia_mensagem("Pronto, aprendi!")
                break
    except Exception as e:
    	print('erro treinar', e)
    	pass



def automensagem():
    try:
        texto = str(pegaConversa().lower().strip())
        respostaauto = chatbot.get_response(texto)
        if float(respostaauto.confidence) < 0.5:
           treinar(pegaConversa())
        else:
            envia_mensagem(respostaauto)
    except Exception as e:
        print('erro automensagem', e)
        pass



def procuraFilmes():
    try:
        Filme = pegaConversa()[2:]  # Nome do filme
        req = requests.get('http://www.omdbapi.com/?t=' + Filme + '&apikey=98200edc')   # Procura o filme no site
        get = json.loads(req.text)   # Transforma de json para .text
        titulo = get['Title']   # Pega o titulo
        ano = get['Year']   # Pega o ano
        atores = get['Actors']  # Pega os atores
        genero = get['Genre']   # Pega os generos
        nota = get['imdbRating']    # Pega nota
        info = '+*Titulo>* ' + titulo + '+*Genero>* ' + genero + '+*Atores>* ' + atores + '+*Ano*> ' + ano + '+*Nota>* ' + nota    # Organiza os dados
        envia_mensagem(info)    # Envia info
    except Exception as e:  # Caso de exceção
        print('erro achar filme:', e)   # printa o erro
        envia_mensagem('Filme não encontrado')  # envia mensagem avisando que não achou
        pass



def enviaValorDolar():
    try:
        requisicaoDollar = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
        respostaDollar = json.loads(requisicaoDollar.text)
        miniDollar = respostaDollar['USD']['low']
        maxiDollar = respostaDollar['USD']['high']
        horariobuscadoDollar = respostaDollar['USD']['create_date']
        envia_mensagem('*-----Dólar-----*')
        envia_mensagem('*Máxima>* ' + maxiDollar)
        envia_mensagem('*Mínimo>* ' + miniDollar)
        envia_mensagem('*Consultado em>* ' + horariobuscadoDollar)
    except Exception as es:
        print('Erro em enviar dolar:', es)
        pass



def enviaClima():
    try:
        cidadeClima = pegaConversa()[2:]
        reqClima = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + cidadeClima + '&APPID=1f2429b7c72b8e0c821d2885c060c0a4')
        dadosClima = json.loads(reqClima.text)
        tempoClima = dadosClima['weather'][0]['main']
        temperaturaClima = float(dadosClima['main']['temp']) - 273.15
        envia_mensagem('*Clima de* ' + cidadeClima)
        envia_mensagem('*Condição do tempo>* ' + tempoClima)
        envia_mensagem('*Temperatura>* ' + str(int(temperaturaClima)))
    except Exception as e:
        print('erro clima > ', e)
        pass



def enviaTwitter():
    consumer_key = '' #chave publica
    consumer_secret = '' #chave_secreta

    token_key = '' # Token publico
    token_secret = ''  # Token secreto

    consumer = oauth2.Consumer(consumer_key, consumer_secret)   # junta chaves
    token = oauth2.Token(token_key, token_secret)   # junta tokens
    cliente = oauth2.Client(consumer, token)    # junta chaves com tokens

    query = pegaConversa()[2:]  # Pesquisa isso
    query_codificada = urllib.parse.quote(query, safe='')   
    requisicao = cliente.request('https://api.twitter.com/1.1/statuses/update.json?status=' + query_codificada, method='POST')

    decodificar = requisicao[1].decode()    # Decotifica para json

    objeto = json.loads(decodificar)    

    envia_mensagem("Twitter postado>",pegaConversa()[2:])



ultima = pegaConversa()
while True:  # Enquanto verdadeiro
    try:
        print('O que deseja fazer?\n [1] - Enviar mensagem para cadastrados\n [2] - Mensagens automaticas')
        menu = input('>')
        while menu == '1':
            msgParaCadastrados = input('O que deseja enviar? >')
            if msgParaCadastrados == '/b' or msgCadastrados == '/q':
            	print('O que deseja fazer?\n [1] - Enviar mensagem para cadastrados\n [2] - Mensagens automaticas')
            	menu = input('>')
            else:
            	msgCadastrados()
            	pass
        while menu == '2':
        	if pegaConversa() != '' and pegaConversa() != ultima:
	            if pegaConversa()[0:1] == '+':
	                automensagem()
	            elif pegaConversa().lower()[0:2] == 'f:':
	                procuraFilmes()
	            elif pegaConversa().lower()[0:2] == 'd:':
	                enviaValorDolar()
	            elif pegaConversa().lower()[0:2] == 'c:':
	                enviaClima()
	            elif pegaConversa().lower()[0:4] == 'cad:':
	            	novoCadastro()
	            	'''
	            elif pegaConversa().lower()[0:2] == 't:':
	                enviaTwitter()
	                '''
	            else:
	            	time.sleep(3)
	            	acha_nova_mensagem()
	        if menu == '/quit':
	            exit()
    except Exception as e:
        print('erro principal >', e)
        pass