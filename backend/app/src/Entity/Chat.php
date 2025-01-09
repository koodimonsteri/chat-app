<?php

namespace App\Entity;

use App\Repository\ChatRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Uid\Uuid;
use Symfony\Component\Serializer\Annotation\Groups;

#[ORM\Entity(repositoryClass: ChatRepository::class)]
class Chat
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    #[Groups(['chat:read'])]
    private ?int $id = null;

    #[ORM\Column(length: 255, nullable: false)]
    #[Groups(['chat:read'])]
    private ?string $name = null;

    #[ORM\Column(type: "boolean", nullable: false)]
    #[Groups(['chat:read'])]
    private bool $is_private = true;

    #[ORM\ManyToOne(targetEntity: User::class)]
    #[ORM\JoinColumn(name: "chat_owner_id", referencedColumnName: "id", nullable: false)]
    #[Groups(['chat:read'])]
    private ?User $chat_owner = null;

    #[ORM\Column(length: 36, nullable: false)]
    #[Groups(['chat:read'])]
    private string $guid;

    #[ORM\Column]
    #[Groups(['chat:read'])]
    private ?\DateTimeImmutable $created_at = null;

    #[ORM\OneToMany(targetEntity: Message::class, mappedBy: 'chat')]
    private Collection $messages;

    public function __construct()
    {
        $this->created_at = new \DateTimeImmutable();
        $this->messages = new ArrayCollection();
        $this->guid = Uuid::v4()->toRfc4122();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): static
    {
        $this->name = $name;

        return $this;
    }

    public function getIsPrivate(): bool
    {
        return $this->is_private;
    }

    public function setIsPrivate(bool $is_private): static
    {
        $this->is_private = $is_private;
        return $this;
    }

    public function getChatOwner(): User
    {
        return $this->chat_owner;
    }

    public function setChatOwner(User $chat_owner): static
    {
        $this->chat_owner = $chat_owner;
        return $this;
    }

    public function getGuid(): ?string
    {
        return $this->guid;
    }

    public function setGuid(?string $guid): static
    {
        $this->guid = $guid;
        return $this;
    }

    public function getCreatedAt(): ?\DateTimeImmutable
    {
        return $this->created_at;
    }

    public function setCreatedAt(\DateTimeImmutable $created_at): static
    {
        $this->created_at = $created_at;

        return $this;
    }

}
