<?php

namespace App\Command;

use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class UpdateUserRolesCommand extends Command
{
    private $entityManager;

    public function __construct(EntityManagerInterface $entityManager)
    {
        parent::__construct();
        $this->entityManager = $entityManager;
    }

    protected static $defaultName = 'app:update-user-roles';

    protected function configure()
    {
        $this->setDescription('Update all users with null roles to empty roles array.');
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        // Find all users with null roles
        $users = $this->entityManager->getRepository(User::class)->findBy(['roles' => null]);

        // Iterate through each user and set their roles to an empty array
        foreach ($users as $user) {
            $user->setRoles([]);  // Set empty roles array
            $this->entityManager->persist($user);
        }

        // Flush the changes to the database
        $this->entityManager->flush();

        $output->writeln('User roles updated successfully!');

        return Command::SUCCESS;
    }
}