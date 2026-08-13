from datetime import datetime

def my_log(func):
    LOG_TEMPLATE = """
        Function {func_name} called:
        {timestamp}
        Arguments: 
        - args: {args}
        - kwargs: {kwargs}
        Execution time: {execution_time}
        """     
    def wrap(*args, **kwargs):
        start = datetime.now() #before
        
        result = func(*args, **kwargs)
        
        end = datetime.now() #after
        execution_time = (end - start).total_seconds()
        
        log = LOG_TEMPLATE.format(
            func_name = func.__name__,
            timestamp = start.strftime("%Y-%m-%d %H:%M:%S"),
            args = args,
            kwargs = kwargs,
            execution_time = f'{execution_time*1000} ms'
        )
        print(log)
        return result
    return wrap

@my_log
def f1(a,b,c = 100):
    pass

f1(1,2,c = 2)
f1(4,2,c = 3)
f1(7,3,c = 5)
f1(7,8)
f1(0,4,c = 3)