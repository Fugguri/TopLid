links = []
with open("chats.txt", "r") as file:
    for line in file.readlines():
        links.append(line.removeprefix(
            "https://t.me/").removeprefix('https://t.me/joinchat/').replace('\n', "").replace('+', ""))
print(links)
