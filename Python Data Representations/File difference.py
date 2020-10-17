

"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    if line1 == line2:
        return IDENTICAL
    minlen = min(len(line1), len(line2))
    for num in range(minlen):
        if line1[num] != line2[num]:
            return num
    return minlen 

# =============================================================================
# l1 = "abcbb"
# l2 = "abc"
# print(singleline_diff(l1, l2))
# =============================================================================

def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    if idx not in range(min(len(line1), len(line2))+1):
        return ""
    if "\n" in line1 or "\r" in line1 or "\n" in line2 or "\r" in line2:
        return ""
    sep = "=" * idx + "^"
    return (line1 + "\n" + sep + "\n" + line2 +"\n")

# =============================================================================
# a = "abd"
# b = "abc"
# c = singleline_diff(a, b)
# print(singleline_diff_format(a, b, 1))
# =============================================================================

def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    if lines1 == lines2:
        return (IDENTICAL, IDENTICAL)
    minlen = min(len(lines1), len(lines2))
    for num in range(minlen):
        if lines1[num] != lines2[num]:
            return (num, singleline_diff(lines1[num], lines2[num]))
    return (minlen, 0)

# =============================================================================
# lines1 = ["acc","ab","a"]
# lines2 = ["acc","ac"]
# print(multiline_diff(lines1, lines2))
# =============================================================================


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    res = []
    data = open(filename, "rt")
    for line in data:
        if "\n" in line:
            res.append(line[:-1])
        else:
            res.append(line)
    data.close()
    return res

# =============================================================================
# filename = "hm2.txt"
# print(get_file_lines(filename))
# =============================================================================

def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    list1 = get_file_lines(filename1)
    list2 = get_file_lines(filename2)
    if list1 == list2:
        return "No differences\n"
    line = multiline_diff(list1, list2)[0]
    idx = multiline_diff(list1, list2)[1]
    line1 = "Line " + str(line) + ":\n"
    if line == len(list1):
        list1.append("")
    if line == len(list2):
        list2.append("")
    return (line1 + singleline_diff_format(list1[line], list2[line], idx))

# =============================================================================
# filename1 = "hm1.txt"
# filename2 = "hm2.txt"
# print(file_diff_format(filename1, filename2))
# =============================================================================
