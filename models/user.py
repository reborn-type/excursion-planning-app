class User:
    user_id: int
    first_name: str
    last_name: str
    age: int
    experience: int
    email: str
    guide_status: bool

    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        age: int,
        experience: int,
        email: str,
        guide_status: bool
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.experience = experience
        self.email = email
        self.guide_status = guide_status

    def __str__(self) -> str:
        return (
            f"""
            Id пользователя: {self.user_id},
            Имя: {self.first_name},
            Фамилия: {self.last_name},
            Возраст: {self.age},
            Опыт в экскурсиях: {self.experience},
            Эл. почта: {self.email},
            Статус гида: {"имеется" if self.guide_status else "не имеется"}
            """
        )

    def change_email(self, new_email: str) -> None:
        self.email = new_email

    def change_first_name(self, new_first_name: str) -> None:
        self.first_name = new_first_name

    def change_last_name(self, new_last_name: str) -> None:
        self.last_name = new_last_name

    def change_age(self, new_age: int) -> None:
        self.age = new_age

    def change_experience(self, new_experience: int) -> None:
        self.experience = new_experience

    def change_guide_status(self, new_guide_status: bool) -> None:
        self.guide_status = new_guide_status

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "experience": self.experience,
            "email": self.email,
            "guide_status": self.guide_status
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            user_id=data["user_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            experience=data["experience"],
            email=data["email"],
            guide_status=data["guide_status"]
        )
