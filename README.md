# Fetch-Rewards-Backend-Project
A service for tracking points paid and spent by payers and users

# Get started
1. Clone this repository
2. Install Python 3 (preferably 3.9)
3. Navigate to the directory containing `requirements.txt` and run  
```
$ pip install -r requirements.txt
```
4. Run `python api.py` or `python3 api.py`
5. Navigate to [127.0.0.1:8080](http://127.0.0.1:8080) in your browser of choice

# Usage
* To add transactions, navigate to [127.0.0.1:8080/add](http://127.0.0.1:8080/add) and fill out the form.  
Fill out the form like this:  
Payer: DANNON  
Points: 1000  
Timestamp: 2020-11-02T14:00:00Z  
Press 'submit' after you fill out all fields.

* To spend points, navigate to [127.0.0.1:8080/spend](http://127.0.0.1:8080/spend) and fill out the form.  
Fill out the form like this:  
Points: 1000  
Press 'submit' after you fill out all fields.

* To return all payer point balances, navigate to [127.0.0.1:8080/balances](http://127.0.0.1:8080/balances).
