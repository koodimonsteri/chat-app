<?php

namespace App\Dto;

use Symfony\Component\Validator\Constraints as Assert;

class LoginDto
{
    #[Assert\Length(max: 255)]
    public string $username;

    #[Assert\NotBlank]
    #[Assert\Length(max: 255)]
    public string $password;
}