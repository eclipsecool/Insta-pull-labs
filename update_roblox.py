import os, requests, re, json

def main():
    # Fetch ID from the workflow environment variable
    user_id = os.getenv("ROBLOX_USER_ID")
    
    if not user_id:
        print("No Roblox User ID provided.")
        return

    status_message = ""
    try:
        # 1. Get User Profile Details (Username/Display Name)
        profile_url = f"https://users.roblox.com/v1/users/{user_id}"
        profile_response = requests.get(profile_url)
        profile_data = profile_response.json()
        display_name = profile_data.get("displayName", "Robloxian")

        # 2. Get Avatar Thumbnail (Headshot)
        thumb_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=352x352&format=Png&isCircular=true"
        thumb_response = requests.get(thumb_url)
        thumb_data = thumb_response.json()
        image_url = thumb_data['data'][0]['imageUrl']

        # 3. Create the Markdown Content
        status_message = f"### 🎮 Roblox Activity\n**User:** {display_name}\n\n<img src='{image_url}' width='150' />"
        
    except Exception as e:
        print(f"Roblox API Error: {e}")
        status_message = "⚠️ *Roblox Engine currently in timeout. Will retry automatically.*"

    # 4. Update the README
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f: 
            content = f.read()
        
        # Look for ROBLOX markers
        pattern = r".*?"
        replacement = f"\n{status_message}\n"
        
        if "" in content:
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        else:
            # Fallback if markers aren't there yet
            new_content = content + f"\n\n{replacement}"

        with open("README.md", "w", encoding="utf-8") as f: 
            f.write(new_content)

        # 5. Standard Auto-Push to GitHub
        os.system('git config --global user.name "eclipsecool-bot"')
        os.system('git config --global user.email "actions@github.com"')
        os.system('git add README.md')
        os.system('git commit -m "Update Roblox Profile" || exit 0')
        os.system('git push')

if __name__ == "__main__":
    main()
