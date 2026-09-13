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
                DO NOTHING
                RETURNING build_id;
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

            result = cursor.fetchone()

        connection.commit()

        return result is not None

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def get_all_builds():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    p.name,
                    p.provider,
                    b.build_number,
                    b.status,
                    b.duration_seconds,
                    b.timestamp,
                    b.url
                FROM builds b
                JOIN pipelines p
                    ON b.pipeline_id = p.pipeline_id
                ORDER BY b.build_number;
                """
            )

            rows = cursor.fetchall()

            return [
                {
                    "pipeline": row[0],
                    "provider": row[1],
                    "build_number": row[2],
                    "status": row[3],
                    "duration_seconds": row[4],
                    "timestamp": row[5].isoformat(),
                    "url": row[6]
                }
                for row in rows
            ]

    finally:
        connection.close()
