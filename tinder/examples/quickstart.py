"""
Custom Tinder bot for Joel
Modified by ChatGPT - Infinite loop after distance adjustment + Recs reset
"""

import requests
import time
import keyboard
from tinderbotj.session import Session
from tinderbotj.helpers.constants_helper import *

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data.get("loc")  # Format: latitude and longitude
        if loc:
            latitude, longitude = map(float, loc.split(','))
            return latitude, longitude
    except Exception as e:
        print("Error getting automatic location:", e)
    return 25.7617, -80.1918  # Fallback: Miami

if __name__ == "__main__":
    session = Session(store_session=True)

    # Set the user's location
    lat, lon = get_current_location()
    print(f"Detected location: {lat}, {lon}")
    session.set_custom_location(latitude=lat, longitude=lon)

    # Manual login
    print("Opening Tinder. Log in manually...")
    session.browser.get("https://tinder.com")
    input("Press ENTER when you have logged in correctly...")

    print("Starting infinite loop. Press 'q' to stop.")
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Bot stopped by user.")
                break

            # Go to the recommendations section
            session.browser.get("https://tinder.com/app/recs")

            # Basic actions
            session.like(amount=1000, ratio="72.5%", sleep=1)
            session.dislike(amount=1)
            session.superlike(amount=1)

            # Adjust preferences
            session.set_distance_range(km=150)
            session.set_age_range(18, 55)
            session.set_sexuality(Sexuality.WOMEN)
            session.set_global(True)

            # Save old matches
            for match in session.get_messaged_matches():
                session.store_local(match)

            # Send messages to new matches
            new_matches = session.get_new_matches(amount=10, quickload=False)
            pickup_line = "Hey {}! You. Me. Pizza? Or don't you like pizza?"
            for match in new_matches:
                name = match.get_name()
                chat_id = match.get_chat_id()
                print(f"Sending message to: {name}")
                session.send_message(chatid=chat_id, message=pickup_line.format(name))
                session.send_gif(chatid=chat_id, gifname="")
                session.send_song(chatid=chat_id, songname="")
                session.send_socials(chatid=chat_id, media=Socials.INSTAGRAM, value="Fredjemees")

            # Geomatches
            for _ in range(5):
                geomatch = session.get_geomatch(quickload=False)
                session.store_local(geomatch)
                session.dislike()

            time.sleep(5)

    except KeyboardInterrupt:
        print("Bot stopped with Ctrl+C")
    except Exception as e:
        print(f"Error in loop execution: {e}")
