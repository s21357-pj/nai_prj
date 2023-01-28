import wikipedia
import csv

rows = [["title", "text"]]
net = wikipedia.page("Computer_network")
rows.append([net.title, net.content])
with open('example.csv', 'w') as file:
    writer = csv.writer(file)
    for data in rows:
        writer.writerow(data)
