import pandas as pd
from ete3 import Tree, TreeStyle, AttrFace, faces, NodeStyle
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Function to parse the CSV data and build a tree
def build_tree_from_csv(csv_file):
    df = pd.read_csv(csv_file, sep="\t", header=None)
    df = df[2:]
    tree = Tree()
    for _, row in df.iterrows():
        # Extracting only the taxonomic data (second column)
        lineage = row[1].split("; ")
        current_node = tree.get_tree_root()
        for name in lineage:
            # Remove rank prefixes (e.g., 'k__', 'p__', etc.)
            name = name.split("__")[-1]
            if not name:
                continue
            child = current_node.search_nodes(name=name)
            if not child:
                current_node = current_node.add_child(name=name)
            else:
                current_node = child[0]
    return tree


# Visualization setup
def layout(node):
    if node.is_leaf():
        name_face = AttrFace("name", fsize=10)
        faces.add_face_to_node(name_face, node, column=0, position="aligned")


def style_tree(tree):
    styles = {
        "Archaea": {"bgcolor": "DarkRed"},
        "Bacteria": {"bgcolor": "DarkBlue"},
        "WPS-2": {"bgcolor": "LightCoral"},
        "Lentisphaerae": {"bgcolor": "LightSkyBlue"},
        "Planctomycetes": {"bgcolor": "LightBlue"},
        "Spirochaetes": {"bgcolor": "LightSteelBlue"},
        "Cyanobacteria": {"bgcolor": "LightSeaGreen"},
        "Fibrobacteres": {"bgcolor": "LightGreen"},
        "Tenericutes": {"bgcolor": "LightPink"},
        "Verrucomicrobia": {"bgcolor": "Thistle"},
        "TM7": {"bgcolor": "Plum"},
        "Synergistetes": {"bgcolor": "LightGoldenrodYellow"},
        "Euryarchaeota": {"bgcolor": "IndianRed"},
        "Actinobacteria": {"bgcolor": "LightSalmon"},
        "Proteobacteria": {"bgcolor": "PaleTurquoise"},
        "Fusobacteria": {"bgcolor": "PeachPuff"},
        "Bacteroidetes": {"bgcolor": "Khaki"},
        "Firmicutes": {"bgcolor": "PaleGreen"},
        "Elusimicrobia": {"bgcolor": "PaleVioletRed"},
    }

    for node in tree.traverse():
        applied = False
        for taxon, style in styles.items():
            if taxon in node.name and not applied:
                nstyle = NodeStyle()
                nstyle["bgcolor"] = style["bgcolor"]
                node.set_style(nstyle)
                applied = True
                break  # Stop checking other taxa after the first match

        if not applied:
            # Apply a default style if no taxon matched
            nstyle = NodeStyle()
            nstyle["bgcolor"] = "white"
            node.set_style(nstyle)

        ts = TreeStyle()
        ts.layout_fn = layout
        ts.show_leaf_name = False
        ts.mode = "c"
        ts.root_opening_factor = 1

    return tree, ts, styles


def plot_legend(styles):
    # Create figure and axis objects
    fig, ax = plt.subplots()

    # Create a list to hold the legend elements
    legend_elements = []

    # Loop through the styles dictionary to create legend elements
    for taxon, properties in styles.items():
        color = properties["bgcolor"]
        # Create a patch (rectangle) for each taxon
        patch = mpatches.Patch(color=color, label=taxon)
        legend_elements.append(patch)

    # Add the legend to the plot
    ax.legend(handles=legend_elements, loc="center")

    # Remove axis
    ax.axis("off")

    # Save the figure
    plt.savefig("taxonomy_legend.png", bbox_inches="tight")


if __name__ == "__main__":
    # Specify your CSV file path
    csv_file_path = (
        "/home/piermarco/Documents/Thesis/data/4_taxonomy/q2:types_to_Taxon_table.csv"
    )
    # Build the tree from the CSV data
    t = build_tree_from_csv(csv_file_path)
    # Build the visualization
    t, ts, style = style_tree(t)
    plot_legend(style)
    t.render("node_background.png", w=400, tree_style=ts)
    t.show(tree_style=ts)
