from fastapi import APIRouter

from app.schemas.content import SocialLinkOut

router = APIRouter(prefix="/api/social-links", tags=["content"])


@router.get("", response_model=list[SocialLinkOut])
def list_social_links() -> list[SocialLinkOut]:
	return [
		SocialLinkOut(
			id=1,
			platform="instagram",
			url="https://www.instagram.com/",
			handle="@gelaender",
		),
		SocialLinkOut(
			id=2,
			platform="bandcamp",
			url="https://bandcamp.com/",
			handle="gelaender",
		),
		SocialLinkOut(
			id=3,
			platform="tidal",
			url="https://tidal.com/",
			handle="gelaender",
		),
	]
