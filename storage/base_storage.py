"""
Abstract Base Storage defining contract for persistence engines.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from models.student import Student

class BaseStorage(ABC):
    @abstractmethod
    def load_students(self) -> List[Student]:
        pass

    @abstractmethod
    def save_students(self, students: List[Student]) -> None:
        pass

    @abstractmethod
    def add_student(self, student: Student) -> None:
        pass

    @abstractmethod
    def get_student(self, student_id: str) -> Optional[Student]:
        pass

    @abstractmethod
    def update_student(self, student: Student) -> None:
        pass

    @abstractmethod
    def delete_student(self, student_id: str, soft_delete: bool = True) -> bool:
        pass