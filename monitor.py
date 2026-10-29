python
import requests
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
THRESHOLD_PRICE = -60.00  # -$60/MWh equals -6c/kWh. Change this to modify!
UPPER_THRESHOLD_PRICE = -500.00  # $500/MWh equals 50c/kWh. Change this to modify!
NTFY_TOPIC = "qld-power-4keith"  # <-- Change this to your ntfy topic

AEMO_URL = "https://aemo.com.au"

def check_qld_price():
    try:
        response = requests.get(AEMO_URL, timeout=10)
        if response.status_code != 200:
            print("Failed to get data from AEMO")
            return

        root = ET.fromstring(response.content)
        
        for price_data in root.findall(".//PRICE"):
            region = price_data.get("REGION")
            if region == "QLD1":
                current_price = float(price_data.get("PRICE"))
                print(f"Current QLD Spot Price: ${current_price:.2f}/MWh")

               if current_price <= THRESHOLD_PRICE:
                    trigger_notification(current_price)
                break

                if current_price >= UPPER_THRESHOLD_PRICE:
                    trigger_notification2(current_price)
                break


    except Exception as e:
        print(f"Error checking market: {e}")

def trigger_notification(price):
    c_per_kwh = price / 10
    message = f"QLD power price is currently {c_per_kwh:.2f}¢/kWh! Go plug in the EV!"
    
    requests.post(
        f"https://ntfy.sh{NTFY_TOPIC}",
        data=message.encode('utf-8'),
        headers={
            "Title": "⚡ Deep Negative Price Alert!",
            "Priority": "high"
        }
    )

def trigger_notification2(price):
    c_per_kwh = price / 10
    message = f"QLD power price is currently {c_per_kwh:.2f}¢/kWh! Export to the grid"
    
    requests.post(
        f"https://ntfy.sh{NTFY_TOPIC}",
        data=message.encode('utf-8'),
        headers={
            "Title": "⚡ High Price Alert!",
            "Priority": "high"
        }
    )

  if __name__ == "__main__":
    check_qld_price()

              
