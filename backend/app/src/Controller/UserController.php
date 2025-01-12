<?php


namespace App\Controller;

use App\Dto\UserUpdateDto;
use App\Repository\UserRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Security\Core\Security;
use Symfony\Component\Serializer\SerializerInterface;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Validator\Validator\ValidatorInterface;


#[Route('/api/user', name: 'api_user_')]
class UserController extends AbstractController
{
    private $security;

    public function __construct(UserRepository $userRepository, Security $security, SerializerInterface $serializer, ValidatorInterface $validator)
    {
        $this->security = $security;
        $this->serializer = $serializer;
        $this->validator = $validator;
        $this->userRepository = $userRepository;
    }

    #[Route('/current', name: 'current_user', methods: ['GET'])]
    public function currentUser()
    {
        $user = $this->security->getUser();
        $data = $this->serializer->serialize($user, 'json', ['groups' => 'user:read']);
        return new JsonResponse($data, 200, [], true);
    }

    #[Route('/', name: 'update_user', methods: ['PATCH'])]
    public function updateUser(Request $request, EntityManagerInterface $entityManager)
    {
        $data = json_decode($request->getContent(), true);

        if (empty($data['username']) || empty($data['email'])) {
            return $this->json([
                'message' => 'Missing required fields: username, email',
            ], 400);
        }
        
        $dto = new UserUpdateDto();
        $dto->username = $data['username'];
        $dto->email = $data['email'];

        $violations = $validator->validate($dto);
        if (count($violations) > 0) {
            return $this->json([
                'message' => 'Validation failed',
                'errors' => (string) $violations,
            ], 400);
        }

        if ($userRepository->findOneBy(['email' => $dto->email])) {
            return $this->json([
                'message' => 'Email is already registered.',
            ], 400);
        }

        if ($userRepository->findOneBy(['username' => $dto->username])) {
            return $this->json([
                'message' => 'Username is already taken.',
            ], 400);
        }


        $entityManager->persist($user);
        $entityManager->flush();

        $data = $this->serializer->serialize($user, 'json', ['groups' => 'user:read']);
        return new JsonResponse($data, 201, [], true);
    }

    #[Route('/$id', name: 'delete_user', methods: ['DELETE'])]
    public function deleteUser(int $id)
    {
        $user = $this->security->getUser();

        $db_user = $this->userRepository()->get_current_user();
    }
}