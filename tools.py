import requests
import random
from spotipy.oauth2 import SpotifyClientCredentials
import bs4
import json
import os



def global_search(query):
    # global final_res, ind_search, res_search, link_search, links, raw_response
    q = '\"' + query + '\"'
    offset = 0
    again = False
    new = None
    token = SpotifyClientCredentials(client_id="8d84e4b31ab44a35ae0e9ca9e96cec3f", client_secret="a07a9133c4b84665ad864f10fc3112e9").get_access_token(as_dict=False, check_cache=False)
    while True:
        if again:
            q = '\"' + input('= ') + '\"'
            new = None
        # print(token)

        # My Search
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        params = {
            'q': q,
            'type': 'track',
            'limit': 5,
            'offset': offset
        }

        try:
            raw_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
        except:
            print('Impossibile raggiungere il servizio, controlla la tua connessione...')
            input('Premi \'Invio\' per chiudere il programma')
            quit()
        # print(raw_response.url)
        response = raw_response.json()
        # print(response)

        if len(response['tracks']['items']) == 0:
            new = input('Non ci sono più risultati, riprovare (vuoto = si, e = exit)?\n')
        if new == 'e':
            print('\nOk, alla prossima!')
            exit()
        elif new == '':
            again = True
            continue

        index = 1
        for sg in response['tracks']['items']:
            artist = sg['artists'][0]['name']
            song = sg['name']
            print(f'{index}) {artist} - {song}')
            index += 1

        # print(res)
        ind = 1
        links = {}
        for link in response['tracks']['items']:
            url = link['external_urls']['spotify']
            links.setdefault(ind, url)
            ind += 1

        # print(ind_search)
        # print(res_search)
        final_res = input('\nQuale canzone (inserisci numero, lasciare vuoto per riprovare, n = next, e = exit)?\n')
        if len(final_res) == 0:
            again = True
            offset = 0
        elif final_res == 'n':
            offset += 5
            again = False
        elif final_res == 'e':
            print('\nOk, alla prossima!')
            quit()
        elif int(final_res) not in range(index):
            print('Numero invalido :(')
            continue
        else:
            break

    link = links[int(final_res)]

    print("\n" + link)
    

def get_common_word():
    url = requests.get("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
    words = url.json()
    # print(len(words))
    random_word = random.choice(words)
    return random_word


def get_a_word():
    url = requests.get("https://raw.githubusercontent.com/words/an-array-of-english-words/master/index.json")
    raw = url.json()
    # print(len(raw))
    word = random.choice(raw)
    return word

def get_settings():
    with open("settings.json", "r") as js:
        settings = json.load(js)
    return settings


inmenu = True
settings = get_settings()
while inmenu:
    options = [
        '\n0) Manage Preferences',
        '1) Random Sample Text',
        '2) Random Color',
        '3) Random Number',
        '4) Search for song',
        '5) Get Website Logo',
        '6) Random Word',
        '7) Random not existing word',
        '8) Print Unicode code for character', 
        '9) Heads or Tails',
        '10) Random Luther\'s insult'
    ]
    for opt in options:
        print(opt)
    
    chosen = int(input("Choose between one the options above: "))

    # PREFERENCES
    if chosen == 0:
        while True:  
            print("These are your current prerences:\n")
            print(json.dumps(settings, indent=4))
            option = input("\nChoose which option to modify (type \"exit\" to go back): ")
            if option == "exit":
                break
            elif option in settings.keys():
                setting = list(settings[option].keys())[0]
                if len(settings[option].keys()) > 1:
                    setting = input("Choose which setting to modify: ")
                    if setting in settings[option].keys():
                        pass
                    else:
                        print("error")
                        quit()

                new = input("New value (specify data type separated by semicolon): ")
                value = new.split(";")[0].strip()
                data_type = new.split(";")[-1].strip()
                data = True
                while data:
                    data = False
                    match data_type:
                        case "int":
                            new_value = int(value)
                        case "str":
                            new_value = str(value)
                        case "bool":
                            new_value = value in ["true", "True"]
                        case _:
                            data_type = type(settings[option][setting]).__name__
                            print(data_type)
                            input()
                            data = True

                    
                settings[option][setting] = new_value

            else:
                print("error")
                quit()
        
        with open("settings.json", "w") as js:
            json.dump(settings, js, indent=4)
            

    # SAMPLE TEXT
    elif chosen == 1:
        # text = requests.get(url='https://baconipsum.com/api/?type=meat-and-filler').json()
        text = "\n".join(requests.get(url=f'https://baconipsum.com/api/?type={settings["Sample Text"]["type"]}').json()) # meat-and-filler or all-meat
        print(text)
        if settings["Sample Text"]["export"]:
            file_name = "sample"
            ind = 0
            while os.path.isfile(f"{file_name}.txt"):
                ind += 1
                file_name = "sample" + str(ind)
            with open(f"{file_name}.txt", "w") as exp_file:
                exp_file.writelines(text)
        
    # RANDOM COLOR
    elif chosen == 2:
        color_json = requests.get(url='https://www.colr.org/json/color/random').json()
        print(f"HEX code: #{color_json['colors'][0]['hex']}\nColor name: {color_json['colors'][0]['tags'][0]['name'].capitalize()}")
    
    # RANDOM NUMBER
    elif chosen == 3:
        print(random.randint(settings["Random Number"]["min"], settings["Random Number"]["max"]))
    
    # SEARCH SONG
    elif chosen == 4:
        global_search(input("Song Name?\n"))
    
    # WEBSITE LOGO
    elif chosen == 5:
        website = input('Website domain?\n')
        img = requests.get(f"https://logo.clearbit.com/{website}?size=512").content
        with open(f'{website.split(".")[0]}.{settings["Website Logo"]["extension"]}', 'wb') as handler:
            handler.write(img)
        print("Saved!")
    
    # RANDOM WORD
    elif chosen == 6:
        simple = input("Would you like a simpler word?\n")
        if simple.lower() == "yes":
            print(f"Your word is: {get_common_word()}")
        else:
            print(f"Your word is: {get_a_word()}")
    
    # NON-EXISTING WORD
    elif chosen == 7:
        html_site = requests.get("https://www.thisworddoesnotexist.com/").text
        soup = bs4.BeautifulSoup(html_site, "html.parser")
        raw_word = soup.find("div", {"id": "definition-word"})
        word = raw_word.text.rstrip().lstrip().split("\n")[0]
        raw_defin = soup.find("div", {"id": "definition-definition"})
        defin = raw_defin.text.rstrip().lstrip().split("\n")[0]
        raw_example = soup.find("div", {"id": "definition-example"})
        example = raw_example.text.rstrip().lstrip().split("\n")[0]
        print(f"\nWord: {word.capitalize()}\nDefinition: {defin.capitalize()}\nExample: {example}")
    
    # UNICODE CODE FOR CHARACTER
    elif chosen == 8:
        char = input("Please input the character for which you would like to know the Unicode code:\n")
        uni_char = ord(char)
        print("U+" + format(uni_char, '04x'))

    # HEADS OR TAILS
    elif chosen == 9:
        print(f'It\'s {random.choice(["Heads", "Tails"])}!')
    
    # RANDOM LUTHER'S INSULT
    elif chosen == 10:
        html_site = requests.get("https://ergofabulous.org/luther/").content
        soup = bs4.BeautifulSoup(html_site, "html.parser")
        insult = soup.find("p", {"class": "larger"}).contents[0]
        print(insult)

