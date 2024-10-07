def print_console(msg):
    try:
        print(msg)
        return True



    except:
        exit(1)

class Logger:
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, message):
        with open(self.filename, 'at') as log_file:
            log_file.write(message)
            log_file.write('\n')



