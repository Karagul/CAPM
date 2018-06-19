# CAPM
Required: Python 3, HTML 5

Realtime Data from: Yahoo, Optimization Data from quandl

Import: numpy, scipy, quandl, html.parser, urllib.request, flask,

- CAPM.py -> Portfolio selector under CAPM

- Portfolio.py -> realtime data and custom portfolio for paper trading

- Utility.py -> Use Portfolio.py to test CAPM.py by paper trading

- app.py -> flask build for the app

- log.txt -> save all portfolio() created 

- log.db -> save all portfolio() created if SQL methods are used

- curr.txt -> save current user in the app

- /templates -> all html interface

- /static -> .js .css and all document that supports html

To Run:

- console: python app.py

- Local Address in browser: http://127.0.0.1:5000/
