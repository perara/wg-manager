import requests

if __name__ == "__main__":
    sess = requests.Session()

    resp = sess.post("http://localhost:8888/api/v1/login", data={
        "username": "admin",
        "password": "admin"
    })
    print(resp.json())
    sess.headers.update({
        "Authorization": f"Bearer {resp.json()['access_token']}"
    })

    for _ in range(20):
        print(sess.get("http://localhost:8888/api/v1/wg/generate_psk").json())
