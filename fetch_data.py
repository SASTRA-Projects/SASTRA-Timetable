# These algorithm needs verification

# def break_periods(cursor: Cursor, breaks=True):
# 	cursor.execute("""SELECT `id`, `start_time`, `end_time`
# 							FROM `periods`
# 							WHERE `is_break`=%s""", (breaks,))
# 	return cursor.fetchall()

# def occupied_periods(cursor: Cursor, class_id):
# 	cursor.execute("""SELECT `day`, `period_id`
# 						 	FROM `timetables`
# 						 	JOIN `faculty_teaches_class_id` `FTC`
# 						 	ON `FTC`.`id`=`timetables`.`faculty_teaches_class_id`
# 							WHERE `FTC`.`class_id`=%s""", (class_id,))
# 	return cursor.fetchall()

# def all_periods(cursor):
# 	cursor.execute("""SELECT `days`.`day`, `periods`.`period_id`
# 						 	FROM `days`, `periods`""")
# 	return cursor.fetchall()

# def available_periods(cursor: Cursor, class_id):
# 	return list(set(all_periods()).difference(occupied_periods(class_id)))

# def faculty_id(cursor: Cursor, faculty_teaches_class_id):
# 	cursor.execute("""SELECT `faculty_id`
# 						 	FROM `faculty_teaches_class`
# 						 	WHERE `id`=%s""", (faculty_teaches_class_id,))
# 	return cursor.fetchone()

# def faculty_department(cursor: Cursor, faculty_id):
# 	cursor.execute("""SELECT `name`, `department`
# 						 	FROM `faculties`
# 						 	WHERE `id`=%s""", (faculty_id,))
# 	return cursor.fetchone()

# def course_faculties(cursor: Cursor, course_id):
# 	cursor.execute("""SELECT `FTC`.`faculty_id`
# 						 	FROM `faculty_teaches_class` `FTC`
# 							JOIN `section_course`
# 						 	ON `section_course`.`id`=`FTC`.`section_course_id`
# 							WHERE `section_course`.`course_id`=%s""", (course_id,))
# 	return cursor.fetchall()

# def periods_split_up(cursor: Cursor, course_id):
# 	cursor.execute("""SELECT `L`, `P`, `T`
# 					   		FROM `courses`
# 						 	WHERE `id`=%s""", (course_id,))
# 	return cursor.fetchone()

from argon2 import PasswordHasher, exceptions
from typehints import *

def get_courses(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[bool, int, str]]], ...]:
    cursor.execute("""SELECT * FROM `courses`""")
    return cursor.fetchall()

def get_course(cursor: Cursor, /, *,
               code: Optional[str] = None) -> Optional[Dict[str, Union[bool, int, str]]]:
    cursor.execute("""SELECT `name`, `department`,
                   `credits`, `L`, `P`, `T`,
                   `is_elective` FROM `courses`
                   WHERE `code`=%s""", (code,))
    return cursor.fetchone()

def get_elective_courses(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
    cursor.execute("""SELECT `code`, `name`,
                   `department`, `credits`,
                   `L`, `P`, `T` FROM `courses`
                   WHERE `is_elective`=%s""", (True,))
    return cursor.fetchall()

def get_nonelective_courses(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[bool, int, str]]], ...]:
    cursor.execute("""SELECT `code`, `name`,
                   `department`, `credits`,
                   `L`, `P`, `T` FROM `courses`
                   WHERE `is_elective`=%s""", (False,))
    return cursor.fetchall()

def get_courses_with_lab(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[bool, int, str]]], ...]:
    cursor.execute("""SELECT * FROM `courses`
                   WHERE `P` > %s""", (0,))
    return cursor.fetchall()

def get_courses_without_lab(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[bool, int, str]]], ...]:
    cursor.execute("""SELECT * FROM `courses`
                   WHERE `P`=%s""", (0,))
    return cursor.fetchall()

def get_classes(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[bool, int]]], ...]:
    cursor.execute("""SELECT * FROM `classes`""")
    return cursor.fetchall()

def get_classes_in_building(cursor: Cursor, /,
                            building_id: Optional[int] = None) -> Tuple[Optional[Dict[str, Union[bool, int, str]]], ...]:
    cursor.execute("""SELECT `id`, `room_no`, `capacity`, `is_lab` FROM `classes`
                   WHERE `building_id`=%s""", (building_id,))
    return cursor.fetchall()

def get_lab_classes(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
    cursor.execute("""SELECT `id`, `building_id`, `room_no`, `capacity` FROM `classes`
                   WHERE `is_lab`=%s""", (True,))
    return cursor.fetchall()

def get_non_lab_classes(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
    cursor.execute("""SELECT `id`, `building_id`, `room_no`, `capacity` FROM `classes`
                   WHERE `is_lab`=%s""", (False,))
    return cursor.fetchall()

def get_faculties(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
	cursor.execute("""SELECT * FROM `faculties`""")
	return cursor.fetchall()

def get_faculty(cursor: Cursor, /, *,
                id: Optional[int] = None) -> Optional[Dict[str, Union[int, str]]]:
	cursor.execute("""SELECT `name` FROM `faculties`
				   WHERE `id`=%s""", (id,))
	return cursor.fetchone()

def get_students(cursor: Cursor, /) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
	cursor.execute("""SELECT * FROM `students`""")
	return cursor.fetchall()

def get_student_by_id(cursor: Cursor, /, *,
                      id: Optional[int] = None) -> Optional[Dict[str, Union[int, str]]]:
	cursor.execute("""SELECT `name` FROM `students`
				   WHERE `id`=%s""", (id,))
	return cursor.fetchone()

def get_student(cursor: Cursor, /, *,
                campus_id=None,
                join_year=None,
                programme_id=None,
                roll_no: Optional[int] = None) -> Optional[Dict[str, Union[int, str]]]:
	cursor.execute("""SELECT `name` FROM `students`
				   WHERE `campus_id`=%s
                   AND `join_id`=%s
                   AND `programme_id`=%s
                   AND `roll_no`=%s""",
                   (campus_id, join_year, programme_id, roll_no))
	return cursor.fetchone()

def get_faculty_details(cursor: Cursor, /, *,
                        id: Optional[int] = None,
                        password: Optional[str] = None) -> Optional[Dict[str, Union[float, int, str]]]:
    try:
        cursor.execute("""SELECT * FROM `faculty_view`
                    WHERE `id`=%s""", (id,))
        faculty: Optional[Dict[str, Union[float, int, str]]] = cursor.fetchone()
        if faculty:
            pwd: Union[float, int, str] = faculty["Password"]
        if isinstance(pwd, str) and password:
            ph: PasswordHasher = PasswordHasher()
            ph.verify(pwd, password)
    except exceptions.VerifyMismatchError:
        if faculty and isinstance(pwd, str):
            cursor.execute("""UPDATE `faculty_info`
                           SET `password`=%s""", ph.hash(pwd))
        try:
            del pwd
            if faculty:
                del faculty["password"]
            del ph
            del password
        finally:
            raise AssertionError("Incorrect Password")
    del pwd
    if faculty:
        del faculty["password"]
    del password
    del ph
    return faculty

def get_student_details(cursor: Cursor, /, *, 
                        campus_id: Optional[int] = None,
                        join_year: Optional[int] = None,
                        programme_id: Optional[int] = None,
                        roll_no: Optional[int] = None) -> None:
    return None
