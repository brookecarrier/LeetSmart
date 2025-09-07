import requests

def get_solved_stats(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userProfile($username: String!) {
      matchedUser(username: $username) {
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    variables = {"username": username}
    headers = {"Content-Type": "application/json", "User-Agent": "LeetSmartBot/1.0"}

    response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
    if response.status_code != 200:
        raise Exception(f"GraphQL query failed with status code {response.status_code}")

    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL error: {data['errors']}")

    user = data["data"]["matchedUser"]
    if not user:
        raise Exception("User not found")

    stats = user["submitStats"]["acSubmissionNum"]
    difficulty_counts = {item["difficulty"]: item["count"] for item in stats if item["difficulty"] != "All"}

    return {
        "easy": difficulty_counts.get("Easy", 0),
        "medium": difficulty_counts.get("Medium", 0),
        "hard": difficulty_counts.get("Hard", 0)
    }
