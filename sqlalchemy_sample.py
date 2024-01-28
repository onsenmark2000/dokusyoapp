from typing import Any, Optional
from sqlalchemy import Integer, String, Select, create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    fullname: Mapped[Optional[str]] = mapped_column(String)


engine = create_engine("sqlite://")  # SQLiteメモリデータベース
session = Session(engine)

# テーブルの作成
Base.metadata.create_all(engine)

# ユーザの作成
nobunaga = User(
    name="nobunaga",
    fullname="Oda Nobunaga"
)
hideyoshi = User(
    name="hideyoshi",
    fullname="Toyotomi Hideyoshi"
)
ieyasu = User(
    name="ieyasu",
    fullname="Tokugawa Ieyasu"
)
session.add_all([nobunaga, hideyoshi, ieyasu])

del_user = session.get(User, 2)
session.delete(del_user)
session.commit()

stmt = Select(User).order_by(User.id)
users = session.execute(stmt)
for user in users:
    print(f"{user.User.id}|{user.User.name}|{user.User.fullname}")

session.close()
