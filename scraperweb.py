#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

datenow = datetime.datetime.now()

#print(datenow)

content = ""
conteudo = ""
#extrair noticias

def extract_news(url):
	print("Extraindo Noticias...")
	conteudo =""
	conteudo += ("<b>Últimas notícias:</b>\n" + "<br />" +'-' *50 + "<br />")
	resposta = requests.get(url)
	conteudo_main = resposta.content
	soup = BeautifulSoup(conteudo_main,"html.parser")
	for i,tag in enumerate(soup.find_all('td', attrs={'class':'titlelink','valign': ''})):
		conteudo_main += ((str(i+1) +' :: '+ tag.text + "\n"+ '<br />') if tag.text != "More" else " ")
		# print(tag.prettify) #find_all('span', attrs= {'class':'sitestr'})
		conteudo_main = conteudo_main.prettify
	return (conteudo_main)


content = extract_news('https://news.ycombinator.com/')
conteudo += str(content)
conteudo += ("<br />------<br />")
conteudo += ("<br /><br />End of Message")


#Envie nosso email

print("Criando nosso email...")

SERVIDOR = "smtp.gmail.com" 
PORTA = 587
FROM = ""
TO = "" #Pode ser uma lista de emails
PASS = ""

# fp = opend (file_name, 'rb')
# mensagem text/plain
msg = MIMEMultipart()

#msg.add_header("Content-Disposition", "attachment", filename="empty.txt")
msg["Subject"] = "Top noticias do \'Hacker News\' "+ " " + str(datenow.day)  + "-" + str(datenow.month) + "-" + str(datenow.year)
msg["From"] = FROM
msg["To"] = TO
msg.attach(MIMEText(conteudo, "html"))
#fp.close()

print("Iniciando servidor")

servidor = smtplib.SMTP(SERVIDOR, PORTA)
#servidor = smtplib.SMPT_SSL("smtp.gmail.com", 465)
servidor.set_debuglevel(1)
servidor.ehlo()
servidor.starttls()
servidor.login(FROM, PASS)
servidor.sendmail(FROM, TO, msg.as_string())
print("Email enviado")
servidor.quit()
