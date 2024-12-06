from pydantic import BaseModel


class GenerateSignedUrlResponse(BaseModel):
    signed_url: str


class Images:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    def generate_signed_url(self, filename: str) -> GenerateSignedUrlResponse:
        """Generate a pre-signed URL for file upload."""
        response = self.client.post(
            f"{self.base_url}/public/v1/images/presigned-url",
            params={"filename": filename},
        )
        response.raise_for_status()
        return GenerateSignedUrlResponse(**response.json())


class ImagesAsync:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    async def generate_signed_url(self, filename: str) -> GenerateSignedUrlResponse:
        """Generate a pre-signed URL for file upload."""
        response = await self.client.post(
            f"{self.base_url}/public/v1/images/presigned-url",
            params={"filename": filename},
        )
        response.raise_for_status()
        return GenerateSignedUrlResponse(**response.json())
