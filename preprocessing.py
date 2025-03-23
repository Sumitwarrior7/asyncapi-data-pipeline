from bs4 import BeautifulSoup
import html
import re
import emoji

def preprocess_html(html_content):
    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Convert headers
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        level = tag.name[1]  # Extract header level (1,2,3..)
        tag.insert_before(f"{'#' * int(level)} ")
        tag.unwrap()  # Remove the HTML tag

    # Convert <strong> to markdown **bold**
    for tag in soup.find_all("strong"):
        tag.insert_before("**")
        tag.insert_after("**")
        tag.unwrap()

    # Convert <a> tags to markdown [text](link)
    for tag in soup.find_all("a", href=True):
        link_text = tag.text.strip()
        link_url = tag["href"]
        tag.replace_with(f"[{link_text}]({link_url})")

    # Convert <code> to markdown `code`
    for tag in soup.find_all("code"):
        tag.insert_before("`")
        tag.insert_after("`")
        tag.unwrap()

    # Get plain text
    clean_text = soup.get_text(separator="\n").strip()

    # Decode HTML entities
    clean_text = html.unescape(clean_text)

    # Remove excessive white spaces (including newlines and tabs)
    clean_text = re.sub(r'\s+', ' ', clean_text)  # Replace multiple spaces with a single space
    clean_text = re.sub(r'\n+', '\n', clean_text)  # Replace multiple newlines with a single newline

    # Remove emojis and other non-ASCII characters (optional)
    # clean_text = clean_text.encode('ascii', 'ignore').decode('ascii')
    clean_text = emoji.demojize(clean_text)

    # Remove markdown images (e.g., ![alt](url))
    clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', clean_text)

    # Remove empty brackets (e.g., [])
    clean_text = re.sub(r'\[\s*\]', '', clean_text)

    # Remove standalone markdown links (e.g., [](url))
    clean_text = re.sub(r'\[\s*\]\(.*?\)', '', clean_text)

    # Remove extra spaces around punctuation
    clean_text = re.sub(r'\s+([.,;!?])', r'\1', clean_text)

    return clean_text


# Example usage
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emoji & Links Page</title>
</head>
<body>

    <h1>✨ Welcome to the Emoji & Links Page! ✨</h1>

    <p>
        🎉 This page is filled with emojis, white spaces, and links! 🎉    
        
        Here’s a fun list of emojis:   
        🚀 🌟 🐱 🖥️ 🔥 😍 🎨 🎭  
    </p>

    <p>Check out some cool websites:</p>

    <ul>
        <li>🌍 <a href="https://www.google.com">Google</a></li>  
        <li>🐦 <a href="https://twitter.com">Twitter</a></li>  
        <li>📘 <a href="https://www.facebook.com">Facebook</a></li>  
        <li>💻 <a href="https://github.com">GitHub</a></li>  
    </ul>

    <pre>
        This    text    contains    random   spaces.   
        Some words       are    spaced out.  
        
        🎵      Music  is   life! 🎵  
    </pre>

    <p>🔗 Follow me on <a href="https://www.linkedin.com">LinkedIn</a>! 💼</p>

    <footer>
        <p>© 2025 Made with ❤️ and lots of emojis! 🎊</p>
    </footer>

</body>
</html>

"""

processed_text = preprocess_html(html_content)
print(processed_text)
