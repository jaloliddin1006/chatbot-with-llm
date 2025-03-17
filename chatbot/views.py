import asyncio
import json
import re
import threading
import time

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Thread, Message
from service.chat import chatbot

# Create your views here.
def save_user_message(thread, question, answer):
    Message.objects.create(
        thread=thread,
        question=question,
        answer=answer
    )


def index(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    thread = Thread.objects.filter(is_active=True, session_id=session_key)
    if thread:
        thread = thread.last()
        #
        # messages = client.beta.threads.messages.list(
        #     thread_id=thread.thread_id,
        # )
        #
        messages_list = []
        #
        # for message in reversed(messages.data):
        #     print(f"{message.role.capitalize()}: {message.content[0].text.value}")
        #     messages_list.append({
        #         'role': message.role,
        #         'content': message.content[0].text.value
        #     })
    else:
        messages_list = []

    context = {
        'messages_list': messages_list
    }

    return render(request, 'assistant.html', context)


@csrf_exempt
def get_answer(request):
    if request.method == 'POST':
        session_id = request.session.session_key

        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message')
        if not request.session.session_key:
            request.session.create()

        thread, created = Thread.objects.get_or_create(
            is_active=True,
            session_id=session_id,
            # defaults={'thread_id': client.beta.threads.create().id}
        )

        assistant_response = chatbot.get_response(user_message)
        print(assistant_response)
        threading.Thread(target=save_user_message, args=(thread, user_message, assistant_response)).start()

        return JsonResponse({'response': assistant_response.get("content", "Kechirasiz, javob bera olmadim.")})


def clear_history(request):
    session_key = request.session.session_key
    if session_key:
        # print("############## 22 ", session_key)
        Thread.objects.filter(session_id=session_key, is_active=True).update(is_active=False)
    return redirect('app:dashboard')


def chat_page(request):
    return render(request, 'assistant.html')