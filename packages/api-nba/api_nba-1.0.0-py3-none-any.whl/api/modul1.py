import data as data
import requests


def parse_players(page, per_page):

    params = {
        "page" : page,
        "per_page" : per_page
    }

    json_response = send_api_request(params)
    players = json_response['data']
    player_list = []


    for player in players:
        player_info = {}

        player_info['player_id'] = player['id']
        player_info['first_name'] = player['first_name']
        player_info['last_name'] = player['last_name']
        player_info['position'] = player['position']

        team_info = player['team']
        player_info['team_id'] = team_info['id']
        player_info['team_abbreviation'] = team_info['abbreviation']
        player_info['team_city'] = team_info['city']
        player_info['team_conference'] = team_info['conference']
        player_info['team_division'] = team_info['division']
        player_info['team_full_name'] = team_info['full_name']
        player_info['team_name'] = team_info['name']

        player_info['weight_pounds'] = player['weight_pounds']
        player_info['height_feet'] = player['height_feet']
        player_info['height_inches'] = player['height_inches']

        player_list.append(player_info)

    return player_list

def send_api_request(querystring):

	url = "https://free-nba.p.rapidapi.com/players"


	headers = {
		"X-RapidAPI-Key": "532dfe47d7msh4f9cf6b2b7ba3f7p128602jsnf5e7f94c2cef",
		"X-RapidAPI-Host": "free-nba.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)

	return response.json()

