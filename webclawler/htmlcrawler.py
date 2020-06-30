from bs4 import BeautifulSoup
import time
import re
import csv

from selenium import webdriver

with open("data.csv", "w+") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ["Total Turns", "Total Players", "Winner", "Turn Number", "Available Halite", "Ships", "Drop Offs", "Map Size",
         "Seed"])
csvfile.close()

game_ids = ['1715764','1715754','1715651','1715572','1715129','1715063','1714897','1714379','1713274','1716490','1713190'
           ,'1708345','1708249','1707210','1707108','1714126','1708249','1708403','1705406','1703381','1705627','1706912'
           ,'1701005','1702679','1696349','1715129','1715754','1704553','1703371','1701373','1701395','1699306','1699231'
           ,'1699180'] 
urls = ['https://halite.io/play?game_id=' + g_id for g_id in game_ids ]

for x in range(len(urls)):
    driver = webdriver.Chrome()
    driver.get(urls[x])

    # executing javascript
    html = driver.execute_script("return document.documentElement.outerHTML")

    sel_soup = BeautifulSoup(html, 'html.parser')

    player_name_xpath = ['//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/h4/a',
                         '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[2]/div[1]/h4/a',
                         '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[3]/div[1]/h4/a',
                         '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[4]/div[1]/h4/a']

    ships_xpath = ['//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[1]/div[2]/ul/li[1]/span',
                   '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[1]/span',
                   '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[3]/div[2]/ul/li[1]/span',
                   '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[4]/div[2]/ul/li[1]/span']

    dropoffs_xpath = ['//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[1]/div[2]/ul/li[2]/span',
                      '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[2]/span',
                      '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[3]/div[2]/ul/li[2]/span',
                      '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[2]/div/div/div[4]/div[2]/ul/li[2]/span']

    turn_number = 0
    total_turns = 400
    iterations = 0
    data = []

    while turn_number < total_turns:
        row = []
        try:
            seed = driver.find_element_by_xpath(
                '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[1]/ul/li[1]/span[2]').text
            map_size = driver.find_element_by_xpath(
                '//*[@id="halitetv-visualizer"]/div/div/div[2]/div[1]/ul/li[1]/span[1]').text
            total_turns = int(driver.find_element_by_xpath('//*[@id="halitetv-visualizer"]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]').text.replace(" ",""))

            row.append(total_turns)
            winner = driver.find_element_by_xpath(
                '//*[@id="halitetv-visualizer"]/div/div/div[1]/div[1]/div/div[2]/span[1]/a').text.replace(' ','')
            player_cards = driver.find_elements_by_class_name('card-player')
            players = round(len(player_cards) / 2)
            winner_index = 0
            for i in range(players):
                player_name = driver.find_element_by_xpath(player_name_xpath[i]).text
                if str.upper(player_name).replace(" ","") == winner:
                    winner_index = i
                    break
            t_number = driver.find_element_by_xpath('//*[@id="halitetv-visualizer"]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/span').text

            turn_number = int(re.sub("\D", "", t_number))

            halite_available = driver.find_element_by_xpath('//*[@id="halitetv-visualizer"]/div/div/div[2]/div[1]/ul/li[2]/span').text

            row.append(players)
            row.append(player_name)
            row.append(turn_number)
            row.append(halite_available)
            ships = driver.find_element_by_xpath(ships_xpath[winner_index]).text
            row.append(ships)
            dropoffs = driver.find_element_by_xpath(dropoffs_xpath[winner_index]).text
            row.append(dropoffs)
            row.append(map_size)
            row.append(seed)
            # print()
        except:
            pass
        data.append(row)
        time.sleep(2)
    # print(data)

    driver.quit()

    with open("data.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        for d in range(len(data)):
            writer.writerow(data[d])
    csvfile.close()

print("complete")

