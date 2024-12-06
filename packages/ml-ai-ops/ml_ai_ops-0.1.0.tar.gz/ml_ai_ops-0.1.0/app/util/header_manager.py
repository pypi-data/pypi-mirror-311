from typing import Dict


class HeaderManager:
    def __init__(
        self,
        *,
        header: Dict[str, any] | None = None
    ) -> None:
        self.header = header

    def set_header(self, new_header: Dict[str, any]) -> None:
        self.header = new_header

    def get_header(self) -> Dict[str, any] | None:
        return self.header
    
    def set_cookies(self, cookies: str) -> None:
        if self.header is None:
            self.header = {}
        self.header["Cookie"] = cookies

