import time
import random
import sys

def type_effect(text, delay=0.05):
    """Simulates typing effect for dramatic output."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def fake_hack():

    type_effect("🔓 Welcome to Skaltuch_HACK Pro 9000 🔓", 0.1)
    type_effect("Connecting to the Galactic Cyber Defense Network...\n", 0.05)
    time.sleep(2)


    target = input("Enter your target host: ").strip()
    type_effect(f"Establishing secure connection to {target}...\n")
    time.sleep(1)


    for i in range(1, 6):
        type_effect(f"Running algorithm {i}/5: {'#' * random.randint(5, 20)}", 0.02)
        time.sleep(random.uniform(0.2, 1.5))
    
    type_effect("\n💻 Connection established! Gaining access to secure data...\n")
    time.sleep(2)


    username = input("Enter the admin username for the system: ").strip()
    type_effect(f"Validating username '{username}'...\n")
    time.sleep(2)

    password = input("Enter the super-secret password: ").strip()
    type_effect("Decrypting password...\n")
    time.sleep(2)

    if random.choice([True, False]):
        type_effect("🔒 Access Denied! Retrying brute force attack...\n")
        time.sleep(2)
    else:
        type_effect("🔓 Password accepted! You're in. 🎉\n")
    

    type_effect(f"Downloading classified files from {target}...\n")
    for i in range(0, 101, random.randint(10, 20)):
        type_effect(f"Downloading: {i}% complete...")
        time.sleep(random.uniform(0.1, 0.5))
    
    type_effect("\n📂 Files downloaded successfully!")
    time.sleep(0.5)


    type_effect("\n🔍 Searching for hidden secrets...\n")
    secrets = [
        "The truth about us election ",
        "XTremely classified CIA-Trump-tehran ",
        "Truth about Aliens 👽",
        "A folder full of videos of putin dancing with his cat 🐱",
        "Xtreme Nudity -18 !!!!🎥"
    ]
    for secret in secrets:
        type_effect(f"Found: {secret}")
        time.sleep(1)


    type_effect("\n⚠️ ERROR: Detected counter-hack attempt! Retaliating...\n", 0.04)
    for i in range(1, 4):
        type_effect(f"Deploying counter-hack protocol {i}/3...")
        time.sleep(1)
    
    type_effect("\n🛡️ Retaliation successful. Opponent's system fried.\n")
    time.sleep(1)


    type_effect("💾 Saving all downloaded files to your desktop as 'Not-Hacked-Files.zip'...\n")
    time.sleep(2)
    type_effect("Send a 1000$ worth of Bitcoin to this address --0x096E1425784147vf25er78gfcv2541er2549eedc5E28-- or you're hard Disk will burn in 60 seconds")

    for i in range(60, 0, -1):
        sys.stdout.write(f"\rTime left: {i} seconds... ")
        sys.stdout.flush()
        
        
        if random.random() < 0.1:  
            sys.stdout.write("Warning: Something is watching you...!!\n")
            sys.stdout.write(" Time is money so dont waste it ...!!\n")
            sys.stdout.flush()
            time.sleep(1)

        
        if random.random() < 0.15:  
            sys.stdout.write("Thump... thump...\n")
            sys.stdout.flush()
            time.sleep(0.5)

        
        if random.random() < 0.05: 
            sys.stdout.write("\033[0;31mERROR: System failure... \033[0m")
            sys.stdout.flush()
            time.sleep(0.3)


        if random.random() < 0.2:  
            sys.stdout.write("\nHurry up and send the money\n")
            sys.stdout.flush()
            time.sleep(2)
            
        time.sleep(1)
        
    sys.stdout.write("\nCountdown complete... \n")
    sys.stdout.flush()
    sys.stdout.write("You are not alone. 😱\n")
    sys.stdout.flush()    
    
    type_effect("😂 Just kidding. You really thought this was real? Go touch some grass. 🌱\n", 0.1)
    type_effect("Thanks for using Skaltuch-HACK PRO. Stay out of trouble! 🖖")

if __name__ == "__main__":
    fake_hack()

