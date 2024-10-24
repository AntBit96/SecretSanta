import random
import pandas as pd
from send_mail import send_mail
df= pd.read_csv('Jakala_Secret_Santa.csv', sep=',')

l=df['Email'].tolist()

l2 = l.copy()
aux=True
while aux:
    random.shuffle(l2)
    for i in range(len(l)):
        if l[i]==l2[i]: break
        elif i==len(l)-1: aux=False
l3=[]

for i in range(len(l)):
    if l[i] not in [i[0] for i in associazioni_forzate]:
        regala_nome = l[i].split('.')[0].capitalize()
        regala_cognome = l[i].split('.')[1].split('@')[0].capitalize()
        riceve_nome = l2[i].split('.')[0].capitalize()
        riceve_cognome = l2[i].split('.')[1].split('@')[0].capitalize()
        #messaggio = f"Ciao {regala_nome},\nabbiamo appena terminato il sorteggio per il Secret Santa🎅siamo contenti che tu abbia deciso di partecipare!\nDovrai fare un regalo a {riceve_nome} {riceve_cognome}, cerca di rispettare il budget da 1-10€ il pensiero è quello che basta 😉\nBuon divertimento!"
        l3.append({
            "regala_mail":l[i],
            "riceve_mail":l2[i],
            "regala_nome":regala_nome,
            "regala_cognome":regala_cognome,
            "riceve_nome":riceve_nome,
            "riceve_cognome":riceve_cognome
        })


for i in l3:
    send_mail(i)