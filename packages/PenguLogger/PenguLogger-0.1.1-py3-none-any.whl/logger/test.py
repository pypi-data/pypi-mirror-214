from logger import Logger

def main():
    logger = Logger("test_log.log")
    log_id = logger.log("This is a test log")
    print("Generated log with id:", log_id)

    print("All logs:")
    print(logger.read_all_logs())

    print("Log with id:")
    print(logger.getLogWithId(log_id))

    logger.clear_all_logs()
    print("All logs after clearing:")
    print(logger.read_all_logs())

if __name__ == "__main__":
    main()
