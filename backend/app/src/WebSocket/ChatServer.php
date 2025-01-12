<?php

namespace App\WebSocket;

use App\Entity\Message;
use App\Entity\Chat;
use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Doctrine\ORM\EntityManagerInterface;
use Lexik\Bundle\JWTAuthenticationBundle\Services\JWTTokenManagerInterface;

class ChatServer implements MessageComponentInterface
{
    private $clients;
    private $entityManager;
    private $jwtManager;

    public function __construct(EntityManagerInterface $entityManager, JWTTokenManagerInterface $jwtManager)
    {
        $this->clients = [];
        $this->entityManager = $entityManager;
        $this->jwtManager = $jwtManager;
    }

    public function onOpen(ConnectionInterface $conn)
    {
        $uri = $conn->httpRequest->getUri();
        echo "Connecting to webserver\n";
        echo $uri;
        preg_match('/\/chat\/(\d+)\/connect/', $uri, $matches);

        if (empty($matches)) {
            echo "Invalid WebSocket URL format\n";
            $conn->send(json_encode(['error' => 'Invalid URL format']));
            $conn->close();
            return;
        }

        $chatId = $matches[1];

        $token = $this->getQueryParam($conn, 'token');

        if ($token) {
            try {
                $decoded = $this->jwtManager->decodeFromJsonWebToken($token);
                
                $conn->user = $decoded;
                $conn->chatId = $chatId;

                echo "User {$conn->user['username']} connected to chat {$chatId}\n";
            } catch (\Exception $e) {
                echo "Invalid JWT token\n";
                $conn->send(json_encode(['error' => 'Unauthorized']));
                $conn->close();
                return;
            }
        } else {
            echo "No token provided\n";
            $conn->send(json_encode(['error' => 'Unauthorized']));
            $conn->close();
            return;
        }

        // Store the connection for broadcasting messages
        $this->clients[$conn->resourceId] = $conn;
    }

    public function onClose(ConnectionInterface $conn)
    {
        unset($this->clients[$conn->resourceId]);
    }

    public function onMessage(ConnectionInterface $from, $msg)
    {
        // Handle incoming messages and broadcast them to the chat room
    }

    public function onError(ConnectionInterface $conn, \Exception $e)
    {
        echo "Error: {$e->getMessage()}\n";
        $conn->close();
    }

    private function getQueryParam(ConnectionInterface $conn, $key)
    {
        $url = $conn->httpRequest->getUri();
        $query = parse_url($url, PHP_URL_QUERY);
        parse_str($query, $params);
        return isset($params[$key]) ? $params[$key] : null;
    }
}
