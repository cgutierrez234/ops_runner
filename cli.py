from cleanup_config import CleanupConfig

def select_cleanup_config(cleanup_configs: list[CleanupConfig]) ->CleanupConfig:

    # iterate loaded cleanup_configs and create a nice little cutesy menu
    for index, config in enumerate(cleanup_configs):
        print(f"{index + 1}. {config}")

    while True: 

        user_choice = input("Please select your cleanup option(a numeric option you've been provided): ")

        try:
            user_choice = int(user_choice)
            if user_choice < 1 or user_choice > len(cleanup_configs):
                print(f"Your selection needs to to be from the list of options")
                continue
            else:
                break
        except ValueError:
            # print(f"{user_choice} is an invalid type. Please re-enter.")
            continue

    user_choice = user_choice - 1

    return cleanup_configs[user_choice]