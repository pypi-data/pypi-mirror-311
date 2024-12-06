from chinus_tools.prints.prints import br_print


def br_input(*lines, prompt=None):
    br_print(*lines)
    return input(prompt)
