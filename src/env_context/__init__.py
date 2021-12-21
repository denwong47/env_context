import os

class EnvironmentContext():
    def __init__(
        self,
        replace:dict=None,
        update:dict=None,
    ):
        self.cache_existing_environment()
        self.replace(replace=replace, push_changes=False)
        self.update(update=update, push_changes=False)

    def cache_existing_environment(self):
        self.existing_environment = dict(os.environ)

    def replace(
        self,
        replace:dict = None,
        push_changes:bool = True,
    )->dict:
        self.new_environment = replace if (isinstance(replace, dict)) else self.existing_environment.copy()

        if (push_changes):
            self.__enter__()

        return self.new_environment
    
    def update(
        self,
        update:dict = None,
        push_changes:bool = True,
    )->dict:
        if (isinstance(update, dict)):
            self.new_environment = {
                **self.new_environment,
                **update,
            }

        if (push_changes):
            self.__enter__()

        return self.new_environment

    def __enter__(self):
        os.environ.clear()
        os.environ.update(self.new_environment)

    def __exit__(self, exc_type, exc_value, exc_tb):
        os.environ.clear()
        os.environ.update(self.existing_environment)


# if __name__=="__main__":
#     with EnvironmentContext(
#         replace={
#             "TEST_WIPE":"Test Wipe"
#             },
#             update={
#             "TEST_ENVVAR":"Test Value"
#         }) as manager:
#         print (os.environ)
#         print (os.environ.get('TEST_ENVVAR'))
    
#     print (os.environ.get('TEST_ENVVAR'))
#     print (os.environ)