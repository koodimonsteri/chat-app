<?php

namespace App\Repository;

use App\Entity\User;
use App\Entity\UserChat;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<UserChat>
 */
class UserChatRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, UserChat::class);
    }

    public function findByUser(User $user): array
    {
        return $this->createQueryBuilder('uc')
            ->innerJoin('uc.chat', 'c')
            ->addSelect('c')
            ->where('uc.user = :user')
            ->setParameter('user', $user)
            ->getQuery()
            ->getResult();
    }

    public function findByUserAndChat(User $user, int $chatId)
    {
        return $this->createQueryBuilder('uc')
            ->innerJoin('uc.chat', 'c')
            ->where('uc.user = :user')
            ->andWhere('uc.chat = :chatId')
            ->setParameter('user', $user)
            ->setParameter('chatId', $chatId)
            ->getQuery()
            ->getOneOrNullResult();
    }

    public function findOneByUserAndChatGuid(User $user, string $guid): ?UserChat
    {
        return $this->createQueryBuilder('uc')
            ->join('uc.chat', 'c')
            ->where('uc.user = :user')
            ->andWhere('c.guid = :guid')
            ->setParameter('user', $user)
            ->setParameter('guid', $guid)
            ->getQuery()
            ->getOneOrNullResult();
    }

    //    /**
    //     * @return UserChat[] Returns an array of UserChat objects
    //     */
    //    public function findByExampleField($value): array
    //    {
    //        return $this->createQueryBuilder('u')
    //            ->andWhere('u.exampleField = :val')
    //            ->setParameter('val', $value)
    //            ->orderBy('u.id', 'ASC')
    //            ->setMaxResults(10)
    //            ->getQuery()
    //            ->getResult()
    //        ;
    //    }

    //    public function findOneBySomeField($value): ?UserChat
    //    {
    //        return $this->createQueryBuilder('u')
    //            ->andWhere('u.exampleField = :val')
    //            ->setParameter('val', $value)
    //            ->getQuery()
    //            ->getOneOrNullResult()
    //        ;
    //    }
}
