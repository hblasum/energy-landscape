import requests
import sqlite3

my_username = 'hblasum'
my_token = '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'

login = requests.get('https://api.github.com/search/repositories?q=github+api', auth=(my_username,my_token))


def sanitize(input_string):
  return str(input_string).replace('\t', '')


def get_github_stats(url):
  """
  Extracts the number of stars and pull requests for a GitHub repository URL.

  Args:
      url: The URL of the GitHub repository.

  Returns:
      A dictionary containing the number of stars and pull requests, or None
      if the URL is invalid or data cannot be retrieved.
  """
  # Extract username and repo name from the URL
  parts = url.split("/")
  if len(parts) < 4 or parts[2] != "github.com":
    return None

  username, repo_name = parts[3], parts[4]

  # Use the GitHub API to get star count
  star_url = f"https://api.github.com/repos/{username}/{repo_name}"
  response = requests.get(star_url, auth=(my_username,my_token))
  if response.status_code == 200:
    data = response.json()
    stars = data.get("stargazers_count")
  else:
    stars = None


  # Use the GitHub API to get pull request count (indirect approach)
  pull_url = f"https://api.github.com/repos/{username}/{repo_name}/pulls"
  response = requests.get(pull_url, auth=(my_username,my_token))
  if response.status_code == 200:
    # Assuming first page has some pull requests (adjust as needed)
    data = response.json()
    pull_requests = len(data)
  else:
    pull_requests = None

  # Use the GitHub API to get fork count (indirect approach)
  fork_url = f"https://api.github.com/repos/{username}/{repo_name}/forks"
  response = requests.get(fork_url, auth=(my_username,my_token))
  if response.status_code == 200:
    # Assuming first page has some fork requests (adjust as needed)
    data = response.json()
    forks = len(data)
  else:
    forks = None

  return {
    "stars": stars,
    "pull_requests": pull_requests,
    "forks": forks
  }


def print_one(url, data, output):
  stats = get_github_stats(url)
  if stats:
    print(f"{url}\t", end="", file=output)
    print(f"{stats['stars']}\t", end="", file=output)
    print(f"{stats['pull_requests']}\t", end="", file=output)
    print(f"{stats['forks']}\t", end = "", file=output)
    print(f"{sanitize(data['name'])}\t{sanitize(data['description'])}\t{sanitize(data['category'])}\t{sanitize(data['subcategory'])}"
          f"\t{sanitize(data['homepage_url'])}\t{sanitize(data['crunchbase'])}\t{sanitize(data['extra'])}", file=output)
  else:
    print(f"Error: Invalid URL {url} or could not retrieve data.")

output = open("log.tsv", "w")
print("Repo\tStars\tPull requests\tForks\tName\tDescription\tCategory\tSubcategory\tHomepage\tCrunchbase\tExtra",
      file=output)
con = sqlite3.connect('landscape.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute(f"select * from items")
repos = cur.fetchall()
for repo in repos:
  if repo['repo_url'] is None:
    pass
  else:
    print_one(repo['repo_url'], repo, output)
con.close()


