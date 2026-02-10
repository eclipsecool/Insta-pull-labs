import os
import instaloader
import re
import random
import time

def main():
    # Fetch the target username from environment variables
    user = os.getenv("INSTA_USERNAME")
    if not user:
        print("Error: INSTA_USERNAME environment variable not set.")
        return

    # Jitter to look less like a bot
    time.sleep(random.randint(5, 45)) 

    status_message = ""
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, user)
        
        # Fetch the most recent post
        post = next(profile.get_posts())
        
        # Create the clickable Markdown image
        status_message = f'[![Latest Post]({post.url})](https://www.instagram.com/p/{post.shortcode}/)'
        
    except Exception as e:
        print(f"Error encountered: {e}")
        status_message = "⚠️ *Instagram Engine currently in timeout/cool-down. Will retry automatically.*"

    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f: 
            content = f.read()
        
        # Using your custom tags
        pattern = r"<insta:start>.*?<insta:stop>"
        replacement = f"<insta:start>\n{status_message}\n<insta:stop>"
        
        if "<insta:start>" in content:
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            with open("README.md", "w", encoding="utf-8") as f: 
                f.write(new_content)

            # Git Automation
            os.system('git config --global user.name "insta-bot"')
            os.system('git config --global user.email "actions@github.com"')
            os.system('git add README.md')
            os.system('git commit -m "Update Insta Status" || exit 0')
            os.system('git push')
        else:
            print("Required tags <insta:start> and <insta:stop> not found in README.md")

if __name__ == "__main__":
    main()
