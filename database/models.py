from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    present = Column(Boolean, nullable=False)
    good_perf = Column(Boolean, nullable=False)
    good_behave = Column(Boolean, nullable=False)
    perf_comment = Column(Text)
    behave_comment = Column(Text)
    
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="assessments")
    
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_email = Column(String, nullable=True)
    
    class_id = Column(Integer, ForeignKey('classes.id'))
    class_ = relationship("Class", back_populates="students")
    
    assessments = relationship("Assessment", cascade="all, delete-orphan", back_populates="student")
    
class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="classes")
    
    students = relationship("Student", cascade="all, delete-orphan", back_populates="class_")
    
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    
    classes = relationship("Class", cascade="all, delete-orphan", back_populates="teacher")
    