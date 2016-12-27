#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
import cookielib
import re
from time import sleep
from daemonize import daemonize
from time import gmtime, strftime

#creates a browser
br = mechanize.Browser()
url = 'http://www.gokano.com'
email = 'xxx@email.com' 
password = 'xxx'   


@daemonize(stdout='gokano_bot_log.txt', stderr='gokano_bot_log.txt')
def gokano_bot():
  
  print "\n\n\nCollecting for "+email+" user:\n"
  while True:

    print "Trying to collect at ", strftime("%Y-%m-%d %H:%M:%S", gmtime())
    try:


      # preparing cookies
      cj = cookielib.LWPCookieJar()
      br.set_cookiejar(cj)

      # browser options
      br.set_handle_equiv(True)
      br.set_handle_gzip(False)
      br.set_handle_redirect(True)
      br.set_handle_referer(True)
      br.set_handle_robots(False)
      br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

      # config the user-agent.
      br.addheaders = [('User-agent', 'Mozilla/5.0 (X11;\
       U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615\
      Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

      #delay time between requests
      delay_time = 60

      br.open(url)

      # Para abrir o primeiro formulário, você pode selecionar com: #0
      br.select_form(nr=0)

      # Preencher o formulário com os dados de login
      br.form['email'] = email
      br.form['password'] = password

      # Enviar o formulário usando o método HTTP POST
      br.submit()

      html = br.response().read()
      link = br.find_link(text_regex=re.compile("Collect daily"),nr=0)
      br.follow_link(link)
      print "Collected!"
  
    except Exception, e:

      print "Couldn't collect. ",str(e)," Trying again in ", delay_time ," minutes."
      sleep(delay_time)


if __name__ == '__main__':
  gokano_bot()