import requests

ENDPOINT = "https://rocky-gorge-77460-611a79604e3d.herokuapp.com"

userPayload = {
    "uid": "sune", 
    "pwd": "1234"
}
WebToken = ""
def test_register():
    post_register = requests.post(ENDPOINT + "/register", json=userPayload)
    assert post_register.status_code == 201

def test_login():
    global WebToken
    post_login = requests.post(ENDPOINT + "/login", json=userPayload)
    assert post_login.status_code == 200
    WebToken = str(post_login.content).split(" ")[1]
    WebToken = WebToken[:-2]

def test_get_users():
    get_user = requests.get(ENDPOINT + "/users")
    assert get_user.status_code == 200
    data = get_user.json()

    users = data["users"]
    assert len(users) >= 2

def test_get_quotes():
    get_quotes = requests.get(ENDPOINT + "/quotes")
    assert get_quotes.status_code == 200
    data = get_quotes.json()
    data1 = data["quotes"][-1].get("qid")
    print(data1)

quotePayload = {
    "quote": "Skulle man kalde det en dag?",
    "attribution": "-- Marcus"
}

def test_post_quote():
    global qid
    header = {"Authorization" : "Bearer "+str(WebToken)}
    quote = requests.post(ENDPOINT + "/quote", quotePayload, headers=header)
    assert quote.status_code == 201
    get_quotes = requests.get(ENDPOINT + "/quotes")
    data = get_quotes.json()
    qid = data["quotes"][-1].get("qid")
    
def test_get_quote():
    quote = requests.get(ENDPOINT + "/quote/"+str(qid))
    assert quote.status_code == 200
    # Test om quoted var det samme som det jeg poster
    # data = quote.json()
    #assert data.get("quote") == quotePayload.get("quote")
    #assert data.get("attribution") == quotePayload.get("attribution")


newQuotePayload = {
    "quote": "Vi kalder det en dag",
    "attribution": "-- Sune"
}

def test_put_quote():
    header = {"Authorization" : "Bearer "+str(WebToken)}
    quote = requests.put(ENDPOINT + "/quote/"+str(qid), newQuotePayload, headers=header)
    assert quote.status_code == 204

def test_delete_quote():
    header = {"Authorization" : "Bearer "+str(WebToken)}
    quote = requests.delete(ENDPOINT + "/quote/"+str(qid), headers=header)
    assert quote.status_code == 204