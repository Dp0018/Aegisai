import asyncio
import os
import sys
import argparse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Add parent directory to sys.path so app imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole


async def list_users(db_url: str):
    engine = create_async_engine(db_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        result = await session.execute(select(User).order_by(User.created_at))
        users = result.scalars().all()
        if not users:
            print("No users found in the database. The database is empty.")
            return

        print(f"\nFound {len(users)} user(s) in the database:")
        print("-" * 70)
        print(f"{'Email':<35} {'Role':<15} {'Active':<8} {'Created At'}")
        print("-" * 70)
        for u in users:
            print(f"{u.email:<35} {u.role.value if hasattr(u.role, 'value') else str(u.role):<15} {str(u.is_active):<8} {u.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)

    await engine.dispose()


async def create_or_reset_admin(db_url: str, email: str, password: str, full_name: str = "System Administrator"):
    engine = create_async_engine(db_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        hashed_pw = get_password_hash(password)

        if user:
            user.hashed_password = hashed_pw
            user.role = UserRole.ADMIN
            user.is_active = True
            if full_name:
                user.full_name = full_name
            await session.commit()
            print(f"\nSuccess: Updated existing user '{email}' to ADMIN with the new password.")
        else:
            new_user = User(
                email=email,
                hashed_password=hashed_pw,
                full_name=full_name,
                role=UserRole.ADMIN,
                is_active=True
            )
            session.add(new_user)
            await session.commit()
            print(f"\nSuccess: Created new ADMIN user '{email}'.")

    await engine.dispose()


def main():
    parser = argparse.ArgumentParser(description="AegisAI User Management & Admin Bootstrap Utility")
    parser.add_argument("--database-url", default=None, help="Database connection URL (defaults to DATABASE_URL in environment)")
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: list
    subparsers.add_parser("list", help="List all registered platform users")

    # Subcommand: create-admin
    create_parser = subparsers.add_parser("create-admin", help="Create or reset an administrator account")
    create_parser.add_argument("--email", required=True, help="Administrator email address")
    create_parser.add_argument("--password", required=True, help="Administrator password")
    create_parser.add_argument("--name", default="Administrator", help="Administrator full name")

    args = parser.parse_args()

    db_url = args.database_url or os.getenv("DATABASE_URL") or settings.DATABASE_URL
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    if args.command == "list":
        asyncio.run(list_users(db_url))
    elif args.command == "create-admin":
        asyncio.run(create_or_reset_admin(db_url, args.email, args.password, args.name))


if __name__ == "__main__":
    main()
