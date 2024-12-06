from typing import Generator, Optional
import requests
import json

from query2clips.pipeline.searcher.abc import Searcher


class YtInitialData:
    def __init__(self, yt_initial_data: dict):
        self.yt_initial_data = yt_initial_data

    def visitor_data(self) -> str:
        return self.yt_initial_data["responseContext"][
            "webResponseContextExtensionData"
        ]["ytConfigData"]["visitorData"]

    def primary_contents(self) -> list[dict]:
        return self.yt_initial_data["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"]

    def item_section_renderer(self) -> dict:
        return next(
            content["itemSectionRenderer"]
            for content in self.primary_contents()
            if "itemSectionRenderer" in content
        )

    def continuation_item_renderer(self) -> dict:
        return next(
            content["continuationItemRenderer"]
            for content in self.primary_contents()
            if "continuationItemRenderer" in content
        )


class YoutubeSearcher(Searcher):
    """
    example usage:
    ```py
    searcher = YoutubeSearcher()
    for video_urls in searcher.search("Top Rated video games walkthrough", 100):
        for video_url in video_urls:
            print(f"Video: {video_url}")
    ```
    """

    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def video_id_to_url(video_id: str) -> str:
        return f"https://youtu.be/{video_id}"

    @staticmethod
    def playlist_id_to_url(playlist_id: str) -> str:
        return f"https://www.youtube.com/playlist?list={playlist_id}"

    def get_yt_initial_data(self, query: str) -> YtInitialData:
        response = self.session.get(
            f"https://www.youtube.com/results?search_query={query}"
        )
        data = response.text
        yt_initial_data = json.loads(
            data.split("var ytInitialData = ")[1].split(";</script>")[0]
        )
        return YtInitialData(yt_initial_data)

    def item_section_renderer_to_results(
        self, item_section_renderer: dict
    ) -> list[dict[str, Optional[str]]]:
        results = []
        for content in item_section_renderer["contents"]:
            if "videoRenderer" in content:
                results.append(
                    self.video_id_to_url(content["videoRenderer"]["videoId"])
                )
        return results

    def search_more(
        self, query: str, continuation_item_renderer: dict, visitor_data: str
    ) -> tuple:
        click_tracking_params = continuation_item_renderer["continuationEndpoint"][
            "clickTrackingParams"
        ]
        continuation = continuation_item_renderer["continuationEndpoint"][
            "continuationCommand"
        ]["token"]
        api_url = continuation_item_renderer["continuationEndpoint"]["commandMetadata"][
            "webCommandMetadata"
        ]["apiUrl"]

        more = {
            "context": {
                "client": {
                    "hl": "en",
                    "gl": "KR",
                    "deviceMake": "Apple",
                    "deviceModel": "",
                    "clientName": "WEB",
                    "clientVersion": "2.20241007.01.00",
                    "visitorData": visitor_data,
                    "osName": "Macintosh",
                    "osVersion": "10_15_7",
                    "originalUrl": f"https://www.youtube.com/results?search_query={query}",
                    "platform": "DESKTOP",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "timeZone": "Asia/Seoul",
                    "browserName": "Chrome",
                    "browserVersion": "128.0.0.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "screenWidthPoints": 1920,
                    "screenHeightPoints": 1080,
                    "screenPixelDensity": 1,
                    "screenDensityFloat": 1,
                    "utcOffsetMinutes": 540,
                    "connectionType": "CONN_CELLULAR_4G",
                    "memoryTotalKbytes": "8000000",
                    "mainAppWebInfo": {
                        "graftUrl": f"https://www.youtube.com/results?search_query={query}",
                        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED",
                        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                        "isWebNativeShareAvailable": True,
                    },
                },
                "user": {"lockedSafetyMode": False},
                "request": {
                    "useSsl": True,
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": [],
                },
                "clickTracking": {
                    "clickTrackingParams": click_tracking_params,
                },
            },
            "continuation": continuation,
        }

        response = self.session.post(f"https://www.youtube.com{api_url}", json=more)
        data = response.json()

        continuation_items = next(
            c["appendContinuationItemsAction"]["continuationItems"]
            for c in data["onResponseReceivedCommands"]
            if "appendContinuationItemsAction" in c
        )

        return (
            next(
                c["itemSectionRenderer"]
                for c in continuation_items
                if "itemSectionRenderer" in c
            ),
            next(
                c["continuationItemRenderer"]
                for c in continuation_items
                if "continuationItemRenderer" in c
            ),
        )

    def search(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
    ) -> Generator[list[str], None, None]:
        yt_initial_data = self.get_yt_initial_data(query)
        visitor_data = yt_initial_data.visitor_data()

        item_section_renderer = yt_initial_data.item_section_renderer()
        continuation_item_renderer = yt_initial_data.continuation_item_renderer()

        fetched_count = 0
        yielded_count = 0
        while yielded_count < limit:
            results = self.item_section_renderer_to_results(item_section_renderer)
            item_section_renderer, continuation_item_renderer = self.search_more(
                query, continuation_item_renderer, visitor_data
            )

            fetched_count += len(results)
            if fetched_count < offset:
                continue

            part = results[offset - fetched_count : limit - yielded_count]
            if len(part) > 0:
                yield part
                yielded_count += len(part)
