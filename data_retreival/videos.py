import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import re


def get_transcript(video_id):
    try:
        # Extract transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Print full transcript
        full_text = " ".join([entry['text'] for entry in transcript])
        # print("Full Transcript:", full_text)

        return full_text
    except Exception as e:
        print(f"Error extracting transcript: {e}")


def get_video_details(video_url):
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        # Create a YoutubeDL object
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info_dict = ydl.extract_info(video_url, download=False)

            # Video details
            title = info_dict.get('title', 'N/A')
            description = info_dict.get('description', 'N/A')
            # views = info_dict.get('view_count', 'N/A')
            length = info_dict.get('duration', 'N/A')
            upload_date = info_dict.get('upload_date', 'N/A')
            uploader = info_dict.get('uploader', 'N/A')
            # thumbnail_url = info_dict.get('thumbnail', 'N/A')

            return {
                "title": title,
                "description": description,
                # "views": views,
                "duration": length,
                "upload_date": upload_date,
                "uploader": uploader,
                # "thumbnail": thumbnail_url
            }

    except Exception as e:
        print(f"Error: {e}")
        return {}

# Get URLs of all videos of a channel
def get_youtube_video_ids(channel_url, api_key):
    # Extract the channel ID from the URL
    channel_id = extract_channel_id(channel_url, api_key)
    if not channel_id:
        print("Invalid channel URL or unable to fetch channel ID.")
        return []

    # Initialize YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_ids = []
    next_page_token = None

    # Fetch videos from the channel
    while True:
        response = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            order="date",
            type="video",
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):
            video_ids.append(item["id"]["videoId"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

def extract_channel_id(channel_url, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Extract channel ID from different formats
    match = re.search(r"youtube\.com/(?:c/|channel/|user/|@)?([^/?]+)", channel_url)
    if not match:
        return None

    identifier = match.group(1)

    # Check if it's already a channel ID
    if identifier.startswith("UC"):
        return identifier

    # Try resolving custom channel name
    response = youtube.search().list(
        part="snippet",
        q=identifier,
        type="channel",
        maxResults=1
    ).execute()

    if response["items"]:
        return response["items"][0]["id"]["channelId"]

    return None


# Get video details of all youtube videos of channel
def get_channel_videos_data(channel_url, api_key):
    # Get the list of video IDs for the given YouTube channel
    video_ids = get_youtube_video_ids(channel_url, api_key)
    # print("video ids :-")
    # for id in video_ids:
    #     print(id)

    # List to store video data
    videos_data = []

    # cnt = 0
    for video_id in video_ids:
        # if cnt > 9:
        #   break
        # Get video details
        info_dict = get_video_details(video_id)
        if len(info_dict) == 0:
            continue

        # Extract relevant details
        video_data = {
            "video_id": video_id,
            "title": info_dict.get("title", "N/A"),
            "description": info_dict.get("description", "N/A"),
            "length": info_dict.get("duration", "N/A"),
            "upload_date": info_dict.get("upload_date", "N/A"),
            "uploader": info_dict.get("uploader", "N/A"),
            "transcript": get_transcript(video_id)  # Get transcript
        }

        # Append to the list
        videos_data.append(video_data)
        cnt += 1

    return videos_data
