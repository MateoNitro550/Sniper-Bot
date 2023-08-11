#!/bin/python3

from pwn import log
from time import sleep
from selenium import webdriver
from discord import Client, Intents
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Color variables
blue_color = "\u001b[0;34m\u001b[1m"
gray_color = "\u001b[0;37m\u001b[1m"
light_blue_color = "\u001b[32;1m"
end_color = "\u001b[0m\u001b[0m"

def initialize_sniper():
    # Set the URL of the product page
    product_url = "https://www.example.com/products/12345"

    p1 = log.progress(gray_color + "SniperBot" + end_color)

    # Set up the Selenium web driver
    s = Service("/path/to/your/web/driver") # Placeholder comment for the actual driver path
    driver = webdriver.Chrome(service=s)

    p1.status(blue_color + "URL reached" + end_color)
    driver.get(product_url)

    search(p1, driver)

def search(p1, driver):
    try:
        # Verify the product availability by checking for the disabled button
        p1.status(blue_color + "Verifying product availability" + end_color)
        button_disabled = driver.find_element(By.CSS_SELECTOR, "/* CSS selector for disabled button */")  # Placeholder comment for the CSS selector

        if button_disabled:
            # If the button is disabled, indicating product is out of stock, wait and refresh the page
            p1.status(blue_color + "Add to Cart button not found" + end_color)
            sleep(60)
            driver.refresh()
            search(p1, driver)

    except NoSuchElementException:
        # If the button is not disabled, indicating product is available
        p1.status(blue_color + "Verifying product availability" + end_color)
        add_to_cart = driver.find_element(By.CSS_SELECTOR, "/* CSS selector for Add to Cart button */")  # Placeholder comment for the CSS selector

        if add_to_cart:
            # Add the item to the cart
            p1.success(light_blue_color + "Item added to cart" + end_color)
            add_to_cart.click()

            sleep(5)
            driver.find_element(By.CSS_SELECTOR, "/* CSS selector for Go to Cart button */").click() # Placeholder comment for the CSS selector

            send_discord_notification("Item added to cart!")

def send_discord_notification(message):
    p2 = log.progress(gray_color + "Discord Notification" + end_color)

    # Discord bot token
    token = "YOUR_DISCORD_BOT_TOKEN"

    # Discord channel ID
    channel_id = "YOUR_DISCORD_CHANNEL_ID"

    # Create a Discord client with specified intents
    intents = Intents.default()
    intents.typing = False
    intents.presences = False
    client = Client(intents=intents)

    @client.event
    async def on_ready():
        # Get the Discord channel
        channel = client.get_channel(int(channel_id))

        # Send the message to the Discord channel multiple times
        for i in range(3):
            p2.success(light_blue_color + "Messages sent" + end_color)
            await channel.send(message)
            sleep(5)

        # Close the Discord client
        await client.close()

    client.run(token)    

    sleep(10800)

def main():
    initialize_sniper()

if __name__ == "__main__":
    main()
