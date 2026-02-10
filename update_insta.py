import os, instaloader, re, random, time

def main():
    user = os.getenv("INSTA_USERNAME")
    time.sleep(random.randint(5, 45)) # Scaling protection

    loader = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(loader.context, user)
    post = next(profile.get_posts())
    
    tag = f'[![Latest Post]({post.url})](https://www.instagram.com/p/{post.shortcode}/)'

    if os.path.exists("README.md"):
        with open("README.md", "r") as f: content = f.read()
        new_content = re.sub(r".*?", 
                             f"\n{tag}\n", 
                             content, flags=re.DOTALL)
        with open("README.md", "w") as f: f.write(new_content)

        os.system('git config --global user.name "insta-bot"')
        os.system('git config --global user.email "actions@github.com"')
        os.system('git add README.md')
        os.system('git commit -m "Update Insta" || exit 0')
        os.system('git push')

if __name__ == "__main__":
    main()
