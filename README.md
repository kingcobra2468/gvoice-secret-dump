# **Google Voice Secret Dump**
Selenium-based Python3.7+ cookie and API key dump for Google Voice service. Utilized
for accessing the internal Google Voice API. 

## **Limitations**
Due to Google's automation detection, it is necessary to run the script in a
non-headless environment. Otherwise, the script will not function properly. It
is also assumed this Google account is not making use of 2FA and has finished
the initial setup.

## **Config**
The following environment variables need to be set prior to running the script:
- **GVOICE_EMAIL=** the Google email for the account.
- **GVOICE_PASSWORD=** the Google password for the account.

## **Setup**
The following steps need to done before running the `secret_dump.py` script:
1. Ensure that a Python3.7+ environment has already been setup.
2. Ensure the Chrome geckodriver has been setup on the machine.
3. Install dependencies with `pip3 install -r requirements.txt`.
4. Set the environment varaibles as described in [config](#config).
5. Navigate to `src/` and run the script with `python3 secret_dump.py`. The
   secrets will be dumped into a `secrets.json` file.

## **Handling Wrong Chrome Version Error**
The following error might pop up when the script is run:
```
selenium.common.exceptions.WebDriverException: Message: unknown error: cannot connect to chrome at 127.0.0.1:50107
from session not created: This version of ChromeDriver only supports Chrome version 101
Current browser version is 98.0.4692.71
```

In the case of the error, you would need to set the chrome driver
version as the major release of the currently installed browser. In this
case it would be **98**. To set it, pass it as an arg when running 
such as: 
```
python3 secret_dump.py 98
```  

## **Using GVoice Secret Dump as a Library**
Google voice secret dump can also be utilized as a package for other Python projects. Simply
install it with: 
```
pip3 install git+https://github.com/kingcobra2468/gvoice-secret-dump
```

### **Sample usage**
Example of logging in and getting secret dump.
```python
from gvoicesecretdump.secrets.gvoice_secret import GVoiceSecret

username='username@gmail.com'
password='password'

# geckodriver chrome version
chrome_version = 100

account = GVoiceSecret(username, password, chrome_version)
account.login()

print(f'secrets: {account.dump_secrets()}')
```
