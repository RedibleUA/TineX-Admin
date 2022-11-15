import psycopg2
from config import host, user, password, db_name


def StickerWrite(UserID: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT * FROM public.\"Stickers ADD\" where \"TakenBy\" is NULL and \"ID\" = (SELECT MIN(\"ID\") FROM public.\"Stickers ADD\")"
        )

        rows = cursor.fetchall()
        for r in rows:
            ID = r[1]

        cursor.execute(
            f"UPDATE public.\"Stickers ADD\" SET \"TakenBy\" = {UserID} where \"ID\" = {ID}"
        )
        connection.commit()

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return rows


def StickerCheck(URL: str):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"Stickers\" where \"URL\" = '{URL}'"
        )

        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

        exist = False
        if (count > 0):
            exist = True

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return exist


def StickersLeft():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"Stickers ADD\""
        )

        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return count


def StickerInsert(UserID: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(f"SELECT \"Category\", \"URL\" FROM public.\"Stickers ADD\" where \"TakenBy\" = {UserID}")

        rows = cursor.fetchall()
        for r in rows:
            Category = r[0]
            URL = r[1]

        answer = ''

        if (StickerCheck(URL) == False):
            cursor.execute(f"INSERT INTO public.\"Stickers\"(\"Category\", \"ID\", \"URL\")  VALUES('{Category}', (SELECT MAX(\"ID\") FROM public.\"Stickers\" WHERE \"Category\" = '{Category}') + 1, '{URL}')")
            connection.commit()
            StickerDelete(UserID)
            answer = "Done"
        else:
            StickerDelete(UserID)
            answer = "Already exists"

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return answer


def StickerDelete(UserID: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"DELETE FROM public.\"Stickers ADD\" where \"TakenBy\" = {UserID}"
        )
        connection.commit()

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()


def StickersAllCount():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"Stickers\""
        )

        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return count


def StickersCategoryCount(Category: str):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"Stickers\" where \"Category\" = '{Category}'"
        )

        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return count


def MakeStickerFree(UserID: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"Stickers ADD\" where \"TakenBy\" = {UserID}"
        )

        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

        answer = ''

        if(count > 0):
            cursor.execute(
                f"UPDATE public.\"Stickers ADD\" SET \"TakenBy\" = null where \"TakenBy\" = {UserID}"
            )
            connection.commit()
            answer = 'Done'
        else:
            answer = 'You dont work'


    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return answer


def CheckLevelAdmin(UserID: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"TineX Admins\" where \"UserID\" = {UserID}"
        )

        count = 0
        rows = cursor.fetchall()
        for r in rows:
            count = r[0]


        if (count > 0):
            cursor.execute(f"SELECT \"Level\" FROM public.\"TineX Admins\" where \"UserID\" = {UserID}")

            rows = cursor.fetchall()
            for r in rows:
                Level = r[0]
        else:
            Level = 0



    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return Level


def AddAdmin(Name: str, UserID: int, Level: int, AdminID: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"TineX Admins\" where \"UserID\" = {UserID}"
        )

        count = 0
        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

        AdminLevel = CheckLevelAdmin(AdminID)

        answer = ''

        if (count == 0 and Level < AdminLevel):
            cursor.execute(f"INSERT INTO public.\"TineX Admins\"(\"Name\", \"UserID\", \"Level\") VALUES ('{Name}', {UserID}, {Level});")
            connection.commit()
            answer = 'Done'
        elif  Level >= AdminLevel:
            answer = 'No accesses'
        else:
            answer = 'Already added'



    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return answer


def ChangeLevelAdmin(UserID: int, Level: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"TineX Admins\" where \"UserID\" = {UserID}"
        )

        count = 0
        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

        answer = ''

        if count > 0:
            cursor.execute(
                f"UPDATE public.\"TineX Admins\" SET \"Level\"= {Level} WHERE \"UserID\" = '{UserID}'"
            )
            connection.commit()
            answer = 'Done'
        else:
            answer = 'User missing'



    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()
    return answer


def DeleteAdmin(UserID: int, AdminID: int):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        cursor = connection.cursor()

        cursor.execute(
            f"SELECT count(*) FROM public.\"TineX Admins\" where \"UserID\" = {UserID}"
        )

        count = 0
        rows = cursor.fetchall()
        for r in rows:
            count = r[0]

        answer = ''

        UserLevel = CheckLevelAdmin(UserID)

        AdminLevel = CheckLevelAdmin(AdminID)


        if count > 0 and UserLevel < AdminLevel:
            cursor.execute(
                f"DELETE FROM public.\"TineX Admins\" WHERE \"UserID\" = '{UserID}'"
            )
            connection.commit()
            answer = 'Done'
        elif UserLevel >= AdminLevel:
            answer = 'No accesses'
        else:
            answer = 'User missing'



    except Exception as _ex:
        print("[INFO] Error while working with PosgreSQL", _ex)
    finally:
        if connection:
            cursor.close()
            connection.close()
    return answer

