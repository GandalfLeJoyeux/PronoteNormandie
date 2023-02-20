from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pushbullet import Pushbullet
from selenium import webdriver
from typing import Text
import time


note1 = ["Matière et Date", "Note élève", "Coefficient", "Moyenne générale"]
dict1 = {}

# Ouvre le login.txt et ajoute chaque ligne dans une liste
with open('login.txt', 'r') as fichier:
    identifiant = []
    for i in range(3):
        ligne = fichier.readline().strip()
        identifiant.append(ligne)

pb = Pushbullet(identifiant[2])

# Options Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # En option si vous souhaitez désactiver les logs selenium.
chrome_prefs = {}
driver = webdriver.Chrome(options=chrome_options)

# Lance chrome sur la page de connexion educonnect.
driver.get("https://educonnect.education.gouv.fr/idp/profile/SAML2/Unsolicited/SSO?providerId=https%3A%2F%2Fent.l-educdenormandie.fr%2Fauth%2Fsaml%2Fmetadata%2Fidp.xml")

# On repère le bouton Elève et on clique dessus.
driver.find_element_by_id("bouton_eleve").click()

# Renseignement des identifiants.
username2 = driver.find_element_by_id("username")
username2.send_keys(identifiant[0])
password2 = driver.find_element_by_id("password")
password2.send_keys(identifiant[1])
connect = driver.find_element_by_id("bouton_valider")
connect.click()

# Nous voila connecté à l'ENT, on ouvre pronote et on attend que tout charge.
driver.get("https://0760095r.index-education.net/pronote/")
time.sleep(5)

# Une fois pronote chargé on clique sur l'onglet "Notes" et on attend que ça charge.
driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[3]/div[1]/div[3]/ul/li[3]/div[1]").click()
time.sleep(3)

# On récupère la moyenne générale.
note1[3] = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/table/tbody/tr/td[1]/div/div/div[2]/div[1]/div[2]/div/div/div[1]/span/span").text

# Et on trie les notes par ordre chronologique.
chrono = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[1]/div/div[5]/div[2]/label[2]").click() 
time.sleep(2)

# Enfin on récupère les 16 dernières notes avec leurs informations ("Matière et Date", "Note élève", "Coefficient").
nbnote=0
for i in range(16):
   try:
      clicknote = driver.find_element_by_id("GInterface.Instances[2].Instances[1]_1_"+ str(nbnote) +"").click()
      time.sleep(0.2)
      try:
         note1[0] = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/table/tbody/tr/td[2]/div/div/div[1]/div/span").text
         note1[1] = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td[2]").text
         note1[2] = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div/table/tbody/tr[2]/td[2]/div").text
      except:
         note1[0] = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/table/tbody/tr/td[2]/div/div/div[1]/div/span").text
         note1[1] = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]").text
         note1[2] = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/table/tbody/tr/td[2]/div/div/div[2]/div/table/tbody/tr/td[2]/div/label").text

      dict1["note"+str(nbnote)] = list(note1)
      nbnote = nbnote+1

   except:
      pass
   
# On lit les anciennes notes, si le fichier est vide alors toutes les notes seront considéré comme nouvelles.
try:
    dict2 = eval(open("note.txt",'r', encoding="utf-8").read())
except:
    dict2 = {'note0': ['', '', '', '']}
    pass

# Comparaison de chaque nouvelle note (dict1) avec chaque ancienne note (dict2), si une nouvelle note (dict1) ne figure pas parmis les 16 dernières (dict2) alors envoyer une notif.
for new in dict1: 
    i=0
    for old in dict2:
        if dict2[old][0:3]==dict1[new][0:3]:
            pass
        else:
            i+=1
            pass
        if i == len(dict2):
            pb.push_note(dict1[new][0], "Ta note est de " + dict1[new][1] + " " + dict1[new][2] + " ta moyenne est maintenant de " + dict1[new][3])
            pass
        else:
            pass
        
#Remplace les anciennes notes par les nouvelles.
open("note.txt",'w', encoding="utf-8").write(str(dict1))
driver.close()
# FIN