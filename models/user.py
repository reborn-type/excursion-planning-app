from dataclasses import dataclass 

@dataclass
class User: 
    user_id: int
    first_name: str 
    last_name: str
    age: int
    experience: int 
    email: str
    
    def change_email(self, new_email: str) -> None:
        self.email = new_email
    
    def change_first_name(self, new_first_name: str) -> None:
        self.first_name = new_first_name
    
    def change_last_name(self, new_last_name: str) -> None:
        self.last_name = new_last_name
    
    def change_age(self, new_age: int) -> None:
        self.age = new_age
        
    def change_experience(self, new_experience) -> None:
        self.experience = new_experience
    
    
    
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id, 
            "name": self.name, 
            "age": self.age, 
            "experience": self.experience, 
            "email": self.email,
        }
        
    @classmethod 
    def from_dict(self, data: dict) -> "User":
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            age=data["age"],
            experience=data["experience"],
            email=data["email"],
        )
    