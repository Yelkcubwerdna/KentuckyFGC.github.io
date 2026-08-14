from ast import And
from graphqlclient import GraphQLClient
import json
import csv
import datetime

phaseID = '1171339'
tournamentName = "capcom-pro-tour-2022-france-spain-portugal"
#eventId = input("Enter event ID: ")
authToken = 'blank'

with open("startggAuthToken.txt") as f:
    authToken = f.read()
    f.close()

apiVersion = 'alpha'
pageNumber = 1
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0"
}

client = GraphQLClient(endpoint='https://api.start.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)

tournamentList = list()

def tournamentSearch(pageNumber):
    tournamentQuery = client.execute('''
    query Tournaments($page: Int!, $perPage: Int!, $addrState: String!, $upcoming: Boolean!){
        tournaments(query: {
            page: $page
            perPage: $perPage
            filter: {
                addrState: $addrState
                upcoming: $upcoming
                }
            }) {
            nodes {
                id
                addrState
                name
                slug
                startAt
                city
                events{
                    id
                    name
                    videogame {
                        displayName
                        }
                    }
                }
            }
        }
    ''',
    {
        "page": pageNumber,
        "perPage": 50,
        "addrState": "KY",
        "upcoming": True
    })

    return tournamentQuery

def monthName(m):
    match m:
        case 1:
            return "January"
        case 2:
            return "February"
        case 3:
            return "March"
        case 4:
            return "April"
        case 5:
            return "May"
        case 6:
            return "June"
        case 7:
            return "July"
        case 8:
            return "August"
        case 9:
            return "September"
        case 10:
            return "October"
        case 11:
            return "November"
        case 12:
            return "December"

def dayPretty(d):
    ones = d % 10
    
    match ones:
        case 1:
            return f"{d}st"
        case 2:
            return f"{d}nd"
        case 3:
            return f"{d}rd"
        case _:
            return f"{d}th"

            

pageNumber = 1
tournamentData = json.loads(tournamentSearch(pageNumber))
tournaments = tournamentData["data"]["tournaments"]["nodes"]
codeBlock = ""

for i in range(0, len(tournaments)):
    tourney = tournaments[i]

    name = tourney["name"]
    url = f"https://start.gg/" + tourney["slug"]
    events = tourney["events"]
    city = tourney["city"]
    startAt = tourney["startAt"]
    date = datetime.datetime.fromtimestamp(startAt)
    dateString = f"{monthName(date.month)} {dayPretty(date.day)}"

    codeBlock += f'''    <a href=\"{url}\" class=\"list-group-item flex-column align-items=start\">
        <div class=\"d-flex w-100 justify-content-between\">
            <h5 class=\"mb-1\">{name}</h5>
            <small>{dateString}</small>
            </div>\n'''

    for e in events:
        eName = e["name"]
        eGame = e["videogame"]["displayName"]
        codeBlock += f'''           <p class=\"mb-1\">{eName} [{eGame}]</p>\n'''

    codeBlock += f'''            <small>{city}</small>
        </a>\n'''
    
with open('indexTemplate.html', 'r') as file:
    data = file.read()
    data = data.replace("<!--EVENTS-->", codeBlock)

with open('index.html', 'w', encoding="utf-8") as wFile:
    wFile.write(data)

file.close()
wFile.close()