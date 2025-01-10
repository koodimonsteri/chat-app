<?php


namespace App\Controller;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Security\Core\Security;
use Symfony\Component\Serializer\SerializerInterface;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

#[Route('/api/user', name: 'api_user_')]
class UserController extends AbstractController
{
    private $security;

    public function __construct(Security $security, SerializerInterface $serializer)
    {
        $this->security = $security;
        $this->serializer = $serializer;
    }

    #[Route('/current', name: 'current_user', methods: ['GET'])]
    public function currentUser()
    {
        $user = $this->security->getUser();
        $data = $this->serializer->serialize($user, 'json', ['groups' => 'user:read']);
        return new JsonResponse($data, 200, [], true);
    }

    #[Route('/update', name: 'update_user', methods: ['PUT'])]
    public function updateUser()
    {
        //TODO: Update user
    }

    #[Route('/delete', name: 'delete_user', methods: ['DELETE'])]
    public function deleteUser()
    {
        // TODO: Delete user
    }
}