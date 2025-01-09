<?php

namespace App\Entity;

use App\Repository\UserChatRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Serializer\Annotation\Groups;

#[ORM\Entity(repositoryClass: UserChatRepository::class)]
class UserChat
{

    #[ORM\Id]
    #[ORM\ManyToOne(targetEntity: User::class)]
    #[ORM\JoinColumn(name: 'user_id', referencedColumnName: 'id', nullable: false)]
    private User $user;

    #[ORM\Id]
    #[ORM\ManyToOne(targetEntity: Chat::class, fetch: 'EAGER')]
    #[ORM\JoinColumn(name: 'chat_id', referencedColumnName: 'id', nullable: false)]
    private Chat $chat;

    ##[ORM\Id]
    ##[ORM\ManyToOne(targetEntity: User::class)]
    ##[ORM\JoinColumn(name: 'user_id', referencedColumnName: 'id', nullable: false)]
    #private User $user;

    ##[ORM\Id]
    ##[ORM\ManyToOne(targetEntity: Chat::class)]
    ##[ORM\JoinColumn(name: 'chat_id', referencedColumnName: 'id', nullable: false)]
    #private Chat $chat;

    ##[ORM\Column(type: 'integer', nullable: false)]
    #private ?int $user_id = null;

    ##[ORM\Column(type: 'integer', nullable: false)]
    #private ?int $chat_id = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getUser(): User
    {
        return $this->user;
    }

    public function setUser(User $user): static
    {
        $this->user = $user;
        #$this->user_id = $user->getId();
        return $this;
    }

    public function getChat(): Chat
    {
        return $this->chat;
    }

    public function setChat(Chat $chat): static
    {
        $this->chat = $chat;
        #$this->chat_id = $chat->getId();
        return $this;
    }
}
