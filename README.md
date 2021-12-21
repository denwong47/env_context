# env_context
 A simple class to manage temporary Environment Variables as a context manager.

 ## env_context.EnvironmentContext
 ## Syntax:
 ```
 env_context.EnvironmentContext(
     replace:Union[
         None,
         Dict[str, str]
     ]=None,
     update:Union[
         None,
         Dict[str, str]
     ]=None,     
 )

 ```
 `replace` will completely replace all environment variables,

 `update` will add or update the provided environment variables instead.

 If both are supplied, it replaces all environment variable with the combination of both dicts.

 If non-dicts are supplied to either of them, that parameter is ignored.

 All environment variables will be reset to the set found at the start of context upon teardown of the context manager, except when env_context.EnvironmentContext.cache_existing_environment() is called within the context.

 ## Usage:
 ```
 with env_context.EnvironmentContext(
     replace:Union[
         None,
         Dict[str, str]
     ]=None,
     update:Union[
         None,
         Dict[str, str]
     ]=None,     
 ):
    do_something_with_the_temporary_nvironment_variables()

 do_something_with_the_original_environment_variables()
 ```

 ## env_context.EnvironmentContext().cache_existing_environment()
 ```
 env_context.EnvironmentContext().cache_existing_environment()
 ```
 Takes no arguments. Replace the cached environment variables with the current set found in os.environ.

 ## env_context.EnvironmentContext().replace()
 ```
 env_context.EnvironmentContext().replace(
     replace:Union[
         None,
         Dict[str, str]
     ]=None,
     push_changes:bool=True,
 )
 ```
 Completely replace all environment variables with the provided set in `replace`.
 `push_changes` is for internal use only; changes will not be applied immediately when set to `False`, until `env_context.EnvironmentContext().__enter__()` is called.

 ## env_context.EnvironmentContext().update()
 ```
 env_context.EnvironmentContext().update(
     update:Union[
         None,
         Dict[str, str]
     ]=None,
     push_changes:bool=True,
 )
 ```
 Updates environment variables with the provided set in `update`.
 `push_changes` is for internal use only; changes will not be applied immediately when set to `False`, until `env_context.EnvironmentContext().__enter__()` is called.