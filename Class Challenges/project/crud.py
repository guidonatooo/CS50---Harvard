from typing import List
from pathlib import Path
from datetime import datetime

from sqlalchemy import create_engine, String, Boolean, Integer, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

from werkzeug.security import generate_password_hash, check_password_hash

current_folder = Path(__file__).parent
PATH_TO_DB = current_folder / 'db_users.sqlite'

class Base(DeclarativeBase):
    pass

class UserVacation(Base):
    __tablename__ = 'user_vacation'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(50))
    manager_access: Mapped[bool] = mapped_column(default=False)
    start_in_company: Mapped[str] = mapped_column(String(50))
    profession: Mapped[str] = mapped_column(String(50))
    vacations: Mapped[List["VacationEvent"]] = relationship(
        back_populates='parent',
        lazy='subquery'
    )

    def __repr__(self):
        return f"UserVacation({self.id=}, {self.name=})"

    def define_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def add_vacation(self, start_vacation, end_vacation):
        total_days = (
            datetime.strptime(end_vacation, '%Y-%m-%d')
            - datetime.strptime(start_vacation, '%Y-%m-%d')
        ).days + 1
        with Session(bind=engine) as session:
            vacation = VacationEvent(
                parent_id=self.id,
                start_vacation=start_vacation,
                end_vacation=end_vacation,
                total_days=total_days
            )
            session.add(vacation)
            session.commit()

    def vacation_list(self):
        list_events = []
        for event in self.vacations:
            list_events.append({
                'title': f'Vacation of {self.name}',
                'start': event.start_vacation,
                'end': event.end_vacation,
                'color': self.get_color_by_profession()
            })
        return list_events

    def get_color_by_profession(self):
        colors = {
            "veterinarian": "green",
            "nurse": "blue",
            "intern": "purple"
        }
        return colors.get(self.profession.lower(), "gray")

def request_vacation_days(self):
    total_days = (
        datetime.now()
        - datetime.strptime(self.start_in_company, '%Y-%m-%d')
    ).days * (30 / 365)
    taken_days = sum(event.total_days for event in self.vacations)
    return total_days - taken_days

class VacationEvent(Base):
    __tablename__ = 'vacation_event'

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('user_vacation.id'))
    parent: Mapped[UserVacation] = relationship(back_populates='vacations', lazy='subquery')
    start_vacation: Mapped[str] = mapped_column(String(50))
    end_vacation: Mapped[str] = mapped_column(String(50))
    total_days: Mapped[int] = mapped_column(Integer())

engine = create_engine(f'sqlite:///{PATH_TO_DB}')
Base.metadata.create_all(bind=engine)

# CRUD Functions
def create_user(name, password, email, profession, **kwargs):
    with Session(bind=engine) as session:
        user = UserVacation(
            name=name,
            email=email,
            profession=profession,
            **kwargs
        )
        user.define_password(password)
        session.add(user)
        session.commit()
        print(f"User '{name}' created successfully.")

def read_all_users():
    with Session(bind=engine) as session:
        sql_command = select(UserVacation)
        users = session.execute(sql_command).fetchall()
        if users:
            print("Users retrieved successfully.")
            return [user[0] for user in users]
        else:
            print("No users found.")
            return []


def read_user_by_id(user_id):
    with Session(bind=engine) as session:
        user = session.get(UserVacation, user_id)
        if user:
            print(f"User with ID {user_id} found: {user}")
            return user
        else:
            print(f"User with ID {user_id} not found.")
            return None


def update_user(user_id, **kwargs):
    with Session(bind=engine) as session:
        user = session.get(UserVacation, user_id)
        if user:
            for key, value in kwargs.items():
                if key == 'password':
                    user.define_password(value)
                else:
                    setattr(user, key, value)
            session.commit()
            print(f"User with ID {user_id} updated successfully.")
        else:
            print(f"User with ID {user_id} not found.")


def delete_user(user_id):
    with Session(bind=engine) as session:
        user = session.get(UserVacation, user_id)
        if user:
            session.delete(user)
            session.commit()
            print(f"User with ID {user_id} deleted successfully.")
        else:
            print(f"User with ID {user_id} not found.")


def view_plain_password(user_id):
    user = read_user_by_id(user_id)
    if user:
        try:
            password = user.get_plain_password()
            print(f"Plain password for user ID {user_id}: {password}")
            return password
        except PermissionError as e:
            print(e)
    else:
        print(f"User with ID {user_id} not found.")

if __name__ == "__main__":

    create_user(
        name="Guilherme Donato",
        password="1234",
        email="gui@exemplo.com",
        profession="veterinarian",
        manager_access=True,
        start_in_company="2022-01-01"
    )
