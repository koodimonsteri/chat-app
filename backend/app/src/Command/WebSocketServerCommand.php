<?php

namespace App\Command;

use App\WebSocket\ChatServer;
use Doctrine\ORM\EntityManagerInterface;
use Lexik\Bundle\JWTAuthenticationBundle\Services\JWTTokenManagerInterface;
use Ratchet\Server\IoServer;
use Ratchet\WebSocket\WsServer;
use React\EventLoop\Loop;
use React\Socket\Server as ReactServer;
#use React\Socket\SecureServer;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;


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
        $output->writeln('Starting WebSocket server...');
        #$sslCert = getenv('SSL_CERT_PATH') ?: '/var/www/html/config/ssl/certificate.crt';
        #$sslKey = getenv('SSL_KEY_PATH') ?: '/var/www/html/config/ssl/private.key';
        #if (!file_exists($sslCert) || !file_exists($sslKey)) {
        #    $output->writeln("<error>SSL certificate or private key is missing!</error>");
        #    return 1;
        #}
        #$output->writeln("SSL certificate and private key found. Proceeding...");

        $chatServer = new ChatServer($this->entityManager, $this->jwtManager);

        $output->writeln('Initializing Event Loop...');
        try {
            #Loop::setDefaultLoop(Loop::get());
            $loop = Loop::get();
            $output->writeln('Event loop created successfully.');
        } catch (\Exception $e) {
            $output->writeln("<error>Error creating event loop: {$e->getMessage()}</error>");
            return 1;
        }

        $output->writeln('Creating React server...');
        try {
            $socket = new ReactServer('0.0.0.0:9090', $loop);
            $output->writeln('React socket server created successfully.');
        } catch (\Exception $e) {
            $output->writeln("<error>Error creating React socket server: {$e->getMessage()}</error>");
            return 1;
        }

        #$output->writeln('Creating secure WebSocket server with SSL...');
        #try {
        #    $secureSocket = new SecureServer($socket, $loop, [
        #        'ssl' => [
        #            'local_cert' => $sslCert,
        #            'local_pk' => $sslKey,
        #            'verify_peer' => false,
        #        ]
        #    ]);
        #    #$output->writeln('Secure WebSocket server created successfully.');
        #} catch (\Exception $e) {
        #    $output->writeln("<error>Error creating secure WebSocket server: {$e->getMessage()}</error>");
        #    return 1;
        #}

        try {
            $server = new IoServer(
                new WsServer($chatServer),
                $socket,
                $loop
            );
            $output->writeln('IoServer created successfully.');
        } catch (\Exception $e) {
            $output->writeln("<error>Error creating IoServer: {$e->getMessage()}</error>");
            return 1;
        }
        
        $output->writeln("WebSocket server started on ws://0.0.0.0:9090");

        $server->run();
    }
}
