import requests

def count_words(subreddit, word_list, count_dict=None):
    if count_dict is None:
        count_dict = {}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        return
    data = response.json()
    for post in data["data"]["children"]:
        title = post["data"]["title"].lower()
        for word in word_list:
            if (f" {word.lower()} " in title or
                title.startswith(f"{word.lower()} ") or
                title.endswith(f" {word.lower()}") or
                title == word.lower()):
                count_dict[word.lower()] = count_dict.get(word.lower(), 0) + 1
    if data["data"]["after"] is not None:
        count_words(subreddit, word_list, count_dict)
    else:
        count_list = [(count, word) for word, count in count_dict.items()]
        count_list.sort(key=lambda x: (-x[0], x[1]))
        for count, word in count_list:
            print(f"{word}: {count}")

# example usage
count_words("learnprogramming", ["python", "javascript", "java"])
