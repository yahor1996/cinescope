from pydantic import BaseModel

class TestMovie(BaseModel):
    name: str
    imageUrl: str
    price: int
    description: str
    location: str
    published: bool
    genreId: int


class MovieCreatedResponse(TestMovie, BaseModel):
    id: int
    genre: dict
    createdAt: str
    rating: float


class GetMoviesResponse(BaseModel):
    movies: list[MovieCreatedResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int
