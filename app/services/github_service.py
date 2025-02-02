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
            description
            createdAt
            updatedAt
            primaryLanguage {
              name
            }
            languages(first: 5) {
              nodes {
                name
              }
            }
            repositoryTopics(first: 5) {
              nodes {
                topic {
                  name
                }
              }
            }
            readme: object(expression: "HEAD:README.md") {
              ... on Blob {
                text
              }
            }
          }
        }
      }
    }
    """ % org

    headers = {"Authorization": f"Bearer {Config.GITHUB_TOKEN}"}
    response = requests.post(Config.GITHUB_API_URL, json={'query': query}, headers=headers)

    print("GitHub API Response:", response.status_code, response.text)  # Debugging line

    try:
        response_json = response.json()
        if "data" in response_json and response_json["data"].get("organization"):
            return response_json["data"]["organization"]["repositories"]["nodes"]
        else:
            return {"error": "Unexpected API response format", "response": response_json}
    except Exception as e:
        return {"error": str(e), "response": response.text}
