#!/usr/bin/env python3

import pyperclip
from colorama import Fore
import os
import getpass
import openai
import time
import threading
import readline


readline.parse_and_bind('tab: complete')
log = []
key = ''
currently_copied_content = ''
wait_bool = False

def test_key():
    global log
    global key
    global wait_bool
    print('[' + Fore.BLUE + '*' + Fore.RESET + '] Testing connection/api key...')
    try:
        question = 'Hello!'
        openai.api_key = key
        wait_bool = True
        loading_thread = threading.Thread(target=loading, args=(), daemon=True)
        loading_thread.start()
        log, response = chat_func(question,'')
        wait_bool = False
        loading_thread.join()
        print('[' + Fore.GREEN + '+' + Fore.RESET + '] Success!                  ')
        print('[' + Fore.GREEN + '+' + Fore.RESET + '] Type ' + Fore.GREEN + 'menu' + Fore.RESET + ' for command help.')
        print("")
        print('[' + Fore.CYAN + '+' + Fore.RESET + ']' + Fore.BLUE + ' ChatGPT' + Fore.RESET + ': ' + response)
        print('')
    except openai.error.AuthenticationError:
        wait_bool = False
        loading_thread.join()
        print('[' + Fore.RED + '-' + Fore.RESET + '] Invalid api key! Please insert a new one.')
        set_key()
    except Exception as e:
        wait_bool = False
        loading_thread.join()
        print('[' + Fore.RED + '-' + Fore.RESET + '] Error: ' + str(e))
    

def set_key():
    global key
    key = getpass.getpass('key > ')
    with open('api_key','w') as writer:
        writer.write(key)
    test_key()
    #return key

def get_key():
    global key
    print('[' + Fore.BLUE + '*' + Fore.RESET + '] Checking if api key is setted...')
    if os.path.isfile('./api_key'):
        with open('api_key','r') as reader:
            key = reader.readline()
            if not key:
                print('[' + Fore.RED + '-' + Fore.RESET + '] Api key not found! Please insert one.')
                set_key()
            else:
                print('[' + Fore.GREEN + '+' + Fore.RESET + '] Found an api key!')
        #return key
        test_key()
    else:
        print('[' + Fore.RED + '-' + Fore.RESET + '] Api key not found! Please insert one.')
        set_key()

def chat_func(question, log):
    question = f'Human: {question}\nAI:'
    model_engine = "text-davinci-003"
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=question,
        temperature=0.7,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Human: "]
    )
    response = f'{completion["choices"][0]["text"]}'
    log += f'{question}{response}'
    return log, response

def get_clipboard():
    while True:
        time.sleep(2)
        global currently_copied_content
        currently_copied_content = pyperclip.paste()

def loading():
    time_sleep = 0.1
    global wait_bool
    while wait_bool:
        print('[' + Fore.CYAN + '\\' + Fore.RESET + ']' + Fore.BLUE + ' ChatGPT' + Fore.RESET + ' is loading (~^w^)~', end='\r')
        time.sleep(time_sleep)
        print('[' + Fore.BLUE + '|' + Fore.RESET + ']' + Fore.BLUE + ' ChatGPT' + Fore.RESET + ' is loading (~^.^)~', end='\r')
        time.sleep(time_sleep)
        print('[' + Fore.RED + '/' + Fore.RESET + ']' + Fore.BLUE + ' ChatGPT' + Fore.RESET + ' is loading (~^.^)~', end='\r')
        time.sleep(time_sleep)
        print('[' + Fore.GREEN + '-' + Fore.RESET + ']' + Fore.BLUE + ' ChatGPT' + Fore.RESET + ' is loading (~^w^)~', end='\r')
        time.sleep(time_sleep)

def main():
    global log
    global key
    global wait_bool
    global currently_copied_content
    exit_bool = False
    get_key()
    openai.api_key = key
    clipboard_thread = threading.Thread(target=get_clipboard, args=(), daemon=True)
    clipboard_thread.start()
    while True:
        #currently_copied_content = pyperclip.paste()
        question = input('[' + Fore.GREEN + '+' + Fore.RESET + '] ' + Fore.GREEN + getpass.getuser() + Fore.RESET + ': ')
        if question == 'exit':
            exit_bool = True
        if question == 'menu':
            print('[' + Fore.GREEN + '+' + Fore.RESET + '] menu     -->     open this help page.')
            print('[' + Fore.GREEN + '+' + Fore.RESET + '] exit     -->     quit application.')
            print('[' + Fore.GREEN + '+' + Fore.RESET + '] $paste   -->     type in question to paste the clipboard.')
            print("")
        else:
            wait_bool = True
            loading_thread = threading.Thread(target=loading, args=(), daemon=True)
            loading_thread.start()
            if '$paste' in question:
                question = question.replace('$paste', currently_copied_content)
            try:
                log, response = chat_func(question,log)
                wait_bool = False
                loading_thread.join()
                print("                              ", end="\r")
                print('[' + Fore.CYAN + '+' + Fore.RESET + ']' + Fore.BLUE + ' ChatGPT' + Fore.RESET + ': ' + response)
                print("")
                if exit_bool:
                    print('[' + Fore.GREEN + '+' + Fore.RESET + '] Bye!' + Fore.CYAN + ' (~^-^)~ ')
                    return
            except openai.error.AuthenticationError:
                wait_bool = False
                loading_thread.join()
                print('[' + Fore.RED + '-' + Fore.RESET + '] Invalid api key! Please insert a new one.')
                set_key()
            except Exception as e:
                wait_bool = False
                loading_thread.join()
                print('[' + Fore.RED + '-' + Fore.RESET + '] Error: ' + str(e))
                print('')


if __name__ == "__main__":
    print(' ________            __                       ______   _______   ________ ')
    print('/        |          /  |                     /      \ /       \ /        |')
    print(Fore.YELLOW + '$$$$$$$$' + Fore.RESET + '/   ______  ' + Fore.YELLOW + '$$' + Fore.RESET + ' |  ______    ______  /' + Fore.YELLOW + '$$$$$$  ' + Fore.YELLOW + '|' + Fore.YELLOW + '$$$$$$$  '+ Fore.RESET + '|' + Fore.YELLOW + '$$$$$$$$' + Fore.RESET + '/ ')
    print(Fore.YELLOW + '$$ ' + Fore.RESET + '|__     /      \ ' + Fore.YELLOW + '$$ ' + Fore.RESET + '| /      \  /      \ ' + Fore.YELLOW + '$$ ' + Fore.RESET + '| _' + Fore.YELLOW + '$$' + Fore.RESET + '/ ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|__' + Fore.YELLOW + '$$ ' + Fore.RESET + '|   ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|   ')
    print(Fore.YELLOW + '$$    ' + Fore.RESET + '|   /' + Fore.YELLOW + '$$$$$$  ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '|/' + Fore.YELLOW + '$$$$$$  ' + Fore.RESET + '| ' + Fore.YELLOW + '$$$$$$  ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '|/    |' + Fore.YELLOW + '$$    $$' + Fore.RESET + '/    ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|   ')
    print(Fore.YELLOW + '$$$$$' + Fore.RESET + '/    ' + Fore.YELLOW + '$$    $$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '|  ' + Fore.YELLOW + '$$ ' + Fore.RESET + '| /    ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$$$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$$$$$$' + Fore.RESET + '/     ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|   ')
    print(Fore.YELLOW + '$$ ' + Fore.RESET + '|      ' + Fore.YELLOW + '$$$$$$$$' + Fore.RESET + '/ ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '|__' + Fore.YELLOW + '$$ ' + Fore.RESET + '|/' + Fore.YELLOW + '$$$$$$$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '\__' + Fore.YELLOW + '$$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '|         ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|   ')
    print(Fore.YELLOW + '$$ ' + Fore.RESET + '|      ' + Fore.YELLOW + '$$       ' + Fore.RESET + '|' + Fore.YELLOW + '$$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$    $$' + Fore.RESET + '/ ' + Fore.YELLOW + '$$    $$ ' + Fore.RESET + '|' + Fore.YELLOW + '$$    $$' + Fore.RESET + '/ ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|         ' + Fore.YELLOW + '$$ ' + Fore.RESET + '|   ')
    print(Fore.YELLOW + '$$' + Fore.RESET + '/        ' + Fore.YELLOW + '$$$$$$$' + Fore.RESET + '/ ' + Fore.YELLOW + '$$' + Fore.RESET + '/ ' + Fore.YELLOW + '$$$$$$$' + Fore.RESET + '/   ' + Fore.YELLOW + '$$$$$$$' + Fore.RESET + '/  ' + Fore.YELLOW + '$$$$$$' + Fore.RESET + '/  ' + Fore.YELLOW + '$$' + Fore.RESET + '/          ' + Fore.YELLOW + '$$' + Fore.RESET + '/    ')
    print(Fore.YELLOW + '                        $$ ' + Fore.RESET + '|                                              ')
    print(Fore.YELLOW + '                        $$ ' + Fore.RESET + '|                                              ')
    print(Fore.YELLOW + '                        $$' + Fore.RESET + '/                                               ')
    print('--------------------------------------------------------------------------')
    print('                        Made by Felpa!' + Fore.CYAN + ' (~^w^)~' + Fore.RESET)
    print('--------------------------------------------------------------------------')
    print('')
    main()
