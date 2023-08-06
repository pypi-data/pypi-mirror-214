import pathlib
from tqdm import tqdm

import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.errors import HttpError


class Channel:
    def __init__(self, id: str, title: str) -> None:
        self.id = id
        self.title = title

    def __repr__(self):
        return "Channel(id=%s, title=%s)" % (repr(self.id), repr(self.title))

    def __key(self):
        return (self.id, self.title)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Channel):
            return self.__key() == other.__key()
        return NotImplemented


class Subscriptions:
    def __init__(self, client_secret: pathlib.Path | None):
        if client_secret == None or not isinstance(client_secret, pathlib.Path):
            raise ValueError("client_secret must be defined as a path to a json file")

        self.client_secret = client_secret

        api_service_name = "youtube"
        api_version = "v3"
        scopes = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube.force-ssl",
        ]

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secret, scopes
        )
        flow.run_local_server()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=flow.credentials
        )

        print("\n", end="")

    def list_channels(
        self, channel_id: str = None, mine: bool = False
    ) -> list[Channel]:
        if mine and channel_id:
            raise ValueError("mine cannot be set along with channel_id")

        if not channel_id and not mine:
            mine = True

        results = list[Channel]()
        response: dict
        next_page_token: str
        pbar_desc = (
            "Fetching subscriptions from channel " + channel_id
            if not mine
            else "Fetching subscriptions from destination channel"
        )
        pbar = tqdm(desc=pbar_desc)

        request, next_page_token = None, None
        while True:
            if mine:
                if next_page_token:
                    request = self.youtube.subscriptions().list(
                        part="snippet",
                        mine=True,
                        pageToken=next_page_token,
                        maxResults=50,
                    )
                else:
                    request = self.youtube.subscriptions().list(
                        part="snippet", mine=True, maxResults=50
                    )
            else:
                if next_page_token:
                    request = self.youtube.subscriptions().list(
                        part="snippet",
                        channelId=channel_id,
                        pageToken=next_page_token,
                        maxResults=50,
                    )
                else:
                    request = self.youtube.subscriptions().list(
                        part="snippet", channelId=channel_id, maxResults=50
                    )

            response = request.execute()
            items = response["items"]

            pbar.total = int(response["pageInfo"]["totalResults"])
            pbar.update(len(items))
            pbar.refresh()

            results.extend(self._parse_results(items))

            if not "nextPageToken" in response:
                break
            else:
                next_page_token = str(response["nextPageToken"])

        return results

    def insert_channels(self, channels: list[Channel]):
        for channel in tqdm(
            channels, desc="Migrating subscriptions to destination channel"
        ):
            request = self.youtube.subscriptions().insert(
                part="snippet",
                body={
                    "snippet": {
                        "resourceId": {
                            "kind": "youtube#channel",
                            "channelId": channel.id,
                        }
                    }
                },
            )
            request.execute()

    def _parse_results(self, results: list[dict]) -> list[Channel]:
        _result = list[Channel]()
        for item in results:
            snippet = item["snippet"]
            channel = Channel(
                id=snippet["resourceId"]["channelId"], title=snippet["title"]
            )
            _result.append(channel)
        return _result
