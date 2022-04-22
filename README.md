This data is not being used so this script is no longer being run. Uncommenting the top lines of [.github/workflows/ci.yml](.github/workflows/ci.yml) will cause it to run once a day.

This small project uses a python script to fetch stats about Clash Royale cards from [https://clashroyale.fandom.com](https://clashroyale.fandom.com) with BeatifulSoup. After scraping the stats, it turns it into JSON and stores it into a file called card_stats.json.

This script was set up to run daily using GitHub Actions to maintain up-to-date data.

Last run at: Fri Apr 22 01:09:25 UTC 2022
