<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20250108225648 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE chat ADD chat_owner_id INT NOT NULL');
        $this->addSql('ALTER TABLE chat ADD CONSTRAINT FK_659DF2AA4A1EB6C9 FOREIGN KEY (chat_owner_id) REFERENCES `user` (id)');
        $this->addSql('CREATE INDEX IDX_659DF2AA4A1EB6C9 ON chat (chat_owner_id)');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE chat DROP FOREIGN KEY FK_659DF2AA4A1EB6C9');
        $this->addSql('DROP INDEX IDX_659DF2AA4A1EB6C9 ON chat');
        $this->addSql('ALTER TABLE chat DROP chat_owner_id');
    }
}
