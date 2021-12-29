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