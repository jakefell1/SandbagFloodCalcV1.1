import streamlit as st
import math
import matplotlib.pyplot as plt

def plot_wall_cross_section_with_bags(height, bag_height, w_base, w_top, bag_width):
    """
    Plots a cross-section of a trapezoidal sandbag wall from bottom (y=0) to top (y=height),
    showing each 'bag' as a small rectangle.

    :param height: total height of the wall (m).
    :param bag_height: height of one sandbag in cross-section (m).
    :param w_base: width of the wall at the bottom (m).
    :param w_top: width of the wall at the top (m).
    :param bag_width: width of each bag in cross-section (m).
    """

    # 1. Compute the number of layers (one bag per layer)
    n_layers = math.ceil(height / bag_height)
    layer_thickness = height / n_layers  # each layer's actual thickness

    fig, ax = plt.subplots(figsize=(6, 4))

    # We'll loop through each layer from bottom (i=0) to top (i = n_layers-1)
    for i in range(n_layers):
        # The bottom and top y-coordinates of this layer
        y_bottom = i * layer_thickness
        y_top = (i + 1) * layer_thickness

        # Interpolate the width at the bottom and top of this layer
        # fraction from 0 (at bottom) to 1 (at top)
        frac_bottom = y_bottom / height if height != 0 else 0
        frac_top = y_top / height if height != 0 else 1

        # The trapezoid's bottom and top widths:
        width_bottom = w_base + (w_top - w_base) * frac_bottom
        width_top    = w_base + (w_top - w_base) * frac_top

        # For simplicity, approximate the layer's width as the average
        # of the bottom and top widths:
        avg_layer_width = (width_bottom + width_top) / 2.0

        # 2. Compute how many bags fit across this layer
        # We'll assume each bag in cross-section is 'bag_width' wide
        n_bags_layer = math.floor(avg_layer_width / bag_width)

        # 3. Total width occupied by those bags
        total_bags_width = n_bags_layer * bag_width

        # 4. Let's center these bags horizontally.
        # The leftmost bag’s center = -total_bags_width/2 + bag_width/2, etc.
        # We'll define x_start as the center of the first bag
        x_start = -(total_bags_width / 2.0) + (bag_width / 2.0)

        # 5. Plot each bag in this layer
        for b in range(n_bags_layer):
            # Center of this bag
            x_center = x_start + b * bag_width

            # Left and right of this bag
            x_left = x_center - bag_width / 2.0
            x_right = x_center + bag_width / 2.0

            # We'll treat the layer thickness as the bag height in the plot
            # (Though it might differ slightly if partial layer thickness remains)
            # The bag extends from y_bottom to y_top
            xs = [x_left, x_right, x_right, x_left, x_left]
            ys = [y_bottom, y_bottom, y_top, y_top, y_bottom]

            ax.fill(xs, ys, color="skyblue", alpha=0.6, edgecolor="blue")

    # Decorate the plot
    ax.set_title(f"Sandbag Wall Cross-Section\nHeight={height} m, Base={w_base} m, Top={w_top} m")
    ax.set_xlabel("Horizontal distance (m)")
    ax.set_ylabel("Height (m)")

    # Set the X range to at least the base width
    half_base = max(w_base, w_top) / 2.0
    ax.set_xlim(-half_base * 1.2, half_base * 1.2)
    ax.set_ylim(0, height * 1.1)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.3)

    return fig

def main():
    st.title("Sandbag Wall Cross-Section (Individual Bags)")
    st.write("Visualize each bag in the cross-section of a trapezoidal wall.")

    # Inputs
    height = st.number_input("Total Wall Height (m):", value=1.0, min_value=0.1)
    base_width = st.number_input("Base Width (m):", value=3.0, min_value=0.1)
    top_width = st.number_input("Top Width (m):", value=1.0, min_value=0.0)
    bag_height = st.number_input("Bag Height (Cross-section) (m):", value=0.10, min_value=0.01)
    bag_width = st.number_input("Bag Width (Cross-section) (m):", value=0.25, min_value=0.01)

    if st.button("Draw Cross-Section"):
        fig = plot_wall_cross_section_with_bags(height, bag_height, base_width, top_width, bag_width)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
