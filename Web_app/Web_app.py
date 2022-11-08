from ast import Add
import streamlit as st
from streamlit_chat import message
from agenda import add_new_print 
from answer_query import find_doc_name, find_pages_number
import classifier as cl
import re


st.set_page_config(page_title="Entreprise Imprimenligne & co",layout="centered")


if 'message_history' not in st.session_state:
    st.session_state["message_history"]=["Salut ! Je suis l'ultra bot 3000, je peux imprimer tes documents."]

if 'user_history' not in st.session_state:
    st.session_state["user_history"]=[False]

if 'message_count' not in st.session_state:
    st.session_state["message_count"]=1

if 'agenda' not in st.session_state:
    st.session_state["agenda"]=[[],[],[],[],[],[]]

if 'model' not in st.session_state:
    st.session_state["model"]=cl.import_model("model.pickle")

jour=["lundi","mardi","mercredi",'jeudi',"dimanche"]

with st.sidebar:
    date_str=str(st.date_input("Vous pouvez modifier le jour pour tester l'agenda"))
    # st.write(date_str)
    [y,mois,d]=re.split("-",date_str)
    # st.write([int(y),int(mois),int(d)])

    F=int(d)+ ((13*int(mois)-1)/5) +int(y[2:])*3/4 +-7/4*int(y[:2])
    day_nb=int(((F-2)%7)//1)
    # Zeller's Rule:
    # d is  the day of the month.
    # mois is the month number.
    # y[2:] is the last two digits of the year.
    # y[:2] is the first two digits of the year
    # 0=monday,1=tuesday,...,6=sunday you get it

    # st.write(((F-2)%7)//1)
    time_str = str(st.time_input("Vous pouvez modifier l'heure pour tester l'agenda"))
    [h,m,s]=re.split(":",time_str)
    time_sec=int(h)*3600+int(m)*60+int(s)
    # st.write(time_sec)
    # st.write([int(h),int(m),int(s)])



    # nb_pages=st.number_input('nb_pages:',value=0,step=1)
    # docname=st.text_input('docname:')
    # hour=st.number_input('hour:',value=0,step=1)
    # day=st.number_input('day:',value=0,min_value=0,max_value=6,step=1)
    # update_agenda=st.button("update agenda:")



placeholder = st.empty()  # placeholder for the messages

input_ = st.text_input("you:") # user input
if input_!='':
    st.session_state["message_history"].append(input_)
    st.session_state["user_history"].append(True)


    pred=st.session_state["model"].predict([input_])[0]
    if pred==1:
        nb_p=find_pages_number(input_)
        doc_n=find_doc_name(input_)
        if nb_p!=-1:
            if doc_n!=-1:
                st.write(time_sec)
                [h_print,d_print]=add_new_print(doc_n,int(nb_p),int(time_sec),int(day_nb),st.session_state["agenda"])
                reponse="nous lançons l'impression de "+str(nb_p)+" pages du document "+str(doc_n)+"."+" L'impression commence à "+str(h_print//3600)+"h"+str((h_print%3600)//60)+" "+jour[d_print]+" et durera "+str(int(nb_p)//60+1)+" min."
            else:
                [h_print,d_print]=add_new_print(str(st.session_state["message_count"]),nb_p,time_sec,day_nb,st.session_state["agenda"])
                reponse="nous lançons l'impression de "+str(nb_p)+" pages. L'impression commence à "+str(h_print//3600)+"h"+str((h_print%3600)//60)+" "+jour[d_print]+" et durera "+str(int(nb_p)//60+1)+" min."
        else:
            reponse="désolé je n'ai pas compris votre requête, pour lancer une impression veuillez me donner le nom de votre document ainsi que son nombre de pages"
    else:
        reponse="désolé je n'ai pas compris votre requête, pour lancer une impression veuillez me donner le nom de votre document ainsi que son nombre de pages"


    st.session_state["message_history"].append(reponse)
    st.session_state["user_history"].append(False)


with placeholder.container(): #display all the messages
    for i in range(len(st.session_state["message_history"])):
        message(st.session_state["message_history"][i],is_user=st.session_state["user_history"][i],key=st.session_state["message_count"])
        st.session_state["message_count"]+=1

# if update_agenda:
#     agenda=add_new_print(docname,nb_pages,hour,day,st.session_state["agenda"])
#     if agenda!=-1:
#         st.session_state["agenda"]=agenda



st.session_state["agenda"]


# st.write("lasage")
# model=cl.import_model("../Model/model.pickle")
# pred=model.predict(["j'aime les bananas, imprime 39 pages du document doc1.pdf"])[0]
# nbp=find_pages_number("j'aime les bananas, imprime 39 pages du document doc1.pdf")
# dc_n=find_doc_name("j'aime les bananas, imprime 39 pages du document doc1.pdf")
# st.write(pred,nbp   ,dc_n)












# try:
#     st.session_state["question"]
#     st.write(type(st.session_state["question"]))
#     st.session_state["question"]==''

# except:
#     'question non definie'



# try:
#     j=st.session_state["flag"]
# except:
#     st.session_state["flag"]=True


# chat_box=st.empty()
# left_margin,client,bot,right_margin=chat_box.columns((1,2,2,1))


# if st.session_state["flag"]:
#     question=client.text_input(label="faites votre commande ici")
#     st.session_state["question"]=(question+ '.')[:-1]
#     st.session_state['flag']=False
# else:
#     # client.empty()
#     client.text_input(label="faites votre commande ici",placeholder=st.session_state["question"],disabled=True)

# st.write('''
   
# ''')
# bot.markdown("***")
# bot.text( st.session_state["question"])

