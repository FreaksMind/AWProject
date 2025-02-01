# services/github_service.py
import requests
from config import Config

def fetch_repos(org):
    query = """
    {
      organization(login: "%s") {
        repositories(first: 5) {
          nodes {
            name
            url
            languages(first: 5) {
              nodes {
                name
              }
            }
          }
        }
      }
    }
    """ % org

    headers = {"Authorization": f"Bearer {Config.GITHUB_TOKEN}"}
    response = requests.post(Config.GITHUB_API_URL, json={'query': query}, headers=headers)
    return response.json()
