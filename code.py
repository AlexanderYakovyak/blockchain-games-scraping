import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


#Function to form a dict with all needed information about game
def game_info(game):
    game_info = {}

    td_s = game.find_all('td')
        
    main_info = td_s[1].find('a')
    
    link = main_info['href']
    game_info['Url'] = link
    text = main_info.get_text().strip().split('\n')
    
    name = text[0]
    game_info['Name'] = name 
    description = text[1]
    game_info['Description'] = description 
    genres = td_s[2].find_all('a')
    
    genres =  [genres[i].get_text() for i in range(len(genres))]
    genres = '\n'.join(genres)
    game_info['Genres'] = genres
    
    blockchain = td_s[3].find('a')['title']
    game_info['Blockchain'] = blockchain
    
    devices = td_s[4].find_all('a')
    
    device = [devices[i]['title'] for i in range(len(devices))]
    device = '\n'.join(device)
    game_info['Device'] = device
    
    status = td_s[5].find('a').get_text()
    game_info['Status'] = status
    
    nft_support = td_s[6].find('a').get_text()
    game_info['Nft support'] = nft_support
    
    return game_info

def webpage_handle(webpage_url):
    #Local variable to store dicts with info about each game
    block_games = []
    
    response = requests.get(wabpage_url)
    webpage_html = bs(response.content,'html.parser')
    
    #Table with info about all games
    table = webpage_html.find('table',{'class':'table table-bordered mainlist'})
    
    #Grabbing info about first 50 blockchain games, excluding sponsors
    trs = table.find_all('tr')[2:]
    
    for tr in trs:
        info = game_info(tr) 
        
        #Convert dict to pandas DataFrame and add it to local list 
        block_games.append(pd.DataFrame([info]))
    
    return block_games
    
    
    
    


#URLs of first two pages with top 100 blockhain games
wabpages_urls = ['https://playtoearn.net/blockchaingames',
                 'https://playtoearn.net/blockchaingames?sort=score.totalscore&direction=desc&page=2']

#Global variable to store dicts with info about each game
blockchain_games = []

#Going  all webpages and grabbing info 
for wabpage_url in wabpages_urls:
    print(wabpage_url)
    blockchain_games += webpage_handle(wabpage_url)

#Concatenating all DataFarmes to one 
games_df = pd.concat(blockchain_games)
games_df.reset_index(drop=True,inplace=True)

#Saving DF to excel file
games_df.to_excel('blockchain_games.xlsx',index=False)



