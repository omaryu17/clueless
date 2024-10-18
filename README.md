# clueless
## Local Development
This project is built using Python `3.10.9`. You should probably have at least that version. 
To develop locally, follow the steps below:
1. Clone the repo to your computer
2. `cd` into the `clueless` folder in a terminal
3. Create a virtual environment by running `python3 -m venv venv`
    - Windows users should use `python -m venv venv` instead   
4. Activate the virtual environment by running `source venv/bin/activate`
    - Windows users should use `venv/Scripts/activate` instead
5. Install the necessary libraries by running `pip install -r requirements.txt`.

## Testing the Server/Client
The server is hosted on Render, but you can also test message sending locally if you have changes to the server you haven't pushed yet. To do so, follow the steps below:
1. Replace the argument to `io.connect` in `client.html` with `http://127.0.0.1:5000`. This reroutes the connection to your localhost.
2. Open up a terminal and `cd` into the `clueless` folder.
3. Run `python3 server.py` or equivalent depending your OS. The server should now be up locally.
4. Open up `client.html` in any web browser and open multiple tabs of it if you want to simulate multiple clients.
5. Test whatever message sending you want. Close a tab to disconnect its client.
6. When you're done, you can kill the server by doing `CTRL + C`.
