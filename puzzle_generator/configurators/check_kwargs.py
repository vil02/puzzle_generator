def check_kwargs(allowed_params, **kwargs) -> None:
    for cur_param in kwargs:
        if cur_param not in allowed_params:
            raise TypeError(
                f"{cur_param} is an invalid keyword argument. "
                f"Valid arguments are {allowed_params}."
            )
