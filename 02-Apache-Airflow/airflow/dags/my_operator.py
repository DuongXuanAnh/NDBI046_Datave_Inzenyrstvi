def consumer(arguments, **kwargs):
    print(f"Content: '{arguments}'")
    print(f"Context: {kwargs}")
    return "My result content"