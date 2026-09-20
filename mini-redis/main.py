"""Mini Redis CLI 실행 모듈."""

from mini_redis import MiniRedis


def main():
    """Mini Redis 명령어 입력을 반복해서 처리한다."""
    redis = MiniRedis()

    while True:
        command_line = input("mini-redis> ").strip()

        if not command_line:
            continue

        if command_line.lower() in ("exit", "quit"):
            break

        parts = command_line.split()

        command = parts[0].upper()
        arguments = parts[1:]

        if command == "SET":
            if len(arguments) != 2:
                print(
                    "(error) wrong number of arguments "
                    "for 'SET' command"
                )
                continue

            key = arguments[0]
            value = arguments[1]

            success = redis.set(key, value)

            if success:
                print("OK")
            else:
                print(
                    "(error) OOM command not allowed when "
                    "used_memory > 'maxmemory'"
                )

        elif command == "GET":
            if len(arguments) != 1:
                print("(error) wrong number of arguments for 'GET' command")
                continue

            key = arguments[0]
            value = redis.get(key)

            if value is None:
                print("(nil)")
            else:
                print(f'"{value}"')

        elif command == "DEL":
            if len(arguments) != 1:
                print("(error) wrong number of arguments for 'DEL' command")
                continue

            key = arguments[0]
            result = redis.delete(key)

            print(f"(integer) {result}")

        elif command == "EXISTS":
            if len(arguments) != 1:
                print("(error) wrong number of arguments for 'EXISTS' command")
                continue

            key = arguments[0]
            result = redis.exists(key)

            print(f"(integer) {result}")

        elif command == "DBSIZE":
            if len(arguments) != 0:
                print("(error) wrong number of arguments for 'DBSIZE' command")
                continue

            result = redis.dbsize()

            print(f"(integer) {result}")

        elif command == "KEYS":
            if len(arguments) != 0:
                print("(error) wrong number of arguments for 'KEYS' command")
                continue

            keys = redis.keys()

            if not keys:
                print("(empty array)")
                continue

            for index, key in enumerate(keys, start=1):
                print(f'{index}) "{key}"')

        elif command == "EXPIRE":
            if len(arguments) != 2:
                print("(error) wrong number of arguments for 'EXPIRE' command")
                continue

            key = arguments[0]

            try:
                seconds = int(arguments[1])
            except ValueError:
                print("(error) value is not an integer or out of range")
                continue

            result = redis.expire(key, seconds)

            print(f"(integer) {result}")

        elif command == "TTL":
            if len(arguments) != 1:
                print("(error) wrong number of arguments for 'TTL' command")
                continue

            key = arguments[0]
            result = redis.ttl(key)

            print(f"(integer) {result}")

        elif command == "CONFIG":
            if len(arguments) != 3:
                print("(error) wrong number of arguments for 'CONFIG' command")
                continue

            subcommand = arguments[0].upper()
            option = arguments[1].lower()

            if subcommand != "SET" or option != "maxmemory":
                print("(error) unsupported CONFIG command")
                continue

            try:
                maxmemory = int(arguments[2])
            except ValueError:
                print("(error) value is not an integer or out of range")
                continue

            if maxmemory < 0:
                print("(error) maxmemory must be greater than or equal to 0")
                continue

            redis.set_maxmemory(maxmemory)
            print("OK")

        elif command == "INFO":
            if len(arguments) != 1:
                print("(error) wrong number of arguments for 'INFO' command")
                continue

            section = arguments[0].lower()

            if section != "memory":
                print("(error) unsupported INFO section")
                continue

            print(redis.info_memory())

        else:
            print(f"(error) unknown command '{command}'")


if __name__ == "__main__":
    main()