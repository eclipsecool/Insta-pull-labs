import os, requests, re

def main():
    user_id = os.getenv("ROBLOX_USER_ID")
    if not user_id:
        return

    try:
        # 1. Fetch Profile Details
        user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
        name = user_info.get("displayName", "Robloxian")

        # 2. Fetch Presence & Game Link
        presence_data = requests.post("https://presence.roblox.com/v1/presence/users", 
                                     json={"userIds": [int(user_id)]}).json()
        presence = presence_data['userPresences'][0]
        
        p_type = presence.get('userPresenceType', 0)
        game_name = presence.get('lastLocation', 'None')
        place_id = presence.get('placeId')

        # Format Status and Link
        if p_type == 2 and place_id:
            status_text = "🟢 **In Game**"
            activity = f"[{game_name}](https://www.roblox.com/games/{place_id})"
        elif p_type == 1:
            status_text = "🟢 **Online**"
            activity = "Browsing Roblox"
        else:
            status_text = "🔴 **Offline**"
            activity = "N/A"

        # 3. Fetch Avatar Thumbnail
        thumb_api = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=352x352&format=Png&isCircular=true"
        thumb_data = requests.get(thumb_api).json()
        image_url = thumb_data['data'][0]['imageUrl']

        # 4. Create Table Format
        table = (
            f"### 🎮 Roblox Activity\n\n"
            f"| Profile | Status | Current Activity |\n"
            f"| :--- | :--- | :--- |\n"
            f"| <img src='{image_url}' width='60' /> <br> **{name}** | {status_text} | {activity} |\n"
        )
        
    except Exception as e:
        print(f"Error: {e}")
        table = "⚠️ *Roblox Engine currently in timeout.*"

    # 5. Inject into README
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        pattern = r"<roblox start>.*?<roblox stop>"
        replacement = f"<roblox start>\n{table}\n<roblox stop>"
        
        if "<roblox start>" in content:
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(new_content)

            # 6. Push changes
            os.system('git config --global user.name "rblx updater"')
            os.system('git config --global user.email "actions@github.com"')
            os.system('git add README.md')
            os.system('git commit -m "Update Roblox Status Table" || exit 0')
            os.system('git push')
