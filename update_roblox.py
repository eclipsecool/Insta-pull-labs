import os, re, robloxpy

def main():
    user_id = os.getenv("ROBLOX_USER_ID")
    if not user_id: return

    try:
        # 1. Fetch Data using robloxpy (The library you just installed)
        image_url = robloxpy.User.External.GetAvatar(user_id)
        user_info = robloxpy.User.Internal.GetPlayerInfo(user_id)
        display_name = user_info.get('displayName', 'User')
        
        # Get Presence (This returns 'Online', 'Offline', or 'In Game: [Game Name]')
        presence = robloxpy.User.Internal.Presence(user_id)

        # 2. Build a Proper Markdown Table
        # NOTE: Blank lines \n are REQUIRED before and after for rendering.
        table = (
            "\n"
            "| Profile | Current Status |\n"
            "| :---: | :--- |\n"
            f"| <img src='{image_url}' width='60' /> <br> **{display_name}** | {presence} |\n"
            "\n"
        )
        
    except Exception as e:
        print(f"Error: {e}")
        table = "\n⚠️ *Roblox Engine Timeout - Retrying soon.*\n"

    # 3. Inject into README
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Use your custom tags
        pattern = r"<roblox start>.*?<roblox stop>"
        replacement = f"<roblox start>\n{table}\n<roblox stop>"
        
        if "<roblox start>" in content:
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(new_content)

            # 4. Commit as "rblx updater"
            os.system('git config --global user.name "rblx updater"')
            os.system('git config --global user.email "actions@github.com"')
            os.system('git add README.md')
            os.system('git commit -m "Fixed Table with robloxpy" || exit 0')
            os.system('git push')
