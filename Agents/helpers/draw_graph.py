
from IPython.display import Image, display


def draw_graph(graph , name="graph_image"):
    graph_image = graph.get_graph(xray=True).draw_mermaid_png()
    with open("graph_image.png", "wb") as f:
        f.write(graph_image)
    display(Image(f"{name}.png"))