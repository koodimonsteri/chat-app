from pydantic import BaseModel, EmailStr, Field, field_validator



class RegisterUser(BaseModel):

    username: str = Field(..., min_length=4, max_length=255, description="User's unique username.")
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255, description="Password with at least one uppercase letter and one digit.")

    @field_validator("password")
    def validate_password(cls, v):
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