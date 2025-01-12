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
use Symfony\Component\Serializer\SerializerInterface;

#[Route('/api/auth', name: 'api_auth_')]
class AuthController extends AbstractController
{
    #[Route('/register', name: 'register', methods: ['POST'])]
    public function register(Request $request, ValidatorInterface $validator, UserPasswordHasherInterface $passwordHasher, UserRepository $userRepository, EntityManagerInterface $entityManager): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (empty($data['username']) || empty($data['email']) || empty($data['password'])) {
            return $this->json([
                'message' => 'Missing required fields: username, email, or password',
            ], 400);
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
        ], 201);
    }

    #[Route('/login', name: 'login', methods: ['POST'])]
    public function login(Request $request, UserPasswordHasherInterface $passwordHasher, UserRepository $userRepository, JWTTokenManagerInterface $JWTManager, ValidatorInterface $validator): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (empty($data['username']) || empty($data['password'])) {
            return $this->json([
                'message' => 'Missing required fields: username or password',
            ], 400);
        }
        
        $dto = new LoginDto();
        $dto->username = $data['username'];
        $dto->password = $data['password'];

        $violations = $validator->validate($dto);
        if (count($violations) > 0) {
            return $this->json([
                'message' => 'Validation failed',
                'errors' => (string) $violations,
            ], 400);
        }

        $user = $userRepository->findOneBy(['username' => $dto->username]);
        if (!$user) {
            return $this->json([
                'message' => 'Invalid username.',
            ], 401);
        }

        // Verify the password against the stored hashed password
        if (!$passwordHasher->isPasswordValid($user, $dto->password)) {
            return $this->json([
                'message' => 'Invalid credentials.',
            ], 401);
        }
        
        $token = $JWTManager->create($user);

        return $this->json([
            'message' => 'Login successful.',
            'token' => $token,
        ], 200);
    }

    #[Route('/logout', name: 'logout', methods: ['POST'])]
    public function logout(): JsonResponse
    {
        // Handle logout logic or simply return a response
        return new JsonResponse(['message' => 'Logged out successfully']);
    }

    #[Route('/test', name: 'test_route', methods: ['GET'])]
    public function testRoute(): JsonResponse
    {
        return new JsonResponse(['message' => 'Test route works!']);
    }
}