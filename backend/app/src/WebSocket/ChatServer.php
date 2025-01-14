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
        echo "New connection {$conn->resourceId}\n";
    
        $headers = $conn->httpRequest->getHeaders();
        echo "Headers: " . print_r($headers, true) . "\n";
    }

    public function onMessage(ConnectionInterface $from, $msg)
    {   
        echo "New message!\n";
        $data = json_decode($msg, true);

        if (isset($data['token'])) {
            try {
                $decoded = $this->jwtManager->decode($data['token']);
                if (!$decoded) {
                    $from->send("Invalid token.");
                    $from->close();
                    return;
                }

                $from->user = $decoded;
                $from->send("Authentication successful.");
            } catch (ExpiredException $e) {
                $from->send("Token has expired.");
                $from->close();
                return;
            } catch (\Exception $e) {
                $from->send("Authentication failed: " . $e->getMessage());
                $from->close();
                return;
            }
        }

        if (isset($data['message'])) {
            $this->sendMessageToAll($data['message']);
        }
    }

    public function onClose(ConnectionInterface $conn)
    {
        echo "Connection {$conn->resourceId} has disconnected\n";
    }

    public function onError(ConnectionInterface $conn, \Exception $e)
    {
        echo "An error occurred: {$e->getMessage()}\n";
    }
}
