#!/usr/bin/env python
import os
import sys
from app import create_app, db
from app.models import User

app = create_app()

def init_db():
    """Инициализировать базу данных"""
    with app.app_context():
        print("Создание таблиц в БД...")
        db.create_all()
        print("[OK] База данных инициализирована успешно!")

def create_demo_user():
    """Создать тестового пользователя"""
    with app.app_context():
        # Проверка существования пользователя
        if User.query.filter_by(email='test@example.com').first():
            print("[ERROR] Тестовый пользователь уже существует!")
            return

        user = User(
            full_name='Testovyy pol',
            email='test@example.com',
            iin='12345678901',
            phone='+77123456789'
        )
        user.set_password('password123')

        db.session.add(user)
        db.session.commit()
        print("[OK] Testovyy pol'zovatel' sozdan:")
        print(f"  Email: test@example.com")
        print(f"  Parol': password123")
        print(f"  IIN: 12345678901")

def reset_db():
    """Очистить базу данных"""
    with app.app_context():
        if input("Vy uvereny? Vce dannyje budut poteriany (y/n): ").lower() == 'y':
            db.drop_all()
            db.create_all()
            print("[OK] Baza dannyh ochiscena i perenincializirована!")
        else:
            print("[CANCEL] Otmeneno")

def list_users():
    """Показать список всех пользователей"""
    with app.app_context():
        users = User.query.all()
        if not users:
            print("[ERROR] Pol'zovatelej ne najdeno")
            return

        print("\n=== Spisok polzovatelej ===\n")
        for user in users:
            print(f"ID: {user.id}")
            print(f"Imya: {user.full_name}")
            print(f"Email: {user.email}")
            print(f"IIN: {user.iin if user.iin else 'Ne ukazan'}")
            print(f"Telefon: {user.phone if user.phone else 'Ne ukazan'}")
            print(f"Data registracii: {user.created_at.strftime('%d.%m.%Y %H:%M:%S') if user.created_at else 'Neizvestno'}")
            print("-" * 40)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
Ispolzovanie: python manage.py [komanda]

Komandy:
  init_db       - Inicializirovat' bazу dannyh
  create_demo   - Sozdat' testovogo pol'zovatelya
  reset_db      - Ochisit' bazу dannyh (VNIMANIE!)
  list_users    - Pokazat' spisok vsekh pol'zovatelej
  help          - Pokazat' etu spravku
        """)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'init_db':
        init_db()
    elif command == 'create_demo':
        init_db()
        create_demo_user()
    elif command == 'reset_db':
        reset_db()
    elif command == 'list_users':
        list_users()
    elif command == 'help':
        print("Ispolzujte python manage.py bez argumentov dlya spravki")
    else:
        print(f"[ERROR] Neizvestnaya komanda: {command}")
        sys.exit(1)
