import requests
import json
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import os
import datetime
import random
from colorama import init, Fore, Style
init()

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H.%M.%S")

#eng: if you want to use more than 1 apikey (to speedup the check), write it below. example: apikeys = ['apikey1', 'apikey2']. instead of apikey1 and apikey2 u should write your apikeys
#ru: если вы хотите юзать больше 1 апикея, то запишите его в список, как в примере: apikeys = ['8ED9B****************', 'IFB8D****************']
apikeys = ['']

lock = threading.Lock()

with open('ids.txt', 'r') as total:
    ids = total.read().splitlines()

total_lines = len(ids)

#eng: default number of threads. you can change it
#ru: дефолтное значение процессов, можете изменить его если хотите, но я не рекомендую
threads = 10

#cool ascii art
print(Fore.GREEN + ' @@@@@@    @@@@@@   @@@   @@@@@@@  ')
print('@@@@@@@@  @@@@@@@   @@@  @@@@@@@@  ')
print('@@!  @@@  !@@       @@!  !@@       ')      
print('!@!  @!@  !@!       !@!  !@!       ')
print('@!@!@!@!  !!@@!!    !!@  !@!       ')
print('!!!@!!!!   !!@!!!   !!!  !!!       ')
print('!!:  !!!       !:!  !!:  :!!       ')
print(':!:  !:!      !:!   :!:  :!:       ')
print('::   :::  :::: ::    ::   ::: :::  ')
print(' :   : :  :: : :    :     :: :: :  ')
print(' Advanced Steam ID Checker')
print(' Made by froggert' + '\n' + Style.RESET_ALL) 
print(Fore.LIGHTBLACK_EX + ' Select mode:' + '\n' + Style.RESET_ALL + Fore.LIGHTYELLOW_EX + '1 - default, 50ids/min, no bugs in output' + Style.RESET_ALL + Fore.LIGHTMAGENTA_EX +'\n' + '2 - threads, experimental, faster, 10+ ids/sec' + Style.RESET_ALL)

mode = int(input())
while mode > 2 or mode < 1:
    print(Fore.RED + 'Select a correct mode.' + Style.RESET_ALL)
    mode = int(input())

if mode == 2:
    
    print(Fore.LIGHTGREEN_EX + '\n Selected threads mode.' + Style.RESET_ALL + Fore.RED + '\n NOTE: THIS IS AN EXPERIMENTAL MODE SO EXPECT BUGS IN OUTPUT. \n' + Style.RESET_ALL)
    print(Fore.YELLOW + f'Input number of threads \n 0 to select default threads ({threads})' + Style.RESET_ALL + Fore.LIGHTBLACK_EX + '\n (Its not recommended to use more than 15 threads if you are using 1 apikey) \n' + Style.RESET_ALL)
    selected_threads = int(input())
        
    if selected_threads == 0:
        print(Fore.YELLOW + f'\n Number of threads: {threads}' + Style.RESET_ALL)
        print(Fore.YELLOW + '\n Starting to check your ids in just 1 second...' + Style.RESET_ALL)
        time.sleep(1)
    else:
        threads = selected_threads
        print(Fore.YELLOW + f'\n Number of threads: {threads}' + Style.RESET_ALL)
        print(Fore.YELLOW + '\n Starting to check your ids in just 1 second...' + Style.RESET_ALL)
        time.sleep(1)
    folder_name = f"check_{formatted_datetime}"
    os.makedirs(folder_name)

    free_file_path = os.path.join(folder_name, "free.txt")
    taken_all_file_path = os.path.join(folder_name, "taken_and_lvls_ALL.txt")
    taken_unconfigured_file_path = os.path.join(folder_name, "taken_UNCONFIGURED.txt")
    taken_lvl0_file_path = os.path.join(folder_name, "taken_LVL0.txt")
    def check_id(id, line_number):
        apikey = random.choice(apikeys)
        r = requests.get(f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={apikey}&vanityurl=' + str(id))
        if 'No match' in r.text:
            with lock:
                print(f'{id:<40} is ' + Fore.LIGHTGREEN_EX + 'free ' + Style.RESET_ALL + f'[{line_number}/{total_lines}]')
            with open(free_file_path, 'a', encoding='utf-8') as free:
                free.write(id + '\n')
        else:
            with lock:
                print(f'{id:<40} is ' + Fore.LIGHTRED_EX + 'taken ' + Style.RESET_ALL + f'[{line_number}/{total_lines}]')
            steamid = requests.get(f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={apikey}&vanityurl=' + str(id))
            s = steamid.text
            s = s.replace('"', '')
            s = s.replace('{', '')
            s = s.replace('}', '')
            s = s.replace(':', '')
            s = s.replace('steamid', '')
            s = s.replace('success', '')
            s = s.replace('response', '')
            s = s.replace(',1', '')
            info = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apikey}&steamids=' + str(s))

            try:
                parsed_data = json.loads(info.text)
                response = parsed_data['response']
                players = response['players']

                for player in players:
                    community_visibility_state = player['communityvisibilitystate']
                    profile_state = player.get("profilestate", None)
                    persona_name = player["personaname"]

                    if profile_state == None:
                        profilestate = 'Unconfigured'
                    else:
                        profilestate = 'Configured'

                    if community_visibility_state == 3:
                        communityvisibilitystate = 'Public'
                    else:
                        communityvisibilitystate = 'Private/Friends only'

                    if community_visibility_state == 3:
                        lvl1 = requests.get(f'http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={apikey}&steamid=' + str(s))
                        lvl = lvl1.text
                        lvl = lvl.replace('"', '')
                        lvl = lvl.replace('{', '')
                        lvl = lvl.replace('}', '')
                        lvl = lvl.replace(':', '')
                        lvl = lvl.replace('response', '')
                        lvl = lvl.replace('player_level', '')
                    else:
                        lvl = 'Couldnt get steam lvl'

                    with open(taken_all_file_path, 'a', encoding='utf-8') as taken:
                        taken.write('ID: ' + str(id) + 
                            '\n' + 'Link: ' 'https://steamcommunity.com/id/' + str(id) + 
                            '\n' + 'Nickname: ' + str(persona_name) + 
                            '\n' + 'Profile status: ' + str(profilestate) + 
                            '\n' + 'Visibility: ' + str(communityvisibilitystate) +
                            '\n' + 'Steam LVL: ' + str(lvl) +
                            '\n' + '\n')

                    if profile_state != 1:
                        with open(taken_unconfigured_file_path, 'a', encoding='utf-8') as unconfigured:
                            unconfigured.write('ID: ' + str(id) + 
                                           '\n' + 'Link: ' 'https://steamcommunity.com/id/' + str(id) + 
                                           '\n' + 'Nickname: ' + str(persona_name) + 
                                           '\n' + 'Profile status: ' + str(profilestate) + 
                                           '\n' + 'Visibility: ' + str(communityvisibilitystate) +
                                           '\n' + 'Steam LVL: ' + str(lvl) +
                                           '\n' + '\n')

                    if lvl == 0 or lvl == '0':
                        with open(taken_lvl0_file_path, 'a', encoding='utf-8') as lvl0:
                            lvl0.write('ID: ' + str(id) + 
                                   '\n' + 'Link: ' 'https://steamcommunity.com/id/' + str(id) + 
                                   '\n' + 'Nickname: ' + str(persona_name) + 
                                   '\n' + 'Profile status: ' + str(profilestate) + 
                                   '\n' + 'Visibility: ' + str(communityvisibilitystate) +
                                   '\n' + 'Steam LVL: ' + str(lvl) +
                                   '\n' + '\n')

            except json.JSONDecodeError:
                with lock:
                    print(f'{id:<40}' + Fore.RED + 'API response error ' + Style.RESET_ALL + f'[{line_number}/{total_lines}]')

    start_time = time.time()

    with ThreadPoolExecutor(threads) as executor:
        futures = [executor.submit(check_id, id, line_number) for line_number, id in enumerate(ids, start=1)]

        for future in futures:
            future.result()

    elapsed_time = time.time() - start_time
    elapsed_time = round(elapsed_time, 2)

    print(Fore.LIGHTGREEN_EX + f'Finished checking IDs. Total time: {elapsed_time} seconds' + Style.RESET_ALL)

if mode == 1:
    
    print(Fore.LIGHTYELLOW_EX + ' Mode: default' + Style.RESET_ALL + Fore.LIGHTWHITE_EX + '\n Average speed: 50ids/min' + Style.RESET_ALL + Fore.GREEN + '\n Starting to check your ids in 1 second... \n' + Style.RESET_ALL)
    
    folder_name = f"check_{formatted_datetime}"
    os.makedirs(folder_name)

    free_file_path = os.path.join(folder_name, "free.txt")
    taken_all_file_path = os.path.join(folder_name, "taken_and_lvls_ALL.txt")
    taken_unconfigured_file_path = os.path.join(folder_name, "taken_UNCONFIGURED.txt")
    taken_lvl0_file_path = os.path.join(folder_name, "taken_LVL0.txt")
    
    time.sleep(1)

    current_line = 0
    start_time = time.time()
    with open('ids.txt', 'r', encoding='utf-8') as ids:
        for id in ids:
            apikey = random.choice(apikeys)
            id = id.strip()
            current_line += 1
            r = requests.get(f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={apikey}&vanityurl=' + str(id))
            if 'No match' in r.text:
                print(f'{id:<40} is ' + Fore.LIGHTGREEN_EX + 'free ' + Style.RESET_ALL + f'[{current_line}/{total_lines}]')
                with open(free_file_path, 'a', encoding='utf-8') as free:
                    free.write(id + '\n')
            else:
                print(f'{id:<40} is ' + Fore.LIGHTRED_EX + 'taken ' + Style.RESET_ALL + f'[{current_line}/{total_lines}]')
                steamid = requests.get(f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={apikey}&vanityurl=' + str(id))
                s = steamid.text
                s = s.replace('"', '')
                s = s.replace('{', '')
                s = s.replace('}', '')
                s = s.replace(':', '')
                s = s.replace('steamid', '')
                s = s.replace('success', '')
                s = s.replace('response', '')
                s = s.replace(',1', '')
                info = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apikey}&steamids=' + str(s))
            
                i = info.text
                parsed_data = json.loads(i)
                response = parsed_data['response']
                players = response['players']
            
                for player in players:
                    community_visibility_state = player['communityvisibilitystate']
                    profile_state = player.get("profilestate", None)
                    persona_name = player["personaname"]
                
                    if profile_state == None:
                        profilestate = 'Unconfigured'
                    else:
                        profilestate = 'Configured'
                    
                    if community_visibility_state == 3:
                        communityvisibilitystate = 'Public'
                    else:
                        communityvisibilitystate = 'Private/Friends only'
            
                if community_visibility_state == 3:
                    lvl1 = requests.get(f'http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={apikey}&steamid=' + str(s))
                    lvl = lvl1.text
                    lvl = lvl.replace('"', '')
                    lvl = lvl.replace('{', '')
                    lvl = lvl.replace('}', '')
                    lvl = lvl.replace(':', '')
                    lvl = lvl.replace('response', '')
                    lvl = lvl.replace('player_level', '')
                else:
                    lvl = 'Couldnt get steam lvl'
                    
                with open(taken_all_file_path, 'a', encoding='utf-8') as taken:
                    taken.write('ID: ' + str(id) + 
                            '\n' + 'Link: ' 'https://steamcommunity.com/id/' + str(id) + 
                            '\n' + 'Nickname: ' + str(persona_name) + 
                            '\n' + 'Profile status: ' + str(profilestate) + 
                            '\n' + 'Visibility: ' + str(communityvisibilitystate) +
                            '\n' + 'Steam LVL: ' + str(lvl) +
                            '\n' + '\n')
                
                if profile_state != 1:
                    with open(taken_unconfigured_file_path, 'a', encoding='utf-8') as unconfigured:
                        unconfigured.write('ID: ' + str(id) + 
                            '\n' + 'Link: ' 'https://steamcommunity.com/id/' + str(id) + 
                            '\n' + 'Nickname: ' + str(persona_name) + 
                            '\n' + 'Profile status: ' + str(profilestate) + 
                            '\n' + 'Visibility: ' + str(communityvisibilitystate) +
                            '\n' + 'Steam LVL: ' + str(lvl) +
                            '\n' + '\n')
                    
                if lvl == 0 or lvl == '0':
                    with open(taken_lvl0_file_path, 'a', encoding='utf-8') as lvl0:
                        lvl0.write('ID: ' + str(id) + 
                            '\n' + 'Link: ' 'https://steamcommunity.com/id/' + str(id) + 
                            '\n' + 'Nickname: ' + str(persona_name) + 
                            '\n' + 'Profile status: ' + str(profilestate) + 
                            '\n' + 'Visibility: ' + str(communityvisibilitystate) +
                            '\n' + 'Steam LVL: ' + str(lvl) +
                            '\n' + '\n')
    elapsed_time = time.time() - start_time
    elapsed_time = round(elapsed_time, 2)

    print(Fore.LIGHTGREEN_EX + f'Finished checking IDs. Total time: {elapsed_time} seconds' + Style.RESET_ALL)