import textwrap
from hw2_fedaniil.table import generate_latex_table

def test_simple_table():
    example_data = [
        ["Character", "Element of Harmony", "Traits", "Role"],
        ["Twilight Sparkle", "Magic", "Intelligent, studious, organized", "Leader, princess, and learner about friendship"],
        ["Applejack", "Honesty", "Hardworking, dependable, straightforward", "Farm pony, runs Sweet Apple Acres"],
        ["Pinkie Pie", "Laughter", "Energetic, cheerful, spontaneous", "Party planner, brings joy and fun"],
        ["Rarity", "Generosity", "Creative, fashionable, dramatic", "Fashion designer, helps friends look their best"],
        ["Rainbow Dash", "Loyalty", "Brave, competitive, confident", "Pegasus, member of the Wonderbolts"],
        ["Fluttershy", "Kindness", "Gentle, shy, nurturing", "Animal caretaker, empathetic friend"],
    ]

    expected_table = textwrap.dedent(r"""
    \begin{table}[h]
        \centering
        \begin{tabular}{|p{0.25\linewidth}|p{0.25\linewidth}|p{0.25\linewidth}|p{0.25\linewidth}|}
            \hline
            Character & Element of Harmony & Traits & Role \\ \hline
            Twilight Sparkle & Magic & Intelligent, studious, organized & Leader, princess, and learner about friendship \\ \hline
            Applejack & Honesty & Hardworking, dependable, straightforward & Farm pony, runs Sweet Apple Acres \\ \hline
            Pinkie Pie & Laughter & Energetic, cheerful, spontaneous & Party planner, brings joy and fun \\ \hline
            Rarity & Generosity & Creative, fashionable, dramatic & Fashion designer, helps friends look their best \\ \hline
            Rainbow Dash & Loyalty & Brave, competitive, confident & Pegasus, member of the Wonderbolts \\ \hline
            Fluttershy & Kindness & Gentle, shy, nurturing & Animal caretaker, empathetic friend \\ \hline
        \end{tabular}
    \end{table}""").lstrip()

    latex_table = generate_latex_table(example_data)
    assert expected_table == latex_table

def test_table_with_custom_spread():
    example_data = [["head 1", "head 2", "head 3"]]
    example_spread = [0.5, 0.25, 0.25]

    expected_table = textwrap.dedent(r"""
    \begin{table}[h]
        \centering
        \begin{tabular}{|p{0.5\linewidth}|p{0.25\linewidth}|p{0.25\linewidth}|}
            \hline
            head 1 & head 2 & head 3 \\ \hline
        \end{tabular}
    \end{table}""").lstrip()

    latex_table = generate_latex_table(example_data, example_spread)
    print(latex_table)
    assert expected_table == latex_table
