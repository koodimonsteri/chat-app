<?php

namespace App\Dto;

use Symfony\Component\Validator\Constraints as Assert;

class CreateChatDto
{
    #[Assert\NotBlank]
    #[Assert\Length(min: 4)]
    public string $name;

    #[Assert\Type("bool")]
    public bool $is_private;
}