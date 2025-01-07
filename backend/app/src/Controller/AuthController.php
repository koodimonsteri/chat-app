<?php

namespace App\Controller;

use App\Dto\RegisterUserDto;
use App\Entity\User;
use App\Repository\UserRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Validator\Validator\ValidatorInterface;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Symfony\Component\Routing\Annotation\Route;
use Doctrine\ORM\EntityManagerInterface;
use Lexik\Bundle\JWTAuthenticationBundle\Services\JWTTokenManagerInterface;

#[Route('/api', name: 'api_')]
class AuthController extends AbstractController
{
    #[Route('/register', name: 'register', methods: ['POST'])]
    public function register(Request $request, ValidatorInterface $validator, UserPasswordHasherInterface $passwordHasher, UserRepository $userRepository, EntityManagerInterface $entityManager): JsonResponse
    {
        // Decode the incoming JSON request body to DTO
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

        // Validate the DTO
        $violations = $validator->validate($dto);
        if (count($violations) > 0) {
            return $this->json([
                'message' => 'Validation failed',
                'errors' => (string) $violations,
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        // Check if the user already exists (optional)
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

        // Create a new user
        $user = new User();
        $user->setUsername($dto->username);
        $user->setEmail($dto->email);
        
        // Use bcrypt to hash the password securely
        $hashedPassword = $passwordHasher->hashPassword($user, $dto->password);
        $user->setPassword($hashedPassword);

        // Save the user
        $entityManager->persist($user);
        $entityManager->flush();

        return $this->json([
            'message' => 'User created successfully!',
        ], JsonResponse::HTTP_CREATED);
    }

    #[Route('/login', name: 'login', methods: ['POST'])]
    public function login(Request $request, UserPasswordHasherInterface $passwordHasher, UserRepository $userRepository, JWTTokenManagerInterface $JWTManager): JsonResponse
    {
        // Assuming you have the email and password from the request
        $data = json_decode($request->getContent(), true);

        if (empty($data['username']) || empty($data['password'])) {
            return $this->json([
                'message' => 'Missing required fields: username or password',
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        $username = $data['username'];
        $plainPassword = $data['password'];

        // Find the user by email
        $user = $userRepository->findOneBy(['username' => $username]);

        if (!$user) {
            return $this->json([
                'message' => 'Invalid username.',
            ], JsonResponse::HTTP_UNAUTHORIZED);
        }

        // Verify the password against the stored hashed password
        if (!$passwordHasher->isPasswordValid($user, $plainPassword)) {
            return $this->json([
                'message' => 'Invalid credentials.',
            ], JsonResponse::HTTP_UNAUTHORIZED);
        }
        
        $token = $JWTManager->create($user);

        // Handle successful login (e.g., issue a JWT or session)
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