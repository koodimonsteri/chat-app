<?php

namespace App\Controller;

use App\Dto\CreateChatDto;
use App\Dto\ChatInviteDto;
use App\Entity\Chat;
use App\Entity\UserChat;
use App\Repository\ChatRepository;
use App\Repository\UserRepository;
use App\Repository\UserChatRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Validator\Validator\ValidatorInterface;
use Symfony\Component\Serializer\SerializerInterface;
use Symfony\Component\Security\Core\Security;
use Psr\Log\LoggerInterface;


#[Route('/api/chat', name: 'api_chat_')]
class ChatController extends AbstractController
{
    private $security;
    private $userChatRepository;
    private $logger;

    public function __construct(Security $security, UserChatRepository $userChatRepository, SerializerInterface $serializer, LoggerInterface $logger)
    {
        $this->security = $security;
        $this->userChatRepository = $userChatRepository;
        $this->serializer = $serializer;
        $this->logger = $logger;
    }

    #[Route('', name: 'get_chats', methods: ['GET'])]
    public function getChats(Request $request, ChatRepository $chatRepository): JsonResponse
    {
        $guid = $request->query->get('guid');

        if ($guid) {
            $user = $this->security->getUser();
            
            $userChat = $this->userChatRepository->findOneByUserAndChatGuid($user, $guid);
            if (!$userChat) {
                return new JsonResponse(['error' => 'Chat not found or access denied'], 403);
            }

            $chat = $userChat->getChat();

            $data = $this->serializer->serialize($chat, 'json', ['groups' => 'chat:read']);
            return new JsonResponse($data, 200, [], true);
        }

        $chats = $chatRepository->findAllPublicChats();

        $data = $this->serializer->serialize($chats, 'json', ['groups' => 'chat:read']);
        return new JsonResponse($data, 200, [], true);
    }

    #[Route('/user', name: 'user_chats', methods: ['GET'])]
    public function getUserChats(): JsonResponse
    {
        $user = $this->security->getUser();

        $userChats = $this->userChatRepository->findByUser($user);
        if (empty($userChats)) {
            $this->logger->notice('No chats found for user with ID: ' . $user->getId());
            return new JsonResponse(['error' => 'No chats found for user'], 200);
        }

        $chats = [];
        foreach ($userChats as $userChat) {
            $chats[] = $userChat->getChat();
        }

        $data = $this->serializer->serialize($chats, 'json', ['groups' => 'chat:read']);
        
        return new JsonResponse($data, 200, [], true);
    }

    #[Route('', name: 'create_chat', methods: ['POST'])]
    public function createChat(Request $request, ValidatorInterface $validator, EntityManagerInterface $entityManager): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (empty($data['name']) || !isset($data['is_private'])) {
            return $this->json([
                'message' => 'Missing required fields: name or is_private',
            ], JsonResponse::HTTP_BAD_REQUEST);
        }
        
        $dto = new CreateChatDto();
        $dto->name = $data['name'];
        $dto->is_private = $data['is_private'];

        $violations = $validator->validate($dto);
        if (count($violations) > 0) {
            return $this->json([
                'message' => 'Validation failed',
                'errors' => (string) $violations,
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        $chat = new Chat();
        $chat->setName($dto->name);
        $chat->setIsPrivate($dto->is_private);

        $user = $this->security->getUser();
        $chat->setChatOwner($user);

        $entityManager->persist($chat);
        $entityManager->flush();
        $this->logger->debug('Before Serialization {chat_id} {name} {is_private} {chat_owner_id} {chat_owner_username}', [
            'chat_id' => $chat->getId(),
            'name' => $chat->getName(),
            'is_private' => $chat->getIsPrivate(),
            'chat_owner_id' => $chat->getChatOwner()->getId(),
            'chat_owner_username' => $chat->getChatOwner()->getUserIdentifier(),
        ]);

        $userChat = new UserChat();
        $userChat->setUser($user);
        $userChat->setChat($chat);

        $entityManager->persist($userChat);
        $entityManager->flush();

        $data = $this->serializer->serialize($chat, 'json', ['groups' => 'chat:read']);
        $this->logger->debug('Serialized chat data: ' . $data);

        return new JsonResponse($data, 201, [], true);
    }

    #[Route('/{id}', name: 'get_chat', methods: ['GET'])]
    public function getChat(int $id): JsonResponse
    {
        $user = $this->security->getUser();

        $userChat = $this->userChatRepository->findByUserAndChat($user, $id);
        if (!$userChat) {
            return new JsonResponse(['error' => 'Chat not found or access denied'], 403);
        }

        $chat = $userChat->getChat();

        $data = $this->serializer->serialize($chat, 'json', ['groups' => 'chat:read']);
        return new JsonResponse($data, 200, [], true);
    }

    #[Route('/{id}', name: 'patch_chat', methods: ['PATCH'])]
    public function patchChat(
        int $id,
        Request $request,
        ChatRepository $chatRepository,
        EntityManagerInterface $entityManager,
        ValidatorInterface $validator
    ): JsonResponse {
        $user = $this->security->getUser();

        $userChat = $this->userChatRepository->findByUserAndChat($user, $id);
        if (!$userChat) {
            return new JsonResponse(['error' => 'Chat not found or access denied'], 403);
        }

        $chat = $userChat->getChat();

        if ($user !== $chat->getChatOwner()) {
            return new JsonResponse(['error' => 'You are not the owner of this chat'], 403);
        }
        
        $data = json_decode($request->getContent(), true);
        if (empty($data['name']) && !isset($data['is_private'])) {
            return new JsonResponse(['message' => 'At least one of the fields (name, is_private) must be provided.'], JsonResponse::HTTP_BAD_REQUEST);
        }

        $dto = new CreateChatDto();
        if (array_key_exists('name', $data)) {
            $dto->name = $data['name'];
        }
        
        if (array_key_exists('is_private', $data)) {
            $dto->is_private = $data['is_private'];
        }

        $violations = $validator->validate($dto);
        if (count($violations) > 0) {
            return $this->json([
                'message' => 'Validation failed',
                'errors' => (string) $violations,
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        if (isset($dto->name)) {
            $chat->setName($dto->name);
        }
    
        if (isset($dto->is_private)) {
            $chat->setIsPrivate($dto->is_private);
        }
    
        $entityManager->flush();
    
        return new JsonResponse(['message' => 'Chat updated successfully'], 200);
    }

    #[Route('/{id}', name: 'delete_chat', methods: ['DELETE'])]
    public function deleteChat(int $id, EntityManagerInterface $entityManager): JsonResponse
    {
        $user = $this->security->getUser();
        
        $userChat = $this->userChatRepository->findByUserAndChat($user, $id);
        if (!$userChat) {
            return new JsonResponse(['error' => 'Chat not found or access denied'], 403);
        }

        $chat = $userChat->getChat();
        if ($chat->getChatOwner() !== $user) {
            return new JsonResponse(['error' => 'You are not the owner of this chat'], 403);
        }

        $userChats = $this->userChatRepository->findBy(['chat' => $chat]);
        foreach ($userChats as $userChat) {
            $entityManager->remove($userChat);
        }

        $entityManager->remove($chat);
        $entityManager->flush();

        return new JsonResponse(['message' => 'Chat removed successfully'], 200);
    }

    #[Route('/{id}/invite-user', name: 'chat_invite', methods: ['POST'])]
    public function inviteUserToChat(
        int $id,
        Request $request,
        ChatRepository $chatRepository,
        UserChatRepository $userChatRepository,
        UserRepository $userRepository,
        ValidatorInterface $validator,
        EntityManagerInterface $entityManager
    ): JsonResponse {
        $user = $this->security->getUser();
        
        $userChat = $userChatRepository->findOneBy(['user' => $user, 'chat' => $id]);
        if (!$userChat) {
            return new JsonResponse(['error' => 'Chat not found or access denied'], 403);
        }

        $chat = $userChat->getChat();
        if ($user !== $chat->getChatOwner()) {
            return new JsonResponse(['error' => 'You are not the owner of this chat'], 403);
        }

        $data = json_decode($request->getContent(), true);
        $inviteDto = new ChatInviteDto($data['username'] ?? null, $data['email'] ?? null);

        $violations = $validator->validate($inviteDto);
        if (count($violations) > 0) {
            return $this->json([
                'message' => 'Validation failed',
                'errors' => (string) $violations,
            ], JsonResponse::HTTP_BAD_REQUEST);
        }

        $invitedUser = null;
        if ($inviteDto->username) {
            $invitedUser = $userRepository->findOneBy(['username' => $inviteDto->username]);
        } elseif ($inviteDto->email) {
            $invitedUser = $userRepository->findOneBy(['email' => $inviteDto->email]);
        }

        if (!$invitedUser) {
            return new JsonResponse(['error' => 'User not found'], 404);
        }

        $existingUserChat = $userChatRepository->findOneBy(['user' => $invitedUser, 'chat' => $chat]);
        if ($existingUserChat) {
            return new JsonResponse(['error' => 'User is already a member of the chat'], 400);
        }

        $userChat = new UserChat();
        $userChat->setUser($invitedUser);
        $userChat->setChat($chat);

        $entityManager->persist($userChat);
        $entityManager->flush();

        return new JsonResponse(['message' => 'User invited to chat successfully'], 201);
    }

    #[Route('/{id}/remove-user', name: 'chat_remove_user', methods: ['POST'])]
    public function removeUserFromChat(
        int $id,
        Request $request,
        ChatRepository $chatRepository,
        UserChatRepository $userChatRepository,
        UserRepository $userRepository,
        EntityManagerInterface $entityManager
    ): JsonResponse {
        $user = $this->security->getUser();
        
        $userChat = $userChatRepository->findOneBy(['user' => $user, 'chat' => $id]);
        if (!$userChat) {
            return new JsonResponse(['error' => 'Chat not found or access denied'], 403);
        }

        $chat = $userChat->getChat();
        if ($user !== $chat->getChatOwner()) {
            return new JsonResponse(['error' => 'You are not the owner of this chat'], 403);
        }

        $data = json_decode($request->getContent(), true);
        $username = $data['username'] ?? null;
        if (!$username) {
            return new JsonResponse(['error' => 'Username is required'], JsonResponse::HTTP_BAD_REQUEST);
        }

        $userToRemove = $userRepository->findOneBy(['username' => $username]);
        if (!$userToRemove) {
            return new JsonResponse(['error' => 'User not found'], 404);
        }

        $userChatToRemove = $userChatRepository->findOneBy(['user' => $userToRemove, 'chat' => $chat]);
        if (!$userChatToRemove) {
            return new JsonResponse(['error' => 'User is not a member of this chat'], 400);
        }

        $entityManager->remove($userChatToRemove);
        $entityManager->flush();

        return new JsonResponse(['message' => 'User removed from chat successfully'], 200);
    }
}