import os, re, asyncio
from roblox import Client

async def main():
    user_id = os.getenv("ROBLOX_USER_ID")
    if not user_id:
        print("Error: ROBLOX_USER_ID not found.")
        return

    client = Client()
    try:
        # 1. Fetch User and Presence using roblox.py
        user = await client.get_user(int(user_id))
        presences = await client.get_user_presences([int(user_id)])
        presence = presences[0]

        # 2. Extract Data
        # Presence Types: 0: Offline, 1: Online, 2: InGame, 3: InStudio
        p_type = presence.user_presence_type.value
        game_name = presence.last_location if presence.last_location else "N/A"
        
        if p_type == 2:
            status_text = "🟢 **In Game**"
            # Link to game if playing
            activity = f"[{game_name}](https://www.roblox.com/games/{presence.place_id})"
        elif p_type == 1 or p_type == 3:
            status_text = "🔵 **Online/Studio**"
            activity = "In App"
        else:
            status_text = "🔴 **Offline**"
            activity = "N/A"

        # 3. Fetch Thumbnail
        thumbnails = await client.thumbnails.get_user_avatar_headshots(
            users=[user], 
            size=(150, 150),
            is_circular=True
        )
        image_url = thumbnails[0].image_url

        # 4. Strictly Formatted Markdown Table
        # NOTE: The empty lines at start and end are REQUIRED for GitHub to render the table.
        table = (
            "\n"
            "| Profile | Status | Current Activity |\n"
            "| :---: | :---: | :--- |\n"
            f"| <img src='{image_url}' width='60' /> <br> **{user.display_name}** | {status_text} | {activity} |\n"
            "\n"
        )
        
    except Exception as e:
        print(f"Roblox API Error: {e}")
        table = "\n⚠️ *Roblox Engine is currently cooling down/timeout.*\n"

    # 5. Inject into README
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Using your custom <roblox start> tags
        pattern = r"<roblox start>.*?<roblox stop>"
        replacement = f"<roblox start>\n{table}\n<roblox stop>"
        
        if "<roblox start>" in content:
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(new_content)

            # 6. Push as "rblx updater"
            os.system('git config --global user.name "rblx updater"')
            os.system('git config --global user.email "actions@github.com"')
            os.system('git add README.md')
            os.system('git commit -m "Fixed Roblox Table Layout" || exit 0')
            os.system('git push')
        else:
            print("Markers <roblox start> and <roblox stop> not found!")

if __name__ == "__main__":
    asyncio.run(main())
