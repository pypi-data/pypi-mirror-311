from datetime import datetime


def decorated_text(text, style=0, text_color=37, background_color=40):
    return f"\033[{style};{text_color};{background_color}m{text}\033[0m"


def console_logger(func):
    def decorated(*args, **kwargs):
        result = func(*args, **kwargs)

        now = datetime.now()
        print(decorated_text("Function invoked at: " + now.strftime("%H:%M:%S"), 4, 32, 40))
        print(decorated_text("Result: " + result, 1, 32, 40))

        return result

    return decorated


def file_logger(log_file):
    def decorator(func):
        def decorated(*args, **kwargs):
            result = func(*args, **kwargs)

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

            # Write log to the specified file
            with open(log_file, "a") as file:
                file.write(f"Function '{func.__name__}' invoked at: {timestamp}\n")
                file.write(f"Result: {result}\n")
                file.write("-" * 50 + "\n")

            return result

        return decorated

    return decorator
