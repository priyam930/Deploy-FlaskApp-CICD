from flask import Flask, render_template
import requests
import json
from tabulate import tabulate
import os

app = Flask(__name__)

def fetch_cricket_scores():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": "1f8d11bf65msh2cf06770e4e7416p1f618ejsn3e0012f2d887"
    }

    response = requests.get(url, headers=headers)
    matches_data = []

    if response.status_code == 200:
        try:
            data = response.json()
            matches = data['typeMatches'][0]['seriesMatches'][0]['seriesAdWrapper']['matches']

            for match in matches:
                try:
                    match_info = match['matchInfo']
                    team1 = match_info['team1']['teamName']
                    team2 = match_info['team2']['teamName']

                    table = [
                        [f" {match_info['matchDesc']} , {team1} vs {team2}"],
                        ["Series Name", match_info['seriesName']],
                        ["Match Format", match_info['matchFormat']],
                        ["Result", match_info['status']]
                    ]

                    # Add team1 score
                    if 'matchScore' in match and 'team1Score' in match['matchScore']:
                        score1 = match['matchScore']['team1Score']['inngs1']
                        table.append([f"{team1} Score", f"{score1['runs']}/{score1['wickets']} in {score1['overs']} overs"])
                    else:
                        table.append([f"{team1} Score", "Score not available"])

                    # Add team2 score
                    if 'matchScore' in match and 'team2Score' in match['matchScore']:
                        score2 = match['matchScore']['team2Score']['inngs1']
                        table.append([f"{team2} Score", f"{score2['runs']}/{score2['wickets']} in {score2['overs']} overs"])
                    else:
                        table.append([f"{team2} Score", "Score not available"])

                    matches_data.append(tabulate(table, tablefmt="html"))

                except KeyError as e:
                    print(f"Skipping a match due to missing key: {e}")
                except Exception as e:
                    print(f"Unexpected error processing match: {e}")

        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
    else:
        print("Failed to fetch cricket scores. Status code:", response.status_code)

    return matches_data


def fetch_upcoming_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/schedule/v1/international"
    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": "1f8d11bf65msh2cf06770e4e7416p1f618ejsn3e0012f2d887"
    }

    response = requests.get(url, headers=headers)
    upcoming_matches = []

    if response.status_code == 200:
        try:
            data = response.json()
            match_schedules = data.get('matchScheduleMap', [])

            for schedule in match_schedules:
                if 'scheduleAdWrapper' in schedule:
                    date = schedule['scheduleAdWrapper']['date']
                    matches = schedule['scheduleAdWrapper']['matchScheduleList']

                    for match_info in matches:
                        for match in match_info['matchInfo']:
                            description = match['matchDesc']
                            team1 = match['team1']['teamName']
                            team2 = match['team2']['teamName']
                            match_data = {
                                'Date': date,
                                'Description': description,
                                'Teams': f"{team1} vs {team2}"
                            }
                            upcoming_matches.append(match_data)
                else:
                    print("No match schedule found for this entry.")

        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        except KeyError as e:
            print("Key error:", e)
    else:
        print("Failed to fetch upcoming matches. Status code:", response.status_code)

    return upcoming_matches


@app.route('/')
def index():
    cricket_scores = fetch_cricket_scores()
    upcoming_matches = fetch_upcoming_matches()
    return render_template('index.html', cricket_scores=cricket_scores, upcoming_matches=upcoming_matches)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)
