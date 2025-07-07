import os, asyncio, httpx
from httpx import Timeout, Limits, HTTPStatusError
from dotenv import load_dotenv

load_dotenv()

class RunwareAI:
    _client: httpx.AsyncClient | None = None           # client “singleton”
    _sem    = asyncio.Semaphore(4)                     # tối đa 4 request song song

    def __init__(self) -> None:
        api_key = os.getenv("STABILITY_API_KEY")
        if not api_key:
            raise RuntimeError("Missing STABILITY_API_KEY")
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "image/*"
        }

    # -------- internal --------
    @classmethod
    async def _get_client(cls) -> httpx.AsyncClient:
        if cls._client is None:
            cls._client = httpx.AsyncClient(
                base_url="https://api.stability.ai",
                http2=True,                           # bật HTTP/2
                timeout=Timeout(60.0),
                limits=Limits(max_connections=100, max_keepalive_connections=20),
            )
        return cls._client

    # -------- public API --------
    async def generate_image(self, prompt: str, aspect_ratio="9:16") -> bytes:
        async with self._sem:                         # tránh spam server
            client = await self._get_client()
            try:
                resp = await client.post(
                    "/v2beta/stable-image/generate/core",
                    headers=self._headers,
                    files={"none": (None, "")},       # multipart bắt buộc
                    data={
                        "prompt": prompt,
                        "output_format": "png",
                        "aspect_ratio": aspect_ratio,
                    },
                )
                resp.raise_for_status()
                return resp.content                   # bytes PNG
            except HTTPStatusError as exc:
                raise RuntimeError(
                    f"Stability API error {exc.response.status_code}: {exc.response.text}"
                ) from exc

    @classmethod
    async def aclose(cls):                            # gọi khi shutdown
        if cls._client:
            await cls._client.aclose()
            cls._client = None
