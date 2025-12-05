## Source-to-Ontology Mapping

| Source                        | Field/Element                     | Ontology mapping                                          | Notes / Transformation                                      |
|------------------------------|-----------------------------------|-----------------------------------------------------------|-------------------------------------------------------------|
| SQLite `Students` table      | `student_id`                      | Individual `Student` (identifier)                         | Use `Student/{student_id}` as URI fragment                  |
| SQLite `Students` table      | `first_name`                      | Data property `firstName`                                 | Direct copy                                                 |
| SQLite `Students` table      | `last_name`                       | Data property `lastName`                                  | Direct copy                                                 |
| SQLite `Students` table      | `date_of_birth`                   | Data property `dateOfBirth`                               | Ensure ISO `YYYY-MM-DD` formatting                          |
| SQLite `Students` table      | `major`                           | Data property `major`                                     | Direct copy                                                 |
| SQLite `Courses` table       | `course_id`                       | Individual `Course` (identifier)                          | Use `Course/{course_id}` as URI fragment                    |
| SQLite `Courses` table       | `course_code`                     | Data property `courseCode`                                | Align with XML `courseCode`                                |
| SQLite `Courses` table       | `course_title`                    | Data property `courseTitle`                               | Direct copy                                                 |
| SQLite `Courses` table       | `department`                      | Object property `offeredByDepartment`                     | Map string to `Department` individual                       |
| SQLite `Courses` table       | `credits`                         | Data property `credits`                                   | Integer                                                     |
| SQLite `Enrollments` table   | `enrollment_id`                   | Individual `Enrollment`                                   | Use `Enrollment/{enrollment_id}` as URI fragment            |
| SQLite `Enrollments` table   | `student_id`                      | Object property `hasEnrollment` / `enrolledInCourse`      | Join to `Student`                                           |
| SQLite `Enrollments` table   | `course_id`                       | Object property `enrolledInCourse`                        | Join to `Course`                                            |
| SQLite `Enrollments` table   | `semester`                        | Data property `semester`                                  | Direct copy                                                 |
| SQLite `Enrollments` table   | `year`                            | Data property `year`                                      | Integer                                                     |
| SQLite `Enrollments` table   | `grade`                           | Data property `grade`                                     | Optional (nullable)                                         |
| CSV `student_contacts.csv`   | `student_id`                      | Align to existing `Student` individual                    | Create new `Student` individuals if IDs missing in DB       |
| CSV `student_contacts.csv`   | `full_name`                       | Split into `firstName` + `lastName`                       | Split by space or custom rule                              |
| CSV `student_contacts.csv`   | `email`                           | Data property `email`                                     | Direct copy                                                 |
| CSV `student_contacts.csv`   | `phone`                           | Data property `phone`                                     | Direct copy                                                 |
| CSV `student_contacts.csv`   | `country`                         | Data property `country`                                   | Direct copy                                                 |
| XML `course_catalog.xml`     | `department/@code`                | Data property `departmentCode` for `Department`           | Create / match `Department` individual                      |
| XML `course_catalog.xml`     | `department/@name`                | Data property `departmentName`                            | Direct copy                                                 |
| XML `course` element         | `courseCode`                      | Data property `courseCode`                                | Align with `Course` individuals                             |
| XML `course` element         | `title`                           | Data property `courseTitle`                               | Direct copy                                                 |
| XML `course` element         | `level`                           | Optional data property `courseLevel`                      | Add property if needed                                      |
| XML `course` element         | `credits`                         | Data property `credits`                                   | Cast to integer                                             |
| XML `course` element         | `language`                        | Optional data property `instructionLanguage`              | Add property if needed                                      |


