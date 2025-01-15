from pydantic import BaseModel, EmailStr, Field, field_validator



class RegisterUser(BaseModel):

    username: str = Field(..., min_length=4, max_length=255)
    email: str = EmailStr
    password: str = Field(..., min_length=6, max_length=255)

    @field_validator("password")
    def password_complexity(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter.")
        return v


class LoginUser(BaseModel):

    username: str = Field(..., min_length=4, max_length=255)
    password: str = Field(..., min_length=6, max_length=255)


class Token(BaseModel):

    token: str
    token_type: str