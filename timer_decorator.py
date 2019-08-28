def time_it_return(original_function):
    import time
    def wrapper(*args, **kvargs):
        t1 = time.time()
        results = original_function(*args, **kvargs)
        t2 = time.time() - t1
        print(f"{original_function.__name__}:\nLength: {results}\nTime: {t2} sec")
    return wrapper

def time_it(original_function):
    import time
    def wrapper(*args, **kvargs):
        t1 = time.time()
        original_function(*args, **kvargs)
        t2 = time.time() - t1
        print(f"{original_function.__name__}:\nTime: {t2} sec")
    return wrapper
