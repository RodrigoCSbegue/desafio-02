class UserService:
    def signup_workflow(self, db, user_data):
        with self.transaction(db):
            # Tenta criar o usuário, se o e-mail já existir, no create_user provavelmente, vai subir um erro e o 'transaction' fará o rollback automaticamente.
            new_user = self.create_user(db, user_data)
            # Se o usuário foi criado com sucesso, cria a conta
            self.create_account(db, user_id=new_user.id)
            return new_user

    def create_account(self, db, user_id):
        # Criar o registro na tabela accounts
        new_account = Account(user_id=user_id, balance=0.0)
        db.add(new_account)