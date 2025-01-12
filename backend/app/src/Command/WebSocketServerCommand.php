<?php

namespace App\Command;

use App\WebSocket\ChatServer;
use Doctrine\ORM\EntityManagerInterface;
use Ratchet\App;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Lexik\Bundle\JWTAuthenticationBundle\Services\JWTTokenManagerInterface;


class WebSocketServerCommand extends Command
{
    private $entityManager;
    private $jwtManager;

    public function __construct(EntityManagerInterface $entityManager, JWTTokenManagerInterface $jwtManager)
    {
        $this->entityManager = $entityManager;
        $this->jwtManager = $jwtManager;
        parent::__construct();
    }

    protected function configure()
    {
        $this->setName('app:websocket-server')
             ->setDescription('Starts the WebSocket server for chat communication.');
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $chatServer = new ChatServer($this->entityManager, $this->jwtManager);

        $app = new App('0.0.0.0', 9090);
        
        $app->route('', $chatServer, ['*']);

        $output->writeln("WebSocket server started on ws://0.0.0.0:9090");

        $app->run();
    }
}
