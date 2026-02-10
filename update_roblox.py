import os, requests, re

def main():
    user_id = os.getenv("ROBLOX_USER_ID")
    if not user_id:
        return

    try:
        # 1. Fetch Display Name
        user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
        name = user_info.get("displayName", "Robloxian")

        # 2. Fetch Avatar Headshot
        thumb_api = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=352x352&format=Png&isCircular=true"
        thumb_data = requests.get(thumb_api).json()
        image_url = thumb_data['data'][0]['imageUrl']

        # 3. Create Markdown Tag
        status = f"### 🎮 Roblox Activity\n**User:** {name}\n\n<img src='{image_url}' width='150' />"
    except Exception as e:
        print(f"Error: {e}")
        status = "⚠️ *Roblox Engine currently in timeout.*"

    # 4. Inject into README
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Using your custom markers
        pattern = r"<roblox start>.*?<roblox stop>"
        replacement = f"<roblox start>\n{status}\n<roblox stop>"
        
        if "<roblox start>" in content:
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(new_content)

            # 5. Push changes only if we actually found the markers
            os.system('git config --global user.name "eclipsecool-bot"')
            os.system('git config --global user.email "actions@github.com"')
            os.system('git add README.md')
            os.system('git commit -m "Update Roblox Profile" || exit 0')
            os.system('git push')
        else:
            print("Markers not found. Skipping push to avoid loop.")

if __name__ == "__main__":
    main()
