from bs4 import BeautifulSoup
import requests


def get_links(url, channel_type):
    url = url+'/items'
    count = 0
    result = []
    while get_channels(get_page(count, url, channel_type=channel_type), result) != []:
        count += 1
    return result


def get_page(page, url, channel_type):
    form = {'_tgstat_csrk': "fRfa5hrOcvyqGDsDu-0EccaaMtSrSW2b6xcPJpz5Qo9LVIKOLvY5v8JidDbo1FMrj-xYptgzAOjeIH9u77UY9Q==",
            'peer_type': channel_type,
            'sort_channel': "members",
            'sort_chat': "members",
            'page': str(page),
            'offset': "0",
            }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
    }
    response = requests.post(url, headers=headers, data=form)
    response.encoding = 'utf-8'
    print(response)
    return response


def get_channels(response, result):
    stop_marker = []
    soup = BeautifulSoup(response.text, features="html.parser")
    date = soup.find_all(
        "div", class_="card card-body py-2 mb-2 mb-sm-3 border border-info-hover position-relative")

    for links in date:
        link = links.find('a').get('href').replace(
            'https://tgstat.ru/channel/', '').replace('https://tgstat.ru/chat/', '')
        result.append(link)
        stop_marker.append(link)
    return stop_marker


def main():
    print(len(get_links(
        url="https://tgstat.ru/ratings/chats/marketing?sort=mau", channel_type="chat")))


if __name__ == "__main__":
    main()
