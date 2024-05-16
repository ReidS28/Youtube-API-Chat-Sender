from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pynput.keyboard import Key, Listener
from colorama import Fore
import sys

chatMessage = "🍚🍚CHAMPA RICE!!!!🍚🍚"
stream_ID = "_9Dz65X-kAk"

# Define the scopes required by your application
SCOPES = ['https://www.googleapis.com/auth/youtube']

# Load OAuth2 credentials from file
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=SCOPES)
credentials = flow.run_local_server()

youtube = build('youtube', 'v3', credentials=credentials)

def getLiveChatId(LIVE_STREAM_ID):
    """
    It takes a live stream ID as input, and returns the live chat ID associated with that live stream

    LIVE_STREAM_ID: The ID of the live stream
    return: The live chat ID of the live stream.
    """
    try:
        stream = youtube.videos().list(
            part="liveStreamingDetails",
            id=LIVE_STREAM_ID,  # Live stream ID
        )
        response = stream.execute()

        if 'items' in response and response['items']:
            liveChatId = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
            print("\nLive Chat ID: ", liveChatId)
            return liveChatId
        else:
            print("No live streams found with ID:", LIVE_STREAM_ID)
            return None
    except Exception as e:
        print("Error occurred while retrieving live chat ID:", str(e))
        return None

def sendMessage(liveChatId, message):   
    try:
        response = youtube.liveChatMessages().insert(
            part="snippet",
            body={
                "snippet": {
                    "liveChatId": liveChatId,
                    "type": "textMessageEvent",
                    "textMessageDetails": {
                        "messageText": message,
                    }
                }
            }
        ).execute()
        
        print("Response from sendMessage API:", response)
        print("Inserted message:", response.get('snippet', {}).get('textMessageDetails', {}).get('messageText'))
    except Exception as e:
        print("Error occurred while sending message:", str(e))

def on_press(key):
    global clicking
    if key == Key.f8:

        sendMessage(getLiveChatId(stream_ID), chatMessage)

        print(
            f"{Fore.GREEN}[LOG]{Fore.WHITE} Sent \"{chatMessage}\". Press f8 again to send again."
        )   
    elif key == Key.esc:
        print(f"{Fore.GREEN}[LOG]{Fore.WHITE} Exiting program...")
        sys.exit(0)

with Listener(on_press=on_press) as listener:

    try:
        listener.join()
    except Exception as e:
        print(
            f"{Fore.RED}[ERROR]{Fore.WHITE} An error occurred: "
        )
        print(e)

youtube.close()