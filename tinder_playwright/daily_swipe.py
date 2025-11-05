from tinderbotj.session import Session
from dotenv import load_dotenv
import sys
import os

# Load .env file
load_dotenv()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python daily_swipe.py \
              <manual_login> \
              <likes> \
              <ratio> \
              <sleep> \
              <change_settings> \
              <latitude> \
              <longitude> \
              <distance_km> \
              Example: DISPLAY=:10 python daily_swipe.py False 10 50.25% 4 False")
        sys.exit(1)

    manual_login = str(sys.argv[1]).strip().lower() in {"1", "true", "yes", "y"}

    print(manual_login)
    # creates instance of session
    session = Session(headless= not manual_login, driver_path=os.getenv("CHROME_BINARY"))
    print("Opening Tinder. Log in manually...")
    
    if manual_login is True:
        # Open Tinder login page for manual login
        session.page.goto("https://tinder.com")
        input(" Please log in manually, then press ENTER to continue...")
        print(" Logged in! Starting bot actions...\n")
    else:
        session.login_using_google(os.getenv("TINDER_EMAIL"), os.getenv("TINDER_PASSWORD"))
    
    change_settings = str(sys.argv[5]).strip().lower() in {"1", "true", "yes", "y"}
    
    if change_settings is True:
        # check if latitude and longitude are valid
        if not sys.argv[6] or not sys.argv[7]:
            print("no latitude or longitude provided; skipping custom location.")
        else:
            latitude = sys.argv[6]
            longitude = sys.argv[7]
            try:
                session.set_custom_location(latitude=float(latitude), longitude=float(longitude))
            except ValueError:
                print("Invalid latitude/longitude values; skipping custom location.")

        if not sys.argv[8]:
            print("no distance_km provided; skipping distance configuration.")
        else:
            distance_km = sys.argv[8]
            try:
                session.set_distance_range(km=int(distance_km))
            except ValueError:
                print("Invalid distance_km; skipping distance configuration.")

    likes = int(sys.argv[2])
    ratio = sys.argv[3]
    sleep = float(sys.argv[4])
    
    session.like(amount=likes, ratio=ratio, sleep=sleep, randomize_sleep=True)

    # new_matches = session.get_new_matches(amount=10, quickload=False)

    # for match in new_matches:
    #     session.store_local(match)

    #     # store name and chatid in variables so we can use it more simply later on
    #     name = match.get_name()
    #     id = match.get_chat_id()

    #     print(name, id)

    #     # first_message = ""

    #     # # send pick up line with their name in it to all my matches
    #     # session.send_message(chatid=id, message=first_message)
