# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from KekikStream.Core                 import PluginBase, SearchResult, MovieInfo
from KekikStream.Core.ExtractorModels import ExtractResult, Subtitle

class SineWix(PluginBase):
    name     = "SineWix"
    main_url = "https://ythls.kekikakademi.org"

    async def search(self, query: str) -> list[SearchResult]:
        istek = await self.oturum.get(f"{self.main_url}/sinewix/search/{query}")

        return [
            SearchResult(
                title  = veri.get("name"),
                url    = f"?type={veri.get('type')}&id={veri.get('id')}",
                poster = self.fix_url(veri.get("poster_path")),
            )
                for veri in istek.json().get("search") if veri.get("type") == "movie"
        ]

    async def load_item(self, url: str) -> MovieInfo:
        item_type = url.split("?type=")[-1].split("&id=")[0]
        item_id   = url.split("&id=")[-1]

        match item_type:
            case "movie":
                istek = await self.oturum.get(f"{self.main_url}/sinewix/movie/{item_id}")
                veri  = istek.json()

                org_title = veri.get("title")
                alt_title = veri.get("original_name") or ""
                title     = f"{org_title} - {alt_title}" if (alt_title and org_title != alt_title)  else org_title

                return MovieInfo(
                    url         = self.fix_url(f"{self.main_url}/sinewix/movie/{item_id}"),
                    poster      = self.fix_url(veri.get("poster_path")),
                    title       = title,
                    description = veri.get("overview"),
                    tags        = [genre.get("name") for genre in veri.get("genres")],
                    rating      = veri.get("vote_average"),
                    year        = veri.get("release_date"),
                    actors      = [actor.get("name") for actor in veri.get("casterslist")],
                )

    async def load_links(self, url: str) -> list[str]:
        istek = await self.oturum.get(url)
        veri  = istek.json()

        org_title = veri.get("title")
        alt_title = veri.get("original_name") or ""
        title     = f"{org_title} - {alt_title}" if (alt_title and org_title != alt_title)  else org_title
        title     = f"{self.name} | {title}"

        for video in veri.get("videos"):
            video_link = video.get("link").split("_blank\">")[-1]
            self._data[video_link] = {
                "name"      : title,
                "referer"   : self.main_url,
                "subtitles" : []
            }

        return list(self._data.keys())

    async def play(self, name: str, url: str, referer: str, subtitles: list[Subtitle]):
        extract_result = ExtractResult(name=name, url=url, referer=referer, subtitles=subtitles)
        self.media_handler.title = name
        self.media_handler.play_with_vlc(extract_result)