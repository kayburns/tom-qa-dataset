import numpy as np


from clause import Question


#def stringify(story, knowledge, config):
def stringify(story):

    lines = []

    i = 0  # The number of descriptions processed
    j = 0  # The number of lines output

    while True:

        line = story[i].render()

        # Capitalize the line
        line = line[0].upper() + line[1:]

        # Prepend the number
        line = '%d %s' % (i + 1, line)

        # Append support if necessary
        if isinstance(story[i], Question) and story[i].idx_support is not None:
            line += '\t%s' % ', '.join([str(x + 1) for x in story[i].idx_support])

        lines.append(line)

        # Increment counters
        i += 1
        #j += template.clauses #TODO: handle multiple-clause templates
        j += 1

        if i >= len(story):
            break

    return lines
