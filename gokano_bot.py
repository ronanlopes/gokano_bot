#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
import cookielib
import re
from time import sleep
from daemonize import daemonize
from time import gmtime, strftime

#cria um navegador, um browser de codigo
br = mechanize.Browser()
url = 'http://www.gokano.com'
email = 'xxx@gmail.com' 
senha = 'xxx'   

# Prepara para tratar cookies
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Ajusta algumas opções do navegador
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Configura o user-agent.
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11;\
 U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615\
Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#tempo de atraso em minutos entre cada requisição
tempo_atraso = 60

@daemonize(stdout='log.txt', stderr='gokano_bot_log.txt')
def gokano_bot():
  while True:

    print "Iniciando Tentativa em ", strftime("%d/%m/%Y %H:%M:%S", gmtime())
    try:

      br.open(url)

      # Para abrir o primeiro formulário, você pode selecionar com: #0
      br.select_form(nr=0)

      # Preencher o formulário com os dados de login
      br.form['email'] = email
      br.form['password'] = senha

      # Enviar o formulário usando o método HTTP POST
      br.submit()

      html = br.response().read()
      link = br.find_link(text_regex=re.compile("Collect daily"),nr=0)
      br.follow_link(link)
  
    except:

      print "Link não encontrado! Tentando novamente em", tempo_atraso ,"minutos."
      sleep(tempo_atraso*60)


if __name__ == '__main__':
  gokano_bot()