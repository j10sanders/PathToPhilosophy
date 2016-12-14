# themuse 2.0

Clearly [the Muse](https://www.themuse.com/) needed a UI overhaul :wink:

I made this job search app by utilizing the Muse's public API.  I had some fun with [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) and [requests](http://docs.python-requests.org/en/master/) (neither of which I had used before).

 Improvements I could add:

1. More testing.  I would prefer a TDD approach, but I just wanted to get a working example up.  There are some basic tests included, but they aren't covering much.
2. Better style -- I basically just copied their font and used some of the same colors.  That isn't enough to really be on-brand (but that wasn't my goal).
3. Make use of Javascript to dynamically update searches with each criteria selection.
4. Asynchronous processing of the company list.