from database.db import get_connection


def get_or_create_pipeline(name, provider):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pipelines (name, provider)
                VALUES (%s, %s)
                ON CONFLICT (name, provider)
                DO UPDATE SET name = EXCLUDED.name
                RETURNING pipeline_id;
                """,
                (name, provider)
            )

            pipeline_id = cursor.fetchone()[0]

        connection.commit()

        return pipeline_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def insert_build(
    pipeline_id,
    build_number,
    status,
    duration_seconds,
    timestamp,
    url
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO builds (
                    pipeline_id,
                    build_number,
                    status,
                    duration_seconds,
                    timestamp,
                    url
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (pipeline_id, build_number)
                DO NOTHING;
                """,
                (
                    pipeline_id,
                    build_number,
                    status,
                    duration_seconds,
                    timestamp,
                    url
                )
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
