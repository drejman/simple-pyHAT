from dataclasses import dataclass, field

from app.config import settings


@dataclass
class Artist:
    name: str
    id: int
    cover_image: str | None = None
    urls: list[str] = field(default_factory=list)
    uri: str | None = None
    members: list[dict] = field(default_factory=list)
    profile: str | None = None
    thumb: str | None = None

    def __post_init__(self):
        if not self.cover_image:
            self.cover_image =  "/static/missing.png"
        
        if not self.thumb:
            self.thumb =  "/static/missing.png"
        
        if not self.profile:
            self.profile = "No profile available"
        else:
            self.profile = self.profile.replace("[", "<").replace("]", ">")

    @property
    def website(self):
        if not self.urls:
            return self.uri  # send discogs uri if no url found
        return self.urls[0]

    @property
    def active_members(self):
        if not self.members:
            return [self.name]
        active_members = [member["name"] for member in self.members if member.get("active") and member.get("name")]
        return active_members[:10]
    
    @property
    def short_profile(self):
        return f"{self.profile[:settings.SEARCH_LENGTH]}..."
