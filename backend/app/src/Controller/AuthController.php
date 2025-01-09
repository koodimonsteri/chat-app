<?php

namespace App\Controller;

use App\Dto\RegisterUserDto;
use App\Dto\LoginDto;
use App\Entity\User;
use App\Repository\UserRepository;
use Doctrine\ORM\EntityManagerInterface;
use Lexik\Bundle\JWTAuthenticationBundle\Services\JWTTokenManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Validator\Validator\ValidatorInterface;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/api', name: 'api_')]
class AuthController extends AbstractController
{
    #[Route('/register', name: 'register', methods: ['POST'])]
    public function register(Request $request, ValidatorInterface $validator, UserPasswordHasherInterface $passwordHasher, UserRepository $userRepository, EntityManagerInterface $entityManager): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (empty($data['username']) || empty($data['email']) || empty($data['password'])) {
            return $this->json([
                'message' => 'Missing required fields: username, email, or password',
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        $dto = new RegisterUserDto();
        $dto->username = $data['username'];
        $dto->email = $data['email'];
        $dto->password = $data['password'];

        $violations = $validator->validate($dto);
        if (count($violations) > 0) {
            return $this->json([
                'message' => 'Validation failed',
                'errors' => (string) $violations,
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        if ($userRepository->findOneBy(['email' => $dto->email])) {
            return $this->json([
                'message' => 'Email is already registered.',
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        if ($userRepository->findOneBy(['username' => $dto->username])) {
            return $this->json([
                'message' => 'Username is already taken.',
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        $user = new User();
        $user->setUsername($dto->username);
        $user->setEmail($dto->email);
        
        // Use bcrypt to hash the password securely
        $hashedPassword = $passwordHasher->hashPassword($user, $dto->password);
        $user->setPassword($hashedPassword);

        $entityManager->persist($user);
        $entityManager->flush();

        return $this->json([
            'message' => 'User created successfully!',
        ], JsonResponse::HTTP_CREATED);
    }

    #[Route('/login', name: 'login', methods: ['POST'])]
    public function login(Request $request, UserPasswordHasherInterface $passwordHasher, UserRepository $userRepository, JWTTokenManagerInterface $JWTManager, ValidatorInterface $validator): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (empty($data['username']) || empty($data['password'])) {
            return $this->json([
                'message' => 'Missing required fields: username or password',
            ], JsonResponse::HTTP_BAD_REQUEST);
        }
        
        $dto = new LoginDto();
        $dto->username = $data['username'];
        $dto->password = $data['password'];

        $violations = $validator->validate($dto);
        if (count($violations) > 0) {
            return $this->json([
                'message' => 'Validation failed',
                'errors' => (string) $violations,
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        $user = $userRepository->findOneBy(['username' => $dto->username]);
        if (!$user) {
            return $this->json([
                'message' => 'Invalid username.',
            ], JsonResponse::HTTP_UNAUTHORIZED);
        }

        // Verify the password against the stored hashed password
        if (!$passwordHasher->isPasswordValid($user, $dto->password)) {
            return $this->json([
                'message' => 'Invalid credentials.',
            ], JsonResponse::HTTP_UNAUTHORIZED);
        }
        
        $token = $JWTManager->create($user);

        return $this->json([
            'message' => 'Login successful.',
            'token' => $token,
        ], JsonResponse::HTTP_OK);
    }

    #[Route('/logout', name: 'logout', methods: ['POST'])]
    public function logout(): JsonResponse
    {
        // Handle logout logic or simply return a response
        return new JsonResponse(['message' => 'Logged out successfully']);
    }

    #[Route('/api/test', name: 'test_route', methods: ['GET'])]
    public function testRoute(): JsonResponse
    {
        return new JsonResponse(['message' => 'Test route works!']);
    }
}