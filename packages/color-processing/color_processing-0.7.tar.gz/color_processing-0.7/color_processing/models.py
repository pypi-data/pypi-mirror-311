from typing import Any, Dict, List
from discord import Embed, File, Message, Color
from io import BytesIO

class WebSafe:
    def __init__(self, hex_: str, rgb: tuple):
        self.hex_ = hex_
        self.rgb = rgb
    
    def __str__(self) -> str:
        return f"<WebSafe hex={self.hex_} rgb={self.rgb}>"
    
    def __dict__(self) -> dict:
        return {"hex_": self.hex_, "rgb": self.rgb}
    
    def dict(self) -> dict:
        return self.__dict__()
    
class ColorInfoResponse:
    def __init__(self, name: str, hex_: str, websafe: dict, rgb: tuple, brightness: int, shades: list, palette: BytesIO, image: BytesIO):
        self.name = name
        self.hex_ = hex_
        self.websafe = WebSafe(**websafe)
        self.rgb = rgb
        self.brightness = brightness
        self.shades = shades
        self.palette = palette
        self.image = image

    
    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "hex_": self.hex_,
            "websafe": self.websafe.__dict__(),
            "rgb": self.rgb,
            "brightness": self.brightness,
            "shades": self.shades,
            "palette": self.palette.getvalue(),
            "image": self.image.getvalue(),
        }
    
    def dict(self) -> dict:
        return self.__dict__()

    @property
    def embed(self) -> Dict[str, Any]:
        shade = ", ".join(m.strip("#") for m in self.shades[:4])
        rgb = f"({self.rgb[0]}, {self.rgb[1]}, {self.rgb[2]})"
        embed = Embed(title=f"{self.name} ({self.hex_})", color=Color.from_str(self.hex_))
        embed.add_field(name="Websafe", value=f"`{self.websafe.hex_} {tuple(self.websafe.rgb)}`", inline=True)
        embed.add_field(name="RGB", value=f"`{rgb}`", inline=True)
        embed.set_image(url="attachment://palette.png")
        embed.add_field(name="Brightness", value=self.brightness, inline=True)
        embed.add_field(name="Shades", value=f"```{shade}```", inline=False)
        embed.set_thumbnail(url="attachment://color.png")
        return {"files": [File(fp = self.image, filename = "color.png"), File(fp = self.palette, filename = "palette.png")], "embed": embed}
    
    async def to_message(self, ctx) -> Message:
        return await ctx.send(**self.embed)

    def __str__(self) -> str:
        return f"<ColorInfoResponse name='{self.name}' hex={self.hex_} WebSafe={self.websafe.__str__()} rgb={self.rgb} brightness={self.brightness} shades={self.shades} image={self.image} palette={self.palette}>"
    

class SearchResult:
    def __init__(self, name: str, hex_: str):
        self.name = name
        self.hex_ = hex_
    
    def __dict__(self) -> dict:
        return {"name": self.name, "hex_": self.hex_}
    
    def __str__(self) -> str:
        return f"<SearchResult name='{self.name}' hex={self.hex_}>"


class SearchResponse:
    def __init__(self, results: List[dict]):
        self.results = [SearchResult(**result) for result in results]

    def __dict__(self) -> dict:
        return {"results": [dict(result) for result in self.results]}
    
    @property
    def count(self) -> int:
        return len(self.results)
    
    def __str__(self) -> str:
        return f"<SearchResponse results={[result.__str__() for result in self.results]} count={self.count}>"
    

