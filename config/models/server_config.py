from pydantic import BaseModel, HttpUrl, computed_field, TypeAdapter

class ServerConfig(BaseModel):
    base_url: HttpUrl
    login_endpoint: str
    marks_endpoint: str

    @computed_field
    @property
    def login_url(self) -> HttpUrl:
        """Full login url"""
        return self._combine_url(self.login_endpoint)
    
    @computed_field
    @property
    def marks_url(self) -> HttpUrl:
        """Full marks url"""
        return self._combine_url(self.marks_endpoint)
    
    def _combine_url(self, endpoint: str) -> HttpUrl :
        """Combine base url + endpoint"""
        return TypeAdapter(HttpUrl).validate_python(f"{self.base_url}{endpoint}")
