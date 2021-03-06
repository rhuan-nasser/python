import json, telegram.ext, os
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackContext
from time import sleep as s

def menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('''
/relatorio: Retorna informações essenciais para o contrato.

/monitoramento: Monitora a fila do suporte em tempo real, obtendo informações essenciais das requisições.

/tecnico: Retorna a quantidade de chamados atendidos por técnico.

/pendentes: Retorna os chamados que estão pendentes
''')
def relatorio(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Buscando informações do relatório...')

    import datetime, time, pandas as pd, emoji, os
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from time import sleep as sl

    # variáveis
    mes = str(datetime.date.today().month)
    ano = str(datetime.date.today().year)
    dia = str(datetime.date.today().day)
    completo = str(time.ctime())
    hora = completo[11:13]
    minuto = completo[14:16]
    chamados_estourados_no_inicio_do_atendimento = total_de_chamados = finalizados = pendentes = 0

    # Abre o navegador
    web = webdriver.Chrome('/home/nasser/Área de Trabalho/chromedriver')

    # Acessa o otrs
    web.get(<url>)
    sl(3)
    web.find_element_by_id('User').send_keys(<login>)
    web.find_element_by_id('Password').send_keys(<senha>, Keys.ENTER)

    web.maximize_window()
    sl(3)

    # Acessa os relatório
    web.find_element_by_xpath('//*[@id="nav-Reports"]/a').click()
    sl(0.5)
    web.find_element_by_xpath('//*[@id="nav-Reports-Statistics"]/a').click()
    sl(2)
    web.find_element_by_xpath('//*[@id="AppWrapper"]/div[3]/div[2]/div/div[2]/table/tbody/tr[19]/td[6]/a').click()
    sl(2)

    # Altera a data de acordo com a data atual para a extração
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStartMonth"]/option[{mes}]').click()
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStartYear"]/option[{ano[2:]}]').click()
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStopDay"]/option[{dia}]').click()
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStopMonth"]/option[{mes}]').click()
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStopYear"]/option[{ano[2:]}]').click()
    web.find_element_by_xpath(f'//*[@id="StartStatistic"]/span').click()
    sl(3)

    # Minimiza a janela
    web.close()

    # Renomeia o arquivo
    os.system(r'rename C:\Users\nasser\Downloads\Rel*.xlsx relatorio.xlsx')

    # Tratamento dos dados
    tabela = pd.read_excel(r"C:\Users\nasser\Downloads\relatorio.xlsx")
    headers = tabela.iloc[0]
    tabela = pd.DataFrame(tabela.values[1:], columns=headers)
    tabela['Tempo de solução em minutos'] = tabela['Tempo de solução em minutos'].astype(int)
    tabela['Primeira Resposta em Minutos'] = tabela['Primeira Resposta em Minutos'].astype(int)
    tabela['Número'] = tabela['Número'].astype(int)
    tabela['Ticket#'] = tabela['Ticket#'].astype(int)
    tabela['Delta de tempo de solução em minutos'] = tabela['Delta de tempo de solução em minutos'].astype(int)

    # Hora da abertura do chamado e o Atendente
    m10m = tabela['Primeira Resposta em Minutos'].mean()
    media_10_minutos = '{:.2f}'.format(m10m)

    # 1,3,36 horas
    ultrapassou_uma_hora = tabela.loc[tabela['Tempo de solução em minutos'] > 60].value_counts().sum()
    em_compliance_uma_hora = tabela.loc[tabela['Tempo de solução em minutos'] <= 60].value_counts().sum()
    ultrapassou_tres_horas = tabela.loc[tabela['Tempo de solução em minutos'] > 180].value_counts().sum()
    em_compliance_tres_horas = tabela.loc[tabela['Tempo de solução em minutos'] <= 180].value_counts().sum()
    ultrapassou_trinta_e_seis_horas = tabela.loc[tabela['Tempo de solução em minutos'] > 2160].value_counts().sum()
    em_compliance_trinta_e_seis_horas = tabela.loc[tabela['Tempo de solução em minutos'] <= 2160].value_counts().sum()

    # Total de chamados abertos, finalizados e pendentes
    qtde_de_chamados = tabela['Estado'].value_counts().sum()
    finalizados = tabela.loc[tabela['Estado'] == 'Finalizado com êxito'].value_counts().sum()
    qtde_de_pendentes_do_mes = 0
    pendentes_do_mes = tabela['Estado'] != 'Finalizado com êxito'
    for pendente in pendentes_do_mes:
        if pendente == True:
            qtde_de_pendentes_do_mes += 1

    # Técnicos
    airanildo = tabela.loc[
        tabela['Atendente/Proprietário'] == 'airanildo.lima', ['Atendente/Proprietário', 'Criado', 'Primeira Resposta',
                                                               'Primeira Resposta em Minutos',
                                                               'Tempo de solução em minutos']]
    thiago = tabela.loc[
        tabela['Atendente/Proprietário'] == 'thiago.gomes', ['Atendente/Proprietário', 'Criado', 'Primeira Resposta',
                                                             'Primeira Resposta em Minutos',
                                                             'Tempo de solução em minutos']]

    # Chamados por setores
    por_setor = tabela[['ID do Cliente', 'Ticket#']].groupby(['ID do Cliente']).count()
    por_setor.sort_values(by=['ID do Cliente', 'Ticket#'], ascending=False)

    # Serviços
    servico = tabela['Serviço'].value_counts()
    servicos_porcentagem = tabela['Serviço'].value_counts(normalize=True).map("{:.1%}".format)

    # Até 10 minutos
    chamados_estourados_no_inicio_do_atendimento = tabela.loc[
        tabela['Primeira Resposta em Minutos'] > 10].value_counts().sum()
    em_compliance_ate_10_minutos = tabela.loc[tabela['Primeira Resposta em Minutos'] <= 10].value_counts().sum()
    porcentagem_estourados_10_minutos = 100 - (chamados_estourados_no_inicio_do_atendimento * 100) / qtde_de_chamados

    # Até 1 hora
    porcentagem_estourados_1_hora = 100 - (ultrapassou_uma_hora * 100) / qtde_de_chamados

    # Até 3 horas
    porcentagem_estourados_3_hora = 100 - (ultrapassou_tres_horas * 100) / qtde_de_chamados

    # Até 36 horas
    porcentagem_estourados_36_horas = 100 - (ultrapassou_trinta_e_seis_horas * 100) / qtde_de_chamados

    update.message.reply_text(f'''
    Foram abertos {qtde_de_chamados} chamados do dia 1/{mes}/{ano} até 
o dia {dia}/{mes}/{ano}. Foram finalizados {finalizados} chamados 
e {qtde_de_pendentes_do_mes} ainda não foram finalizados.



Início do atendimento <= 10 minutos: 
(Meta: >= 90%):
Meta atual: {porcentagem_estourados_10_minutos:.0f}%
Compliance: {em_compliance_ate_10_minutos} chamado(s)
Vencidos:  {chamados_estourados_no_inicio_do_atendimento} chamado(s)
Media do tempo no início do atendimento:  {media_10_minutos} Segundos



Chamados resolvidos em até 1 hora: 
(Meta: >= 75%):
Meta atual: {porcentagem_estourados_1_hora:.0f}%
Compliance: {em_compliance_uma_hora} chamado(s)
Vencidos: {ultrapassou_uma_hora} chamado(s)



Chamados resolvidos em até 3 horas:
(Meta: >= 95%):
Meta atual: {porcentagem_estourados_3_hora:.0f}%
Compliance: {em_compliance_tres_horas} chamado(s)
Vencidos: {ultrapassou_tres_horas} chamado(s)



Chamados resolvidos em até 36 horas:
(Meta: >= 100%):
Meta atual: {porcentagem_estourados_36_horas:.0f}%
Compliance: {em_compliance_trinta_e_seis_horas} chamado(s)
Vencidos: {ultrapassou_trinta_e_seis_horas} chamado(s)



Atenciosamente,
Equipe de Atendimento ao Usuário
{emoji.emojize(":telephone_receiver:(61) 9999-9999   :computer:", use_aliases=True)}''')

    os.system(r'del /f /a C:\Users\nasser\Downloads\relatorio.xlsx')
def monitoramento(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('''Iniciado o monitoramento da fila de chamados!

Informações de futuras requisições de usuários serão encaminhadas para "Monitoramento do OTRS"''')

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from time import sleep as s
    from datetime import datetime
    import requests

    def hora_e_minuto():
        hora = datetime.today().hour
        minuto = datetime.today().minute
        if hora == 18 and minuto == 55:
            update.message.reply_text('Fim de expediente, tenha uma boa noite!!')
            exit()
            updater.start_polling()
    def logar():
        url = <url>
        login = <login>
        senha = <senha>

        # Abre o navegador
        w = webdriver.Chrome('/home/nasser/Área de Trabalho/chromedriver')
        w.maximize_window()
        w.get(url)
        w.find_element_by_id('User').send_keys(login)
        w.find_element_by_id('Password').send_keys(senha, Keys.ENTER)
        s(3)
        w.find_element_by_xpath('//*[@id="nav-Tickets"]/a').click()
        w.find_element_by_xpath('//*[@id="nav-Tickets-Queueview"]/a').click()
        w.minimize_window()

        count = 0
        while True:
            hora_e_minuto()

            abertos_na_fila = w.find_elements_by_xpath('//table/tbody/tr')

            if not abertos_na_fila:
                if count == 0:
                    update.message.reply_text('Não há chamados abertos na fila!')
                    count += 1
                s(5)
                w.refresh()

            if abertos_na_fila:
                count = 0
                prop = w.find_element_by_xpath('//td[10]/div').text

                if 'Admin OTRS' in prop:
                    qtde_de_chamados = 0
                    for chamados in abertos_na_fila:
                        todos_os_chamados_dic = dict()
                        todos_os_chamados_lis = list()

                        qtde_de_chamados += 1
                        ticket = chamados.get_attribute('id')
                        todos_os_chamados_dic['idade'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[5]').text
                        todos_os_chamados_dic['titulo'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[6]').text
                        todos_os_chamados_dic['estado'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[7]').text
                        todos_os_chamados_dic['setor'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[11]').text
                        todos_os_chamados_dic['responsavel'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[10]').text
                        todos_os_chamados_lis.append(todos_os_chamados_dic.copy())

                    for ch in todos_os_chamados_lis:
                        idade, titulo, estado, setor, responsavel = ch.values()

                        update.message.reply_text(f'''
#################################
{ticket}    Qtde: {qtde_de_chamados}   

Usuário/Título: {titulo} 

Setor: {setor}
Estado: {estado}
Tempo: {idade}
responsável: {responsavel}
#################################
    ''')

                    todos_os_chamados_dic.clear()
                    todos_os_chamados_lis.clear()
                    while True:
                        hora_e_minuto()
                        abertos_na_fila = w.find_elements_by_xpath('//table/tbody/tr')
                        s(3)
                        if abertos_na_fila:
                            pass
                        else:
                            break

                else:
                    qtde_de_chamados = 0
                    for chamados in abertos_na_fila:
                        todos_os_chamados_dic = dict()
                        todos_os_chamados_lis = list()

                        qtde_de_chamados += 1
                        ticket = chamados.get_attribute('id')
                        todos_os_chamados_dic['idade'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[5]').text
                        todos_os_chamados_dic['titulo'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[6]').text
                        todos_os_chamados_dic['estado'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[7]').text
                        todos_os_chamados_dic['setor'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[11]').text
                        todos_os_chamados_dic['responsavel'] = w.find_element_by_xpath(f'//table/tbody/tr[@id="{ticket}"]/td[10]').text
                        todos_os_chamados_lis.append(todos_os_chamados_dic.copy())

                    for ch in todos_os_chamados_lis:
                        idade, titulo, estado, setor, responsavel = ch.values()

                        update.message.reply_text(f'''
#################################
{ticket}    Qtde: {qtde_de_chamados}

Usuário/Título: {titulo} 

Setor: {setor}
Estado: {estado}
Tempo: {idade}
responsavel: {responsavel}
#################################
                    ''')

                    todos_os_chamados_dic.clear()
                    todos_os_chamados_lis.clear()
                    while True:
                        hora_e_minuto()
                        abertos_na_fila = w.find_elements_by_xpath('//table/tbody/tr')
                        s(3)
                        if abertos_na_fila:
                            pass
                        else:
                            break

    logar()
def tecnico(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Buscando as informações dos técnicos...')

    import datetime, time, pandas as pd, win32com.client as win32, emoji, os
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from time import sleep as sl

    # variáveis
    mes = str(datetime.date.today().month)
    ano = str(datetime.date.today().year)
    dia = str(datetime.date.today().day)
    completo = str(time.ctime())
    hora = completo[11:13]
    minuto = completo[14:16]
    chamados_estourados_no_inicio_do_atendimento = total_de_chamados = finalizados = pendentes = 0

    # Abre o navegador
    web = webdriver.Chrome('/home/nasser/Área de Trabalho/chromedriver')

    # Acessa o otrs
    web.get(<url>)
    sl(3)
    web.find_element_by_id('User').send_keys(<login>)
    web.find_element_by_id('Password').send_keys(<senha>, Keys.ENTER)

    web.maximize_window()
    sl(3)

    # Acessa os relatório
    web.find_element_by_xpath('//*[@id="nav-Reports"]/a').click()
    sl(0.5)
    web.find_element_by_xpath('//*[@id="nav-Reports-Statistics"]/a').click()
    sl(2)
    web.find_element_by_xpath('//*[@id="AppWrapper"]/div[3]/div[2]/div/div[2]/table/tbody/tr[19]/td[6]/a').click()
    sl(2)

    # Altera a data de acordo com a data atual para a extração
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStartMonth"]/option[{mes}]').click()
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStartYear"]/option[{ano[2:]}]').click()
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStopDay"]/option[{dia}]').click()
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStopMonth"]/option[{mes}]').click()
    web.find_element_by_xpath(f'//*[@id="UseAsRestrictionCreateTimeStopYear"]/option[{ano[2:]}]').click()
    web.find_element_by_xpath(f'//*[@id="StartStatistic"]/span').click()
    sl(3)

    # Minimiza a janela
    web.close()

    # Renomeia o arquivo
    os.system(r'rename C:\Users\nasser\Downloads\Rel*.xlsx relatorio.xlsx')

    tabela = pd.read_excel(fr"C:/Users/nasser/Downloads/relatorio.xlsx")
    nomes_das_colunas = tabela.loc[0]
    tabela = pd.DataFrame(tabela.values[1:], columns=nomes_das_colunas)

    atendente = tabela.loc[
        tabela['Atendente/Proprietário'] == 'airanildo.lima', ['Ticket#', 'ID do Cliente', 'Usuário Cliente',
                                                               'Atendente/Proprietário', 'Primeira Resposta em Minutos',
                                                               'Tempo de solução em minutos']]
    qtde_de_chamados_atendidos_por_tecnico = tabela.loc[:, ['Atendente/Proprietário']].value_counts()
    tabela['Primeira Resposta em Minutos'] = pd.to_numeric(tabela['Primeira Resposta em Minutos'])
    qtde_de_pendentes_do_mes = 0
    pendentes_do_mes = tabela['Estado'] != 'Finalizado com êxito'
    for pendente in pendentes_do_mes:
        if pendente == True:
            qtde_de_pendentes_do_mes += 1

    tabela['Tempo de solução em minutos'] = tabela['Tempo de solução em minutos'].astype(int)
    tabela['Primeira Resposta em Minutos'] = tabela['Primeira Resposta em Minutos'].astype(int)
    setores_mais_usuarios = tabela['Usuário Cliente'].groupby(tabela['ID do Cliente']).value_counts()

    total_de_chamados = tabela.loc[tabela['Tempo de solução em minutos'] <= 180].value_counts().sum()
    estourado = tabela.loc[tabela['Primeira Resposta em Minutos'] > 10].value_counts().sum()
    # medidor = total_de_chamados - chamados_estourados_no_inicio_do_atendimento
    # print(medidor)
    # print(total_de_chamados)
    # print(estourado)

    # airanildo = tabela.loc[tabela['Atendente/Proprietário'] == 'airanildo.lima', ['Atendente/Proprietário', 'Criado', 'Primeira Resposta', 'Primeira Resposta em Minutos', 'Tempo de solução em minutos']]
    # thiago = tabela.loc[tabela['Atendente/Proprietário'] == 'thiago.gomes', ['Atendente/Proprietário', 'Criado', 'Primeira Resposta', 'Primeira Resposta em Minutos', 'Tempo de solução em minutos']]

    # top_usuarios = tabela[['Usuário Cliente', 'Ticket#']].groupby('Usuário Cliente').count()
    # airanildo.to_excel(fr"C:\Users\nasser\OneDrive\Área de Trabalho\Relatório diário detalhado\Airanildo Chamados.xlsx", index=False)
    # thiago.to_excel(fr"C:\Users\nasser\OneDrive\Área de Trabalho\Relatório diário detalhado\Thiago Chamados.xlsx", index=False)

    airanildo = tabela.loc[tabela['Atendente/Proprietário'] == 'airanildo.lima'].value_counts().sum()
    thiago = tabela.loc[tabela['Atendente/Proprietário'] == 'thiago.gomes'].value_counts().sum()

    os.system(r'del /f /a C:\Users\nasser\Downloads\relatorio.xlsx')

    update.message.reply_text(f'Airanildo atendeu {airanildo} chamados e o Thiago atendeu {thiago} chamados.')
def pendentes(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Verificando se há chamados pendentes na fila...')

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from time import sleep as s

    url = <url>
    login = <login>
    senha = <senha>

    # Abre o navegador
    w = webdriver.Chrome('/home/nasser/Área de Trabalho/chromedriver')
    w.maximize_window()
    w.get(url)
    w.find_element_by_id('User').send_keys(login)
    w.find_element_by_id('Password').send_keys(senha, Keys.ENTER)
    s(3)
    w.find_element_by_xpath('//*[@id="nav-Tickets"]/a').click()
    w.find_element_by_xpath('//*[@id="nav-Tickets-Queueview"]/a').click()
    w.find_element_by_xpath('//*[@id="AppWrapper"]/div[3]/div[1]/div[1]/ul/li[3]/a').click()

    chamados_fila_de_pendentes = w.find_elements_by_xpath('//table/tbody/tr')

    if not chamados_fila_de_pendentes:
        print('Não há chamados pendentes na fila!')
    if chamados_fila_de_pendentes:
        qtde_de_chamados_pendentes = 0
        todos_os_chamados_pendentes_dic = dict()
        todos_os_chamados_pendentes_lis = list()

        for chamado in chamados_fila_de_pendentes:
            qtde_de_chamados_pendentes += 1
            ticket = chamado.get_attribute('id')
            todos_os_chamados_pendentes_dic['idade'] = w.find_element_by_xpath(
                f'//table/tbody/tr[@id="{ticket}"]/td[5]').text
            todos_os_chamados_pendentes_dic['titulo'] = w.find_element_by_xpath(
                f'//table/tbody/tr[@id="{ticket}"]/td[6]').text
            todos_os_chamados_pendentes_dic['estado'] = w.find_element_by_xpath(
                f'//table/tbody/tr[@id="{ticket}"]/td[7]').text
            todos_os_chamados_pendentes_dic['setor'] = w.find_element_by_xpath(
                f'//table/tbody/tr[@id="{ticket}"]/td[11]').text
            todos_os_chamados_pendentes_lis.append(todos_os_chamados_pendentes_dic.copy())

        w.close()
        update.message.reply_text(f'Quantidade de chamados pendentes: {qtde_de_chamados_pendentes}')

        for ch in todos_os_chamados_pendentes_lis:
            idade, titulo, estado, setor = ch.values()
            update.message.reply_text(f'''
{titulo}    

Setor: {setor}
Estado: {estado}
Idade: {idade}
------------------------------------------------(#)
        ''')

updater = Updater(<token_telegram_bot>)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("menu", menu))
dispatcher.add_handler(CommandHandler("relatorio", relatorio))
dispatcher.add_handler(CommandHandler("monitoramento", monitoramento))
dispatcher.add_handler(CommandHandler("tecnico", tecnico))
dispatcher.add_handler(CommandHandler("pendentes", pendentes))

updater.start_polling()
