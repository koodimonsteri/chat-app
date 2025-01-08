<?php

namespace App\Controller;

use App\Entity\Chat;
use App\Repository\ChatRepository;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Serializer\SerializerInterface;

class ChatController extends AbstractController
{
    #[Route('/api/chats', name: 'api_chat_index', methods: ['GET'])]
    public function index(ChatRepository $chatRepository, SerializerInterface $serializer): JsonResponse
    {
        $chats = $chatRepository->findAll();

        $data = $serializer->serialize($chats, 'json', ['groups' => 'chat:read']);

        return new JsonResponse($data, 200, [], true);
    }

    #[Route('/api/chats', name: 'api_chat_create', methods: ['POST'])]
    public function create(Request $request, ChatRepository $chatRepository, SerializerInterface $serializer): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (isset($data['name'])) {
            $chat = new Chat();
            $chat->setName($data['name']);
            $chat->setCreatedAt(new \DateTimeImmutable());

            $entityManager = $this->getDoctrine()->getManager();
            $entityManager->persist($chat);
            $entityManager->flush();

            $data = $serializer->serialize($chat, 'json', ['groups' => 'chat:read']);

            return new JsonResponse($data, 201, [], true);
        }

        return new JsonResponse(['error' => 'Invalid data'], 400);
    }

    #[Route('/api/chats/{id}', name: 'api_chat_show', methods: ['GET'])]
    public function show(int $id, ChatRepository $chatRepository, SerializerInterface $serializer): JsonResponse
    {
        $chat = $chatRepository->find($id);

        if (!$chat) {
            return new JsonResponse(['error' => 'Chat not found'], 404);
        }

        $data = $serializer->serialize($chat, 'json', ['groups' => 'chat:read']);
        return new JsonResponse($data, 200, [], true);
    }

    #[Route('/api/chats/{id}', name: 'api_chat_update', methods: ['PUT'])]
    public function update(int $id, Request $request, ChatRepository $chatRepository, SerializerInterface $serializer): JsonResponse
    {
        $chat = $chatRepository->find($id);

        if (!$chat) {
            return new JsonResponse(['error' => 'Chat not found'], 404);
        }

        $data = json_decode($request->getContent(), true);

        if (isset($data['name'])) {
            $chat->setName($data['name']);
            $entityManager = $this->getDoctrine()->getManager();
            $entityManager->flush();

            $data = $serializer->serialize($chat, 'json', ['groups' => 'chat:read']);
            return new JsonResponse($data, 200, [], true);
        }

        return new JsonResponse(['error' => 'Invalid data'], 400);
    }

    #[Route('/api/chats/{id}', name: 'api_chat_delete', methods: ['DELETE'])]
    public function delete(int $id, ChatRepository $chatRepository): JsonResponse
    {
        $chat = $chatRepository->find($id);

        if (!$chat) {
            return new JsonResponse(['error' => 'Chat not found'], 404);
        }

        $entityManager = $this->getDoctrine()->getManager();
        $entityManager->remove($chat);
        $entityManager->flush();

        return new JsonResponse(['message' => 'Chat deleted'], 200);
    }
}