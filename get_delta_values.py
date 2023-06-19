import datetime


def get_delta_values(current_time, schedule_time):
    """
    Get the delta values for the current time and schedule time.

    Args:
        current_time (datetime.datetime): The current time.
        schedule_time (datetime.datetime): The schedule time.

    Returns:
        tuple: The delta values for the start and end times.
    """

    start_time = current_time - schedule_time
    end_time = current_time

    return start_time, end_time


def main():
    """
    Get the delta values and print them.
    """

    current_time = datetime.datetime.now()
    schedule_time = datetime.datetime.strptime("08:00:00", "%H:%M:%S")

    start_time, end_time = get_delta_values(current_time, schedule_time)

    print(start_time)
    print(end_time)


if __name__ == "__main__":
    main()
