from pydantic import BaseModel


class SocialLinkOut(BaseModel):
	id: int
	platform: str
	url: str
	handle: str
