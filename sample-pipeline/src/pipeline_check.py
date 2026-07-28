def check_pipeline_status(successful_jobs, failed_jobs):
    total = successful_jobs + failed_jobs

    if total == 0:
        return 0

    return round((successful_jobs / total) * 100, 2)


if __name__ == "__main__":
    rate = check_pipeline_status(9, 1)
    print(f"Pipeline success rate: {rate}%")
