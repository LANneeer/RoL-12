import asyncio

import asyncpg

from data import config


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.PG_USER,
                password=config.PG_PASSWORD,
                host=config.IP
            )
        )

    async def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS Students(
        id INT NOT NULL,
        username VARCHAR(255) NOT NULL,
        last_name VARCHAR(32) NOT NULL,
        first_name VARCHAR(32) NOT NULL,
        school VARCHAR(32) NOT NULL,
        groups VARCHAR(16) NOT NULL,
        classroom_number INT NOT NULL,
        classroom_letter VARCHAR(4) NOT NULL,
        pargroup INT NOT NULL
        );
        '''
        await self.pool.execute(sql)

        sql = '''
        CREATE TABLE IF NOT EXISTS Teachers(
        id INT NOT NULL,
        username VARCHAR(255) NOT NULL,
        last_name VARCHAR(32) NOT NULL,
        first_name VARCHAR(32) NOT NULL,
        school VARCHAR(32) NOT NULL,
        groups VARCHAR(16) NOT NULL,
        subject VARCHAR(255) NOT NULL,
        pargroup INT NOT NULL
        );
        '''
        await self.pool.execute(sql)

        sql = '''
        CREATE TABLE IF NOT EXISTS Students_work(
        id INT NOT NULL,
        username VARCHAR(255) NOT NULL,
        last_name VARCHAR(32) NOT NULL,
        first_name VARCHAR(32) NOT NULL,
        school VARCHAR(32) NOT NULL,
        groups VARCHAR(16) NOT NULL,
        classroom_number INT NOT NULL,
        classroom_letter VARCHAR(4) NOT NULL,
        pargroup INT NOT NULL,
        subject VARCHAR(255) NOT NULL,
        file_id VARCHAR(255) NOT NULL
        );
        '''
        await self.pool.execute(sql)

        sql = '''
        CREATE TABLE IF NOT EXISTS Teachers_work(
        id INT NOT NULL,
        username VARCHAR(255) NOT NULL,
        school VARCHAR(32) NOT NULL,
        groups VARCHAR(16) NOT NULL,
        classroom_number INT NOT NULL,
        classroom_letter VARCHAR(4) NOT NULL,
        pargroup INT NOT NULL,
        subject VARCHAR(255) NOT NULL,
        file_id VARCHAR(255) NOT NULL
        );
        '''
        await self.pool.execute(sql)

        sql = '''
        CREATE TABLE IF NOT EXISTS Accepting(
        id INT NOT NULL,
        username VARCHAR(255) NOT NULL,
        last_name VARCHAR(32) NOT NULL,
        first_name VARCHAR(32) NOT NULL,
        school VARCHAR(32) NOT NULL,
        groups VARCHAR(16) NOT NULL,
        classroom_number INT NOT NULL,
        classroom_letter VARCHAR(4) NOT NULL,
        pargroup INT NOT NULL,
        subject VARCHAR(255) NOT NULL,
        accepts BOOL NOT NULL
        );
        '''
        await self.pool.execute(sql)

        sql = '''
        CREATE TABLE IF NOT EXISTS ban(id INT NOT NULL, username VARCHAR(255) NOT NULL);
        '''
        await self.pool.execute(sql)

    async def add_ban(self, id: int, username: str):
        sql = 'INSERT INTO ban(id, username) VALUES($1, $2)'
        await self.pool.execute(sql, id, username)

    async def del_ban(self, id: int):
        sql = 'DELETE FROM Students WHERE id = $1'
        await self.pool.execute(sql, id)
        sql = 'DELETE FROM Students_work WHERE id = $1'
        await self.pool.execute(sql, id)

    async def unban(self, id: int):
        sql = 'DELETE FROM ban WHERE id = $1'
        await self.pool.execute(sql, id)

    async def exists_ban(self, id: int):
        sql = 'SELECT * FROM ban WHERE id = $1'
        return bool(len(await self.pool.fetch(sql, id)))

    async def exists_with_username(self, username: str):
        sql = 'SELECT id FROM Students WHERE username = $1'
        return await self.pool.fetchval(sql, username)

    async def exists_with_username_in_ban(self, username: str):
        sql = 'SELECT id FROM ban WHERE username = $1'
        return await self.pool.fetchval(sql, username)

    async def add_students(self, id: int, username: str, last_name: str, first_name: str, school: str, groups: str,
                           classroom_number: int, classroom_letter: str, pargroup: int):
        sql = '''
        INSERT INTO Students(id, username, last_name, first_name, school, groups, 
        classroom_number, classroom_letter, pargroup)
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)
        '''
        await self.pool.execute(sql, id, username, last_name, first_name, school, groups, classroom_number,
                                classroom_letter, pargroup)

    async def add_teachers(self, id: int, username: str, last_name: str, first_name: str, school: str, groups: str,
                           subject: str, pargroup: int):
        sql = '''
        INSERT INTO Teachers(id, username, last_name, first_name, school, groups, subject, pargroup) 
        VALUES($1, $2, $3, $4, $5, $6, $7, $8)
        '''
        await self.pool.execute(sql, id, username, last_name, first_name, school, groups, subject, pargroup)

    async def add_students_work(self, id: int, username: str, last_name: str, first_name: str, school: str, groups: str,
                                classroom_number: int, classroom_letter: str,
                                subject: str, file_id: str, pargroup: int):
        sql = '''
        INSERT INTO Students_work(id, username, last_name, first_name, school, groups,
        classroom_number, classroom_letter, subject, file_id, pargroup) 
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        '''
        await self.pool.execute(sql, id, username, last_name, first_name, school, groups,
                                classroom_number, classroom_letter, subject, file_id, pargroup)

    async def add_teachers_work(self, id: int, username: str, school: str, groups: str, classroom_number: int,
                                classroom_letter: str, subject: str, file_id: str, pargroup: int):
        sql = '''
        INSERT INTO Teachers_work(id, username, school, groups, classroom_number,
         classroom_letter, subject, file_id, pargroup)
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)
        '''
        await self.pool.execute(sql, id, username, school, groups, classroom_number, classroom_letter, subject, file_id,
                                pargroup)

    async def add_students_accepts(self, id: int, username: str, last_name: str, first_name: str, school: str,
                                   group: str,
                                   classroom_number: int,
                                   classroom_letter: str, pargroup: int, subject: str, accepts: bool):
        sql = '''INSERT INTO Accepting(id, username, last_name, first_name, school, groups, classroom_number, 
        classroom_letter, pargroup, subject, accepts)
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        '''
        await self.pool.execute(sql, id, username, last_name, first_name, school, group, classroom_number,
                                classroom_letter, pargroup, subject, accepts)

    async def add_teacher_accepts(self, id: int, username: str, last_name: str, first_name: str, school: str,
                                  group: str,
                                  classroom_number: int,
                                  classroom_letter: str, pargroup: int, subject: str, accepts: bool):
        sql = '''INSERT INTO Accepting(id, username, last_name, first_name, school, groups, classroom_number, 
        classroom_letter, pargroup, subject, accepts)
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        '''
        await self.pool.execute(sql, id, username, last_name, first_name, school, group, classroom_number,
                                classroom_letter, pargroup, subject, accepts)

    async def update_students_accepts(self, id: int, subject: str, accept: bool):
        sql = 'UPDATE Accepting SET accepts = $3 WHERE id = $1 AND subject = $2'
        return await self.pool.execute(sql, id, subject, accept)

    async def update_teacher_accepts(self, id: int, subject: str, school: str, classroom_number: int,
                                     classroom_letter: str, group: str, pargroup: int, accept: bool):
        sql = '''UPDATE Accepting SET accepts = $8 WHERE id = $1 AND subject = $2 AND school = $3 AND
        classroom_number = $4 AND classroom_letter = $5 AND groups = $6 AND pargroup = $7
        '''
        return await self.pool.execute(sql, id, subject, school, classroom_number, classroom_letter, group,
                                       pargroup, accept)

    async def get_teacher_data(self, id: int):
        sql = 'SELECT subject, groups, pargroup, school FROM Teachers WHERE id = $1'
        return await self.pool.fetchrow(sql, id)

    async def get_student_group(self, id: int):
        sql = 'SELECT groups FROM Students WHERE id = $1'
        return await self.pool.fetchval(sql, id)

    async def get_student_data(self, id: int):
        sql = '''SELECT classroom_number, classroom_letter, groups, first_name, last_name, pargroup, username, school
        FROM Students WHERE id = $1'''
        return await self.pool.fetchrow(sql, id)

    async def get_students_work0(self, classroom_number: int,
                                 classroom_letter: str, subject: str, group: str, school: str):
        sql = '''SELECT last_name, first_name, file_id, username, id FROM Students_work 
        WHERE classroom_number = $1 AND classroom_letter = $2 AND 
        subject = $3 AND groups = $4 AND school = $5
        '''
        return await self.pool.fetch(sql, classroom_number, classroom_letter, subject, group, school)

    async def get_students_work(self, classroom_number: int,
                                classroom_letter: str, subject: str, group: str, pargroup: int, school: str):
        sql = '''SELECT last_name, first_name, file_id, username, id FROM Students_work 
        WHERE classroom_number = $1 AND classroom_letter = $2 AND 
        subject = $3 AND groups = $4 AND pargroup = $5 AND school = $6
        '''
        return await self.pool.fetch(sql, classroom_number, classroom_letter, subject, group, pargroup, school)

    async def get_teachers_work(self, classroom_number: int,
                                classroom_letter: str, subject: str, group: str,
                                pargroup: int, school: str):
        sql = '''SELECT file_id, id, username FROM Teachers_work 
        WHERE classroom_number = $1 AND classroom_letter = $2 AND subject = $3 AND groups = $4 AND 
        (pargroup = $5 OR pargroup = 0) AND school = $6
        '''
        return await self.pool.fetch(sql, classroom_number, classroom_letter, subject, group, pargroup, school)

    async def get_teachers_username(self, id: int):
        sql = 'SELECT username FROM Teachers WHERE id = $1'
        return await self.pool.fetchval(sql, id)

    async def get_teachers_pargroup(self, group: str, pargroup: int, school: str, subject: str):
        sql = '''SELECT pargroup FROM Teachers WHERE groups LIKE $1 AND (pargroup = $2 OR pargroup = 0) AND school = $3 
        AND subject LIKE $4
        '''
        return await self.pool.fetchval(sql, group, pargroup, school, subject)

    async def get_teachers_account(self, group: str, school: str, pargroup: int):
        sql = '''SELECT username, subject FROM Teachers WHERE groups LIKE $1 AND school = $2 AND 
        (pargroup = $3 OR pargroup = 0)'''
        return await self.pool.fetch(sql, group, school, pargroup)

    async def exist_students_work(self, subject: str, id: int):
        sql = 'SELECT id FROM Students_work WHERE subject = $1 AND id = $2'
        return bool(len(await self.pool.fetch(sql, subject, id)))

    async def exist_teachers_work(self, subject: str, group: str, pargroup: int,
                                  classroom_number: int, classroom_letter: str, school: str):
        sql = '''SELECT id FROM Teachers_work WHERE subject = $1 AND groups = $2 AND pargroup = $3 
        AND classroom_number = $4 AND classroom_letter = $5 AND school = $6
        '''
        return bool(len(await self.pool.fetch(sql, subject, group, pargroup,
                                              classroom_number, classroom_letter, school)))

    async def get_students_id0(self, classroom_number: int, classroom_letter: str, group: str, school: str):
        sql = '''SELECT id FROM Students WHERE classroom_number = $1 AND classroom_letter = $2 AND groups = $3
        AND school = $4
        '''
        return await self.pool.fetch(sql, classroom_number, classroom_letter, group, school)

    async def get_students_id(self, classroom_number: int, classroom_letter: str,
                              group: str, pargroup: int, school: str):
        sql = '''SELECT id FROM Students WHERE classroom_number = $1 AND classroom_letter = $2 AND groups = $3
        AND pargroup = $4 AND school = $5
        '''
        return await self.pool.fetch(sql, classroom_number, classroom_letter, group, pargroup, school)

    async def get_subject(self, id: int):
        sql = 'SELECT subject FROM Teachers WHERE id = $1'
        return await self.pool.fetchrow(sql, id)

    async def exist_user(self, id: int):
        sql = '''SELECT id FROM Students WHERE id = $1
              UNION SELECT id FROM Teachers WHERE id = $1 '''
        return bool(len(await self.pool.fetch(sql, id)))

    async def exist_student(self, id: int):
        sql = 'SELECT id FROM Students WHERE id = $1'
        return bool(len(await self.pool.fetch(sql, id)))

    async def exist_teacher(self, id: int):
        sql = 'SELECT id FROM Teachers WHERE id = $1'
        return bool(len(await self.pool.fetch(sql, id)))

    async def exist_students_accepts(self, school: str, group: str, classroom_number: int, classroom_letter: str,
                                     pargroup: int, subject: str):
        sql = '''SELECT accepts, id, username, first_name, last_name FROM Accepting WHERE 
        school = $1 AND groups = $2 AND classroom_number = $3 AND
        classroom_letter = $4 AND pargroup = $5 AND subject = $6
        '''
        return await self.pool.fetch(sql, school, group, classroom_number, classroom_letter, pargroup, subject)

    async def exist_open_accepts(self, school: str, group: str, classroom_number: int, classroom_letter: str,
                                 pargroup: int, subject: str, accept: bool):
        sql = '''SELECT id FROM Accepting WHERE 
        school = $1 AND groups = $2 AND classroom_number = $3 AND
        classroom_letter = $4 AND pargroup = $5 AND subject = $6 AND accepts = $7
        '''
        return bool(len(await self.pool.fetch(sql, school, group, classroom_number,
                                              classroom_letter, pargroup, subject, accept)))

    async def exist_open_accepts_for_teachers(self, school: str, group: str, classroom_number: int,
                                              classroom_letter: str, pargroup: int, subject: str, id: int):
        sql = '''SELECT accepts FROM Accepting WHERE 
        school = $1 AND groups = $2 AND classroom_number = $3 AND
        classroom_letter = $4 AND pargroup = $5 AND subject = $6 AND id = $7
        '''
        return await self.pool.fetchval(sql, school, group, classroom_number,
                                        classroom_letter, pargroup, subject, id)

    async def exist_one_students_accepts(self, subject: str, id: int, classroom_number: int, classroom_letter: str,
                                         group: str, pargroup: int):
        sql = '''SELECT accepts FROM Accepting WHERE subject = $1 AND id = $2 AND classroom_number = $3 AND
        classroom_letter = $4 AND groups LIKE $5 AND pargroup = $6
        '''
        return await self.pool.fetchval(sql, subject, id, classroom_number, classroom_letter, group, pargroup)

    async def exist_students_for_work0(self, classroom_number: int, classroom_letter: str, group: str, school: str):
        sql = '''SELECT first_name, last_name, id FROM Students 
              WHERE classroom_number = $1 AND classroom_letter = $2 AND groups = $3 AND school = $4
              '''
        return await self.pool.fetch(sql, classroom_number, classroom_letter,  group, school)

    async def exist_students_for_work1(self, classroom_number: int, classroom_letter: str,
                                       pargroup: int, group: str, school: str):
        sql = '''SELECT first_name, last_name, id FROM Students 
              WHERE classroom_number = $1 AND classroom_letter = $2 AND pargroup = $3 AND groups = $4 AND school = $5
              '''
        return await self.pool.fetch(sql, classroom_number, classroom_letter, pargroup, group, school)

    async def exist_students_for_work2(self, id: int, subject: str):
        sql = 'SELECT id FROM Students_work WHERE id = $1 AND subject = $2'
        return bool(len(await self.pool.fetch(sql, id, subject)))

    async def find_student(self, id: int):
        sql = 'SELECT first_name, last_name FROM Students WHERE id = $1'
        return await self.pool.fetchrow(sql, id)

    async def delete_teachers_work(self, subject: str, group: str, pargroup: int,
                                   classroom_number: int, classroom_letter: str, school: str):
        sql = '''DELETE FROM Teachers_work WHERE subject = $1 AND groups = $2 AND pargroup = $3 
        AND classroom_number = $4 AND classroom_letter = $5 AND school = $6
        '''
        await self.pool.execute(sql, subject, group, pargroup, classroom_number, classroom_letter, school)

    async def delete_students_work(self, subject: str, id: int):
        sql = 'DELETE FROM Students_work WHERE subject = $1 AND id = $2'
        await self.pool.execute(sql, subject, id)

    async def delete_students_file(self, id: int, subject: str, file_id: str):
        sql = '''DELETE FROM Students_work WHERE id = $1 AND subject = $2 AND file_id = $3'''
        await self.pool.execute(sql, id, subject, file_id)

    async def delete_students_accepts(self, id: int, subject: str, pargroup: int, ):
        sql = '''DELETE FROM Accepting WHERE id = $1 AND subject = $2 AND pargroup = $3'''
        await self.pool.execute(sql, id, subject, pargroup)

    async def delete_from_Teachers(self, id: int):
        sql = 'DELETE FROM Teachers WHERE id = $1'
        await self.pool.execute(sql, id)

    async def delete_from_Students(self, id: int):
        sql = 'DELETE FROM Students WHERE id = $1'
        await self.pool.execute(sql, id)
