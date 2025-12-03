from Domain.Entities.Book.BookEntity import BookEntity


class BookReadEntity(BookEntity):
    category_name: str
    knowledge_area_name: str
    sub_area_name: str
    editorial_name: str
    fullname_user: str
    author_name: str



    def serialize(self) -> dict:

        data = self.model_dump()
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()

        return data
