<?php

namespace App\Dto;

use Symfony\Component\Validator\Constraints as Assert;

class UserUpdateDto
{
    #[Assert\NotBlank]
    #[Assert\Length(min: 4, max: 255)]
    public string $username;

    #[Assert\NotBlank]
    #[Assert\Email]
    #[Assert\Length(max: 255)]
    public string $email;

}