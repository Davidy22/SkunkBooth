# Text attributes for use when printing to the Screen.
# 1-4 correspond to ASCIImatics attribute codes, 5+ are derivative attributes not
# supported by ASCIImatics
A_BOLD = 1
A_NORMAL = 2
A_REVERSE = 3
A_UNDERLINE = 4
A_BOLD_REVERSE = 5
A_BOLD_UNDERLINE = 6
A_UNDERLINE_REVERSE = 7
A_BOLD_REVERSE_UNDERLINE = 8
L_REVERSE = [
    A_REVERSE,
    A_BOLD_REVERSE,
    A_UNDERLINE_REVERSE,
    A_BOLD_REVERSE_UNDERLINE,
]
L_BOLD = [
    A_BOLD,
    A_BOLD_REVERSE,
    A_BOLD_UNDERLINE,
    A_BOLD_REVERSE_UNDERLINE,
]
L_UNDERLINE = [
    A_UNDERLINE,
    A_BOLD_UNDERLINE,
    A_UNDERLINE_REVERSE,
    A_BOLD_REVERSE_UNDERLINE,
]
