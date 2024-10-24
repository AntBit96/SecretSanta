import random
import pandas as pd

df= pd.read_csv('Jakala_Secret_Santa.csv', sep=',')
associazioni_forzate=[['rosanna.pannozzo@jakala.com',	'rocco.oliva@jakala.com'],
    ['rocco.oliva@jakala.com',	'rosanna.pannozzo@jakala.com'],
    ['antonella.vassallo@jakala.com',	'davide.ciliberto@jakala.com'],
    ['davide.ciliberto@jakala.com',	'antonella.vassallo@jakala.com'],
    ['daniele.mauro@jakala.com',	'andrea.vitali@jakala.com'],
    ['andrea.vitali@jakala.com',	'daniele.mauro@jakala.com'],
    ['ezio.dellirocili@jakala.com',	'gennaro.oriolo@jakala.com'],
    ['gennaro.oriolo@jakala.com',	'ezio.dellirocili@jakala.com'],
    ['irene.cutrona@jakala.com',	'gennaro.oriolo@jakala.com'],
    ['gennaro.oriolo@jakala.com',	'irene.cutrona@jakala.com']]

df = df[~df['Email'].isin([i[0] for i in associazioni_forzate])]
l=df['Email'].tolist()

l2 = l.copy()
aux=True
while aux:
    random.shuffle(l2)
    for i in range(len(l)):
        if l[i]==l2[i]: break
        elif i==len(l)-1: aux=False
#f= open("SecretSantaAssociazioni.csv",'w')
# f.write(f'"regala","riceve","regala_nome","regala_cognome","riceve_nome","riceve_cognome"\n')
# for i in range(len(l)):
#     f.write(f'"{l[i]}","{l2[i]}"\n')  
# f.close()
l3=[]

for i in range(len(l)):
    if l[i] not in [i[0] for i in associazioni_forzate]:
        regala_nome = l[i].split('.')[0].capitalize()
        regala_cognome = l[i].split('.')[1].split('@')[0].capitalize()
        riceve_nome = l2[i].split('.')[0].capitalize()
        riceve_cognome = l2[i].split('.')[1].split('@')[0].capitalize()
        messaggio = f"Ciao {regala_nome},\nabbiamo appena terminato il sorteggio per il Secret Santa🎅siamo contenti che tu abbia deciso di partecipare!\nDovrai fare un regalo a {riceve_nome} {riceve_cognome}, cerca di rispettare il budget da 1-10€ il pensiero è quello che basta 😉\nBuon divertimento!"
        l3.append([l[i],l2[i],regala_nome,regala_cognome,riceve_nome,riceve_cognome,messaggio])
for l in associazioni_forzate:
    regala_nome = l[0].split('.')[0].capitalize()
    regala_cognome = l[0].split('.')[1].split('@')[0].capitalize()
    riceve_nome = l[1].split('.')[0].capitalize()
    riceve_cognome = l[1].split('.')[1].split('@')[0].capitalize()
    messaggio = f"Ciao {regala_nome},\nabbiamo appena terminato il sorteggio per il Secret Santa🎅!\nDovrai fare un regalo a {riceve_nome} {riceve_cognome}, cerca di rispettare il budget da 1-10€ il pensiero è quello che basta 😉\nBuon divertimento!"
    l3.append([l[0],l[1],regala_nome,regala_cognome,riceve_nome,riceve_cognome,messaggio])

df= pd.DataFrame(l3, columns=["regala","riceve","regala_nome","regala_cognome","riceve_nome","riceve_cognome","messaggio"])
print(df)
df.to_excel('SecretSantaAssociazioni.xlsx')