from markitdown import MarkItDown

md = MarkItDown()

result = md.convert("/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/A_component-based_framework_for_modeling_and_analyzing_probabilistic_real-time_systems.pdf")

with open("paper.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)