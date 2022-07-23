from tkinter import *
from easygui import *


global chat
global text
global wid
global enter
global out

chat = Tk()
wid = 907//100


#libraries for chat bot
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#Downloading the article
article=Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521?p=1')
article.download()
article.parse()
article.nlp()
corpus=article.text


#Converting the entire matter in the article into sentences(tokens)
text = corpus
sentence_list = nltk.sent_tokenize(text)


#default function for greetings responses
def greeting_response(text):
  text=text.lower()

  bot_greetings = ['hi','hey','hello','hola']
  user_greetings=['hi','hey','hello','hola','greetings','wassup']

  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)



#index sorting
def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))
  x=list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]]> x[list_index[j]]:
        temp = list_index[i]
        list_index[i]=list_index[j]
        list_index[j]=temp
  return list_index


#Bot response
def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response=''
  cm = CountVectorizer().fit_transform(sentence_list)
  similarity_scores = cosine_similarity(cm[-1],cm)
  similarity_scores_list = similarity_scores.flatten()
  index = index_sort(similarity_scores_list)
  index  = index[1:]
  response_flag = 0
  j=0
  for i in range(len(index)):
    if similarity_scores_list[index[i]]>0.0:
      bot_response = bot_response+' '+sentence_list[index[i]]
      response_flag = 1
      j = j+1
    if j > 2:
      break
    
    if response_flag == 0:
      bot_response = bot_response+"Sorry, I don't understand."
    sentence_list.remove(user_input)
    return bot_response

def output_cal(user_input):
    if greeting_response(user_input) != None:
        bot_output('Doc Bot  : '+greeting_response(user_input))
    else:
        bot_output('Doc Bot  : '+bot_response(user_input))

def proceed():
    text.configure(state=NORMAL,font=(10))
    text.insert(INSERT,"----------------------------------------------\n\nUser      : ")
    text.configure(font=(5))
    text.insert(INSERT,inp.get())
    text.insert(INSERT,"\n")
    if(inp.get() == "cls" or inp.get() == "clear"):
      text.delete("1.0","end")
    else:
      output_cal(inp.get())
    text.configure(state=DISABLED)
    inp.delete(0,END)

def entering(event):
    text.configure(state=NORMAL,font=(10))
    text.insert(INSERT,"User      : ")
    text.configure(font=(5))
    text.insert(INSERT,inp.get())
    text.insert(INSERT,"\n")
    if(inp.get() == "cls" or inp.get() == "clear"):
      text.delete("1.0","end")
    else:
      output_cal(inp.get())
    text.configure(state=DISABLED)
    inp.delete(0,END)

def bot_output(text1):
    text.configure(state=NORMAL)
    text.insert(INSERT,text1)
    text.insert(INSERT,"\n\n----------------------------------------------\n")
    text.configure(state=DISABLED)

    
def destroy():
    print("Chat bot is stopped")
    chat.destroy()

def clears():
  text.configure(state=NORMAL)
  text.delete("1.0","end")
  text.configure(state=DISABLED)

bottom = Frame(chat)
bottom.pack(side=BOTTOM,fill='x')

chat.title("CHAT BOT")
chat.geometry("907x550")
chat.attributes('-topmost',True)

Label(chat, text='A I   C H A T B O T   🤖',font=("Arial",15),anchor='n').pack(fill='both',padx=20,pady=20)
inp = Entry(chat,font=("Arial",18),bg="lightgrey")
inp.pack(fill='x',in_=bottom,side=BOTTOM,padx=20,pady=20,ipadx=5,ipady=5)



text = Text(chat)
text.configure(state=DISABLED)

scrollbar = Scrollbar(chat)
scrollbar.config(command=text.yview)
scrollbar.pack( side=RIGHT, fill=Y)

text.config(yscrollcommand=scrollbar.set)
text.configure(font=(3))
text.pack( side=LEFT, fill=BOTH, expand=True,padx=10,pady=10)


bot_output('Doc Bot  : I am Doctor Bot for short. I will answer your queries about Chronic Kidney Disease. If you want to exit, type bye.')
enter = Button(chat,text="ENTER",command=proceed,font=("Arial",13),borderwidth=1,bg="cyan",activebackground="blue",width=wid)
enter.pack(fill='x',in_=bottom,side=RIGHT,padx=20,pady=2,ipadx=5,ipady=5)

clear = Button(chat,text="CLEAR",command=clears,font=("Arial",13),borderwidth=1,bg="cyan",activebackground="blue",width=wid)
clear.pack(fill='x',in_=bottom,side=RIGHT,padx=20,pady=2,ipadx=5,ipady=5)

out = Button(chat,text="EXIT",command=destroy,font=("Arial",13),borderwidth=1,bg="cyan",activebackground="blue",width=wid)
out.pack(fill='x',in_=bottom,side=RIGHT,padx=20,pady=2,ipadx=5,ipady=5)

chat.bind('<Return>',entering)


def window(event):
    global wid
    wid = chat.winfo_width()
    enter.config(width = wid//30)
    clear.config(width = wid//30)
    out.config(width = wid//30)



chat.bind("<Configure>", window)

print("Chat bot is running")
chat.mainloop()
