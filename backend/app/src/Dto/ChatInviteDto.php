<?php

namespace App\Dto;

use Symfony\Component\Validator\Constraints as Assert;

class ChatInviteDto
{
    #[Assert\Length(min: 4, max: 255)]
    public ?string $username = null;

    #[Assert\Email]
    #[Assert\Length(max: 255)]
    public ?string $email = null;

    public function __construct(?string $username = null, ?string $email = null)
    {
        $this->username = $username;
        $this->email = $email;
    }

    #[Assert\IsTrue(message: "Either username or email must be provided, but not both.")]
    public function isValid(): bool
    {
        return ($this->username !== null && $this->email === null) || ($this->username === null && $this->email !== null);
    }
}