<?php

namespace App\Command;

use App\WebSocket\Chat;
use Ratchet\Http\HttpServer;
use Ratchet\Server\IoServer;
use Ratchet\WebSocket\WsServer;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;



class WSServerCommand extends Command
{
    public function __construct()
    {
        parent::__construct();
    }
    
    protected function configure()
    {
        $this->setName('app:websocket-server-test')
             ->setDescription('Starts the WebSocket server for chat communication.');
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {   
        $output->writeln('Starting WebSocket server...');
        $server = IoServer::factory(
            new HttpServer(
                new WsServer(
                    new Chat()
                )
            ),
            9090
        );
        $server->run();
        $output->writeln("WebSocket server started on ws://0.0.0.0:9090");
    }
}
