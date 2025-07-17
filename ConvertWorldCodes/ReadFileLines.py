with open("WORLDcodes_no_comments.cpp") as file:
  # read the complete file into a List
  completeTextFile = file.readlines()

  # determine the number of lines in the file
  numLinesInFile = len(completeTextFile)

  # go through the file, one line at a time
# for lineCount in range(numLinesInFile):
  for lineCount in range(1):
    currentLine = completeTextFile[lineCount]
    print(currentLine)

    # go through this line, one character at a time
#   for char in currentLine:
#     print(char)
    for i, char in enumerate(currentLine):
      print(f"Index {i}: {char}")
