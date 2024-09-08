from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
import google_auth_oauthlib.flow
import os
import googleapiclient.discovery
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Define scopes and client secrets file
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
client_secrets_file = os.getenv("GOOGLE_SECRET_API")


def get_channel():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # API service information
    api_service_name = "youtube"
    api_version = "v3"

    # Authenticate and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=8000)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Make an API request to list subscriptions
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=50)

    response = request.execute()
    return response


def subscriptions_to_dataframe(response):
    # Extract data into a list of dictionaries
    data = [
        {
            'Channel Title': item['snippet']['title'],
            'Channel ID': item['snippet']['resourceId']['channelId'],
            'Description': item['snippet']['description'],
            'Published At': item['snippet']['publishedAt']
        }
        for item in response.get('items', [])
    ]

    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    # Fetch channel subscriptions
    result = get_channel()

    # Convert result to DataFrame
    df = subscriptions_to_dataframe(result)

    # Print the DataFrame
    print(df)

    # Save DataFrame to CSV file with UTF-8 encoding with BOM
    df.to_csv('youtube_subscriptions.csv', index=False, encoding='utf-8')

    print("Data saved to youtube_subscriptions.csv with utf-8-sig encoding")
