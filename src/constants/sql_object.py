GET_USER_DETAIL_BY_NAME = """SELECT id
                            ,username
                            ,display_name
                            ,email
                            ,expiration_date
                            ,last_active
                        FROM userdetail
                        WHERE username = '{}'
                            AND (expiration_date IS NULL OR strftime('%s', expiration_date) >= strftime('%s', '{}'))"""

GET_USER_PASSWORD = """SELECT password
                        FROM userdetail
                        WHERE username = '{}'"""

UPDATE_LAST_ACTIVE_USER_BY_NAME = """UPDATE userdetail
                                    SET last_active = '{}'
                                    WHERE username = '{}'
                                        AND (expiration_date IS NULL OR strftime('%s', expiration_date) >= strftime('%s', '{}'))"""
