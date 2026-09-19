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
    """
    Insert a new build or update an existing build when its
    status changes.

    Returns:
        ("new", None)
        ("updated", previous_status)
        ("unchanged", previous_status)
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT status
                FROM builds
                WHERE pipeline_id = %s
                  AND build_number = %s;
                """,
                (pipeline_id, build_number)
            )

            existing = cursor.fetchone()

            # New pipeline run
            if existing is None:
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
                    VALUES (%s, %s, %s, %s, %s, %s);
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

                return "new", None

            previous_status = existing[0]

            # Existing run changed status
            if previous_status != status:
                cursor.execute(
                    """
                    UPDATE builds
                    SET
                        status = %s,
                        duration_seconds = %s,
                        timestamp = %s,
                        url = %s
                    WHERE pipeline_id = %s
                      AND build_number = %s;
                    """,
                    (
                        status,
                        duration_seconds,
                        timestamp,
                        url,
                        pipeline_id,
                        build_number
                    )
                )

                connection.commit()

                return "updated", previous_status

            # Nothing changed
            connection.commit()

            return "unchanged", previous_status

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
```

