<?php

namespace App\Entity;

use App\Repository\UserRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
use Symfony\Component\Security\Core\User\UserInterface;

#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: '`user`')]
class User implements PasswordAuthenticatedUserInterface, UserInterface
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    #[Groups(['user:read'])]
    private ?int $id = null;

    #[ORM\Column(length: 255, unique: true)]
    #[Groups(['user:read', 'user:create'])]
    private ?string $username = null;

    #[ORM\Column(length: 255, unique: true)]
    #[Groups(['user:read', 'user:create'])]
    private ?string $email = null;

    #[ORM\Column(length: 255)]
    #[Groups(['user:create'])]
    private ?string $pw_hash = null;

    #[ORM\Column(type: 'json')]  // Use JSON to store array of roles
    private array $roles = [];

    #[ORM\Column]
    #[Groups(['user:read'])]
    private ?\DateTimeImmutable $created_at = null;

    public function __construct()
    {
        $this->created_at = new \DateTimeImmutable();
        $this->roles = [];
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getUserIdentifier(): string
    {
        return (string) $this->username;
    }

    public function getRoles(): array
    {
        $roles = $this->roles ?? [];
        // Ensure the user has at least one role
        if (empty($roles)) {
            $roles[] = 'ROLE_USER';  // Adding a default role if none is set
        }
        return array_unique($roles);  // Remove duplicate roles if any
    }

    public function setRoles(array $roles): self
    {
        $this->roles = $roles;
        return $this;
    }

    public function eraseCredentials()
    {
        // You can add code here to erase any sensitive data, if necessary.
    }

    public function setUsername(string $username): static
    {
        $this->username = $username;

        return $this;
    }

    public function getEmail(): ?string
    {
        return $this->email;
    }

    public function setEmail(string $email): static
    {
        $this->email = $email;

        return $this;
    }

    public function getPassword(): ?string
    {
        return $this->pw_hash;
    }

    public function setPassword(string $password): static
    {
        $this->pw_hash = $password;

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
