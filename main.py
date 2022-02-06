from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, PrefixHandler)
from telegram.ext.filters import Filters, MessageFilter
from telegram.utils.request import Request
import random, logging, datetime, requests, pytz, os, scrapy, platform
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import pandas as pd
import socket as socket
import json
from datetime import datetime
import pytz
import sensData
import urlLinks
import urlMedia

#LOG
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#VARIAVEIS
THEGAME = range(2)
varScore = 0
varLives = 5
varEmpate = 0
    #WELCOME
def welcome(update: Update, context: CallbackContext):
    for membro in update.message.new_chat_members:
        update.message.reply_text(f"Olá, <b>{membro.first_name}</b>!\nSeja bem-vindo/a ao grupo!\nSeja participativo/a e leia as regras.\nPara começar, digite <b>?menu</b>.", parse_mode ='HTML')
    #START
def start(update: Update, context: CallbackContext):
    primNome = update.message.from_user.first_name
    context.bot.send_message(chat_id= update.message.chat_id, text="Olá, " + primNome + "!\nBem-vindo ao <i>CæsarBot 0.2 «Sardegna»</i>! \U0001F916" + "\n----------------------------------------------------\nLISTA DE COMANDOS:\n\U0001F4CB <code>?menu</code> » menu e meus comandos\n\U0001F3A5 <code>?cine</code> » estreias do cinema\n\U0001F3B0 <code>?loto</code> » resultados da loteria\n\U0001F3AE <code>?steam</code> » ofertas do steam\n\u270B\uFE0F <code>?jokenpo</code> » pedra, papel, tesoura\n\U0001F468\u200D\U0001F3EB <code>?udemy</code> » cursos free ou com desconto de 100% na udemy\n\U0001F517 <code>?links</code> » links de compiladores online, bancos de imgs, vídeos, vetores etc.\n\U0001F5D2 <code>?clog</code> » registro de versões e respectivas alterações/correções de erros/melhorias\n----------------------------------------------------\n", parse_mode ='HTML')
    #MENU
def menu(update: Update, context: CallbackContext):
    primNome = update.message.from_user.first_name
    context.bot.send_message(chat_id= update.message.chat_id, text="Olá, " + primNome + "!\nBem-vindo ao <i>CæsarBot 0.2 «Sardegna»</i>! \U0001F916" + "\n----------------------------------------------------\nLISTA DE COMANDOS:\n\U0001F4CB <code>?menu</code> » menu e meus comandos\n\U0001F3A5 <code>?cine</code> » estreias do cinema\n\U0001F3B0 <code>?loto</code> » resultados da loteria\n\U0001F3AE <code>?steam</code> » ofertas do steam\n\u270B\uFE0F <code>?jokenpo</code> » pedra, papel, tesoura\n\U0001F468\u200D\U0001F3EB <code>?udemy</code> » cursos free ou com desconto de 100% na udemy\n\U0001F517 <code>?links</code> » links de compiladores online, bancos de imgs, vídeos, vetores etc.\n\U0001F5D2 <code>?clog</code> » registro de versões e respectivas alterações/correções de erros/melhorias\n----------------------------------------------------\n", parse_mode ='HTML')
    #CHANGELOG
def changelog(update, context):
    update.message.reply_text("ChangeLog\n0.1.5 'Piemonte'\n\n»Corrigida a localização dos resultados das promoções no Steam\n»Corrigido erro na contagem da pontuação do Jokenpo")
    update.message.reply_text("ChangeLog\n0.2 «Sardegna» (11.08.2021)\n\n»Adicionado sistema de listas de sites (Fase de teste)\n»Comando ?steam aprimorado:\nI. Modelo de resposta das entradas aprimorado\nII. Corrigido erro de retorno de entradas Steam referentes a pacotes de jogos\nIII. Imagens raspadas diretamente da db de cada jogo, ao invés do link de redirecionamento\nIV. Adicionada a entrada 'Desconto' e link de redirecionamento substituído por hiperlink\n»Nomes de comandos reduzidos para maior facilidade:\nI. ?cinema -> ?cine\nII. ?loteria -> ?loto\nIII. ?changelog -> ?clog\nAdicionadas informações do servidor do bot através do comando ?info")  #INFO
def myInfo(update, context):
    context.bot.send_message(chat_id = update.message.chat_id, text= "<b>Bot</b>\nCaesarBot 0.2 «Sardegna»\nCriado por @PrizrakXIII\nImplantado em: 13.05.2021\n\n<b>Servidor</b>\nPlataforma: " + platform.platform() + "\nO.S.: " + platform.system() + " " + platform.machine() +"\nVersão: " + platform.version(), parse_mode="HTML")
#JOKENPO
def jokenpo(update: Update, context: CallbackContext):
    update.message.reply_text('Vamos jogar <b>Pedra ✊ Papel ✋ Tesoura ✌️</b>?\n<b>REGRAS:</b>\nVocê começa com <b>5</b> vidas e perde uma cada vez que eu ganhar. Se você acertar, ganha <b>1</b> ponto. O jogo acaba quando você não tiver mais vidas restantes.\n<b>COMANDOS:</b>\n<code>pedra</code> / <code>papel</code> / <code>tesoura</code> » jogar\n<code>status</code> » ver pontuação, vidas e empates\n<code>sair</code> » terminar o jogo a qualquer hora\nEscolha uma opção:', parse_mode ='HTML')
    return THEGAME  
#JOGO JOKENPO
def thegame(update,context):
    msgUser = update.message.text.lower()
    global varScore
    global varLives
    global varEmpate
    while True:
        computer = ("pedra", "papel", "tesoura")
        computer = random.choice(computer)
        if (msgUser== "pedra" and computer == "papel") or (msgUser== "papel" and computer == "tesoura") or (msgUser=="tesoura" and computer == "pedra"):
            update.message.reply_text("Eu escolhi <i>" + computer + "</i>. <b>Você perdeu!</b>", parse_mode ='HTML')
            varLives -= 1
        if (msgUser== "pedra" and computer == "tesoura") or (msgUser == "papel" and computer == "pedra") or (msgUser == "tesoura" and computer == "papel"):
            update.message.reply_text("Eu escolhi <i>" + computer + "</i>. <b>Você ganhou!</b>", parse_mode ='HTML')
            print("The computer chose", computer,". You win.")
            varScore +=1
        if (msgUser== computer):
            update.message.reply_text("Nós dois escolhemos <i>" + computer +"</i>. <b>Empate!</b>", parse_mode ='HTML')
            varEmpate +=1
        if (msgUser== "status"):
            update.message.reply_text("Sua pontuação atual: " + str(varScore) + " pontos.\nVocê possui "+ str(varLives)+ " vidas restantes.\nNós empatamos " + str(varEmpate) +' vezes.')
        if (msgUser== "sair") or (varLives == 0):
            update.message.reply_text("Jogo finalizado. Sua pontuação final: <b>" + str(varScore) + "</b> pontos.\nEmpatamos " + str(varEmpate) +' vezes.\n', parse_mode ='HTML')
            varScore = 0
            varEmpate = 0
            varLives = 5
            return ConversationHandler.END
        update.message.reply_text('Escolha uma opção: ')
        return
#LOTERIA
def loteria(update, context):
    url = Request(urlLinks.loteria, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(url)
    bs = BeautifulSoup(html, 'lxml')
    concursos = bs.findAll('div', attrs={'class': 'lt-result'})
    megaSena = concursos[0]
    quina = concursos[1]
    lotoFacil = concursos[2]
    lotoMania = concursos[3]
    duplaSena1 = concursos[4]
    duplaSena2 = concursos[5]
    update.message.reply_text("<b>RESULTADOS DA LOTERIA</b>:\n\U0001f7e2 <b>Mega-Sena</b>:" + str(megaSena.text) +"\n\U0001f535 <b>Quina</b>:" + str(quina.text) +"\n\U0001f7e3 <b>Lotofácil</b>:" + str(lotoFacil.text) +"\n\U0001f7e0 <b>Lotomania</b>:" + str(lotoMania.text)+"\n\U0001f534 <b>Dupla Sena 1</b>:" + str(duplaSena1.text)+"\n\U0001f534 <b>Dupla Sena 2</b>:" + str(duplaSena2.text), parse_mode='HTML')
#PROMOÇÕES STEAM
def steamStore(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    res = requests.get(urlLinks.steamAPIUrl)
    paramCom = ['prm', 'nov', 'top', 'brv']
    #### FUNÇÃO
    def listagem(categoria):
        try:
            lista = res.json()[categoria]['items']
            random.shuffle(lista)
            varVezes = 0
            for i in lista:
                if varVezes < 5:           
                    gamePic = i['large_capsule_image']
                    gameName = i['name']
                    if i['original_price'] is None:
                        gamePriceOrg = "Gratuito"
                    
                    
                    # ADICIONAR VERIFICAÇÃO DE CATEGORIA. SE CATEGORIA FOR COMING_SOON, RETIRAR TODOS OS PRICES
                    
                    
                    else:
                        gamePriceOrg = (f"R${(i['original_price']/100):.2f}").replace('.',',')
                    if i['discounted'] == True:                           
                        gamePriceFin = (f"R${(i['final_price']/100):.2f}").replace('.',',')
                        gameDiscount =f"{i['discount_percent']}%"
                    else:
                        gamePriceFin = (f"R${(i['final_price']/100):.2f}").replace('.',',')
                        gameDiscount = "Nenhum!"
                    if (i['type'] == 0):    tipo = "app/"
                    elif (i['type'] == 1):  tipo = "sub/"
                    elif (i['type'] == 2):  tipo = "bundle/"
                    gameURL =f"{urlLinks.steamLink}{tipo}{i['id']}"
                    #gameExpDate = datetime.fromtimestamp(i['discount_expiration'],pytz.timezone("America/Sao_Paulo")).strftime('%d/%m/%y | %H:%M')
                    gamePlatf = []                
                    if (i['windows_available']):    gamePlatf.append('🪟')
                    if (i['mac_available']):    gamePlatf.append('🍎')
                    if (i['linux_available']):  gamePlatf.append('🐧')        
                    gamePlatfFinal = " | ".join(gamePlatf)
                    context.bot.send_photo(chat_id= update.message.chat_id, photo= gamePic,
                    caption=(f'''<b>{gameName}</b>
\U0001f3ae Plataforma(s): {gamePlatfFinal}
\u274C Preço original: <b>{gamePriceOrg}</b>
\u2705 Preço final: <b>{gamePriceFin}</b>
\U0001F3F7 Desconto: <b>{gameDiscount}</b>'''),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Página no Steam', url=gameURL)],]), parse_mode="HTML")
                    varVezes += 1
                else:
                    break
        except:
            update.message.reply_text('Não foi possível recuperar esta lista no Steam. Pode haver algum problema com a API. Tente novamente mais tarde.')
#### FIM DA FUNÇÃO
    try:
        if (context.args[0]) == paramCom[0]:    listagem('specials')
        elif (context.args[0]) == paramCom[1]:  listagem('new_releases')
        elif (context.args[0]) == paramCom[2]:  listagem('top_sellers')
        elif (context.args[0]) == paramCom[3]:  listagem('coming_soon')
        #elif (context.args[0]) not in paramCom:
        else:
            update.message.reply_text('Esse parâmetro não existe! Confira a lista de parâmetros:\n <b>?steam ofertas</b>: retorna os jogos atualmente em oferta',parse_mode="HTML")
    except IndexError:
        update.message.reply_text('Por favor, envie o comando com um parâmetro!')
    
# ------------------------------------------------------------

#ESTREIAS DO CINEMA
def cineestreia(update, context):
    url = Request(urlLinks.cinema10, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urlopen(url)
    except HTTPError as falha:
        update.message.reply_text(falha)
    except URLError as falha:
        update.message.reply_text("Servidor não encontrado!", falha)
    bs = BeautifulSoup(html, 'lxml')
    cartoes = bs.findAll('div', attrs={'class': 'post-article'})
    varVezes = 1
    random.shuffle(cartoes)
    for cartao in cartoes:
        if varVezes <= 5:
            poster = cartao.find('img', attrs={'class': 'bordaRoxa'})
            titulo = cartao.find('span', attrs={'class': 'movie-name'})
            movMetaData = cartao.find_all('span', attrs={'class': 'movie-metadata'})
            dataEstreia = movMetaData[0].contents[-1].strip()
            genFilme = movMetaData[1].contents[-1].strip()
            durFilme = movMetaData[2].contents[-1].strip()
            sinopse = cartao.find('span', attrs={'class': 'movie-desc'}).contents[-1].strip()
            context.bot.send_photo(chat_id= update.message.chat_id, photo= poster.attrs['src'], caption= (
                "<b>" +str(titulo.text.upper()) + "</b>\n\U0001F4C5 <b>Estreia: </b>"+str(dataEstreia) + "\n\U0001F3AD <b>Genêro(s): </b>" + str(genFilme) +'\n\U0001F558 <b>Duração: </b>' + str(durFilme) + "\n\U0001F441\u200D\U0001F5E8 <b>Sinopse: </b>" + str(sinopse)
            ), parse_mode='HTML')
            varVezes += 1
#CUPONS -100% NA UDEMY
def udemy(update, context):
    url = Request(urlLinks.udemy, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(url).read()
    bs = BeautifulSoup(html, 'html.parser')
    print(bs.text)
    cartoes = bs.find('section', attrs={'class': 'card'})
    curso = cartoes.find('a', attrs={'class': 'card-header'})
    print(curso.text)
    print(curso.attrs['href'])
    update.message.reply_text('<b>' + str(curso.text)+ '</b>\n' + str(curso.attrs['href']), parse_mode='HTML')
#LISTA DE SITES
def listasites(update, context):
    df = pd.read_csv("lista_links.csv")
    comp1 = pd.DataFrame(df, columns= [context.args[0]])    
    comp1 = comp1.dropna()
    context.bot.send_message(chat_id= update.message.chat_id, text=str(comp1), disable_web_page_preview=True)

#def moedas(update, context):
#    url = Request("https://www.infomoney.com.br/", headers={'User-Agent': 'Mozilla/5.0'})
#    html = urlopen(url)
#    bs = BeautifulSoup(html, 'lxml')
#    moedinhas = bs.find('div', attrs={'id': 'ticker-content'})
#    print(bs.text)
#    listaMoedas = moedinhas.find('a')
#    print(listaMoedas)
    
def vocab(update: Update, context: CallbackContext) -> None:
    try:        
        verbete = requests.get(urlLinks.defUrl + context.args[0])
        respostas = json.loads(verbete.content)
        cont = 1
        txtFinal = ''
        for item in respostas:
            conjMeanings = '\n• '.join(item['meanings'])
            txtFinal += (f'{cont}. <i>{item["class"]}</i>\n• {conjMeanings} \n\n')
            cont += 1
            print(txtFinal)
            #context.bot.send_message(chat_id= update.message.chat_id, text=('<b>' + context.args[0] + '</b>\n<i>' + item['class'] + '</i>\n\n' + conjMeanings), parse_mode="HTML")
        context.bot.send_message(chat_id= update.message.chat_id, text=(f'<b>{context.args[0]}</b>\n{txtFinal}'), parse_mode="HTML")
        return        
    except:
        context.bot.send_message(chat_id= update.message.chat_id, text=(f"Não foi possível encontrar <b>{context.args[0]}</b>. Tente novamente."), parse_mode="HTML")
        return

def shrt(update: Update, context: CallbackContext) -> None:
    try:
        linkUser = {'query': f'{context.args[0]}'}
        requisicao = requests.get(urlLinks.shortUrl, params=linkUser)
        linksFinais = json.loads(requisicao.content)
        linkCurto = linksFinais['is.gd']
        print(type(linkCurto))
        print(linkCurto)
        context.bot.send_message(chat_id= update.message.chat_id, text=("Link curto: <b>" + linkCurto + "</b>"), parse_mode="HTML", disable_web_page_preview=True)
        return
    except:
        context.bot.send_message(chat_id= update.message.chat_id, text=("Não foi possível encurtar este link. Tente novamente mais tarde."))
        return

def imgA(update: Update, context: CallbackContext):
    photoFile = update.message.photo[-1].get_file()
    print(type(photoFile))
    context.bot.send_message(chat_id = update.message.chat_id, text="Imagem recebida!")
    photoFile.download('user_pic2.jpg')
    context.bot.send_photo(chat_id=update.message.chat_id, photo=update.message.photo[-1])
    #context.bot.send_photo(chat_id=update.message.chat_id, photo=open('user_pic2.jpg', 'rb'))
   

def mgnt(update: Update, context: CallbackContext) -> None:
    try:
        linkUser = {'m': f'{context.args[0]}'}
        requisicao = requests.get(urlLinks.shortMagnet, params=linkUser)
        linksFinais = json.loads(requisicao.content)
        linkCurto = linksFinais['shorturl']
        context.bot.send_message(chat_id= update.message.chat_id, text=("Link curto: <b>" + linkCurto + "</b>"), parse_mode="HTML", disable_web_page_preview=True)
        return
    except:
        context.bot.send_message(chat_id= update.message.chat_id, text=("Não foi possível encurtar este magnet."))
        return

def keyWords(update, context):
    listaPal = ["césar", "cesar", "julio", "júlio", "julius", "kaiser"]
    msgUser = update.message.text.lower()
    updtChat = update.message.chat_id
    #if (msgUser[::-1] == msgUser) and (len(msgUser) > 3):
    #    update.message.reply_text('Palíndromo!')
    if "obrigado" in msgUser.lower():
        context.bot.send_video(chat_id = updtChat, video = urlMedia.thx)
    if "cringe" in msgUser:
        context.bot.send_video(chat_id = updtChat, video = urlMedia.cringe)
    if "xiu!" in msgUser:
        context.bot.send_video(chat_id = updtChat, video = urlMedia.shhh)
    if "hmmm" in msgUser:
        context.bot.send_video(chat_id = updtChat, video = urlMedia.hmmm)
    if "geek" in msgUser:
        context.bot.send_video(chat_id = updtChat, video = urlMedia.geek)
    if "php" in msgUser:
        context.bot.send_photo(chat_id = updtChat, photo = urlMedia.php)
    if "vinho" in msgUser:
        context.bot.send_photo(chat_id = updtChat, photo = urlMedia.vinho)
    if "casas bahia" in msgUser:
        context.bot.send_photo(chat_id = updtChat, photo = urlMedia.bahia)
    if "patos" in msgUser:
        context.bot.send_photo(chat_id = updtChat, photo = urlMedia.pato, caption="Eu acredito na sincera superioridade intelectual dos patos de todo este planeta.")
    if "analise" in msgUser:
        context.bot.send_photo(chat_id = updtChat, photo = urlMedia.analise)
    if "freebsd" in msgUser:
        context.bot.send_video(chat_id = updtChat, video = urlMedia.freebsd)
    if "ebaaa" in msgUser:
        context.bot.send_video(chat_id = updtChat, video = urlMedia.ebaaa)
    for pal in listaPal:
        if pal in msgUser:
            listaResp1 = ["Sim, sou eu mesmo!", "Fala, meu romanizado!", "Veni, vidi, vici!", "Saudações!", "Olá, como tem passado?", "CæsarBot no pedaço!", "Pode falar, companheiro!"]
            resp1 = random.choice(listaResp1)
            update.message.reply_text(resp1)
            break
    # Função na qual o bot recebe texto através da MsgHandler e retorna algo

    if (len(msgUser) > 1) and (msgUser[0] == "?"):
        update.message.reply_text('Este comando <b>não existe</b>!\nPor favor, use <code>?menu</code> para ver os comandos disponíveis.', parse_mode ='HTML')
        return
#computer = random.choice(listaPal)


def main():
    updater = Updater(token= os.environ['TGTOKEN'])
    
    
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    convHandler = ConversationHandler( #comandos do jogo
        entry_points=[PrefixHandler('?', 'jokenpo', jokenpo)],
        fallbacks=[],
        states = {
            THEGAME: [MessageHandler(Filters.text, thegame)]
        })
    dp.add_handler(convHandler)
    dp.add_handler(PrefixHandler('?', 'menu', menu))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(PrefixHandler('?', 'loto', loteria))
    dp.add_handler(PrefixHandler('?', 'steam', steamStore))
    dp.add_handler(PrefixHandler('?', 'udemy', udemy))
    dp.add_handler(PrefixHandler('?', 'cine', cineestreia))
    dp.add_handler(PrefixHandler('?', 'clog', changelog))
    dp.add_handler(PrefixHandler('?', 'info', myInfo))
    dp.add_handler(PrefixHandler('?', 'links', listasites))
    dp.add_handler(PrefixHandler('?', 'def', vocab))
    dp.add_handler(PrefixHandler('?', 'shrt', shrt))
    dp.add_handler(PrefixHandler('?', 'mgnt', mgnt))
    #dp.add_handler(PrefixHandler('?', 'moedas', moedas))
    dp.add_handler(MessageHandler(Filters.text, keyWords))
    #o handler aguarda texto (e o filtra), e o que estiver dentro de keywords retornará os comandos
    dp.add_handler(MessageHandler(Filters.photo & Filters.caption_regex(r'\d+'), imgA))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()