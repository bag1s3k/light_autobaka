from pydantic import BaseModel, HttpUrl, computed_field, TypeAdapter, Field

class ServerConfig(BaseModel):
    base_url: HttpUrl
    login_endpoint: str = Field(alias="login_endpoint")
    marks_endpoint: str = Field(alias="marks_endpoint")
    after_login_endpoint: str = Field(alias="after_login_endpoint")

    @computed_field
    def login_url(self) -> HttpUrl:
        """Full login url"""
        return self._combine_url(self.login_endpoint)
    
    @computed_field
    def marks_url(self) -> HttpUrl:
        """Full marks url"""
        return self._combine_url(self.marks_endpoint)

    @computed_field
    def success_url(self) -> HttpUrl:
        """Url which is displayed after u login, it means successful login"""
        return self._combine_url(self.after_login_endpoint)

    def _combine_url(self, endpoint: str) -> HttpUrl :
        """Combine base url + endpoint"""
        return TypeAdapter(HttpUrl).validate_python(f"{self.base_url}{endpoint}")
