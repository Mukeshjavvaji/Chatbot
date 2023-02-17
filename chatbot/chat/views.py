from django.shortcuts import render, redirect
import pickle
import keras
import numpy as np
import json
import tensorflow as tf
import os


# Create your views here.
def get_context(ck):
    file = str(ck) + '.txt'
    path = 'D:/Academics/Sem-8/Project/Chatbot/chatbot/static/logs/' + file
    f = open(path, 'r')
    msgs = []
    for i in f.readlines():
        msgs.append(i.split("-"))
    n = no_of_conversations()
    context = {
        'messages': msgs,
        'conversation': ck,
        'conversations': range(1, int(n)+1)
    }
    return context

def index(request):
    context = get_context(1)
    return render(request, 'index.html', context)

def send(request, ck):
    message = request.POST['messagesent']
    file = str(ck) + '.txt'
    path = 'D:/Academics/Sem-8/Project/Chatbot/chatbot/static/logs/' + file
    f = open(path, 'a')

    model = tf.keras.models.load_model('D:\Academics\Sem-8\Project\Chatbot\chatbot\static\model\chat_model')

    with open("D:\Academics\Sem-8\Project\Chatbot\chatbot\static\data\intents.json") as info:
        data = json.load(info)

    with open('D:/Academics/Sem-8/Project/Chatbot/chatbot/static/model/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    with open('D:\Academics\Sem-8\Project\Chatbot\chatbot\static\model\label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
    
    response = model.predict(keras.utils.pad_sequences(tokenizer.texts_to_sequences([message]), truncating='post', maxlen=20))
    tag = lbl_encoder.inverse_transform([np.argmax(response)])

    for i in data['intents']:
        if i['tag'] == tag:
            reply = np.random.choice(i['responses'])
    
    
    message = message + '\n'
    f.write("R-"+ message)
    if 'http' in reply:
        replies = reply.split("=")
        replies[0] = replies[0] + "\n"
        replies[1] = replies[1] + "\n"
        f.write("L-" + replies[0])
        f.write("B-" + replies[1])
    else:
        reply = reply + "\n"
        f.write("L-" + reply)

    context = get_context(ck)
    response = redirect('/'+str(ck), context)
    return response
    
def display(request, ck):
    n = no_of_conversations()
    if ck> n:
        return redirect('/'+str(n))
    context = get_context(ck)
    return render(request, 'index.html', context)

def no_of_conversations():
    folder = "D:\Academics\Sem-8\Project\Chatbot\chatbot\static\logs"
    file_count = sum(len(files) for _, _, files in os.walk(folder))
    return file_count

def newconvo(request):
    n = no_of_conversations()
    file = str(n+1) + '.txt'
    path = 'D:/Academics/Sem-8/Project/Chatbot/chatbot/static/logs/' + file
    f = open(path, 'w')
    context = get_context(n+1)
    response = redirect('/'+str(n+1), context)
    return response
    
