import streamlit as st
import math
import matplotlib.pyplot as plt

def calculate_bags(height, length, shape, bag_length=0.35, bag_height=0.10):
    """
    Calculate total sandbags needed for a given wall height and shape.
    
    Parameters:
    -----------
    height : float
        Desired wall height (m).
    length : float
        Linear dimension (m), or radius for circle/semicircle, or arc length.
    shape : str
        "Straight", "Arc", "Circle", or "Semicircle".
    bag_length : float
        Approx. length of a sandbag (m).
    bag_height : float
        Approx. thickness (height) of a single sandbag layer (m).
    
    Returns:
    --------
    (total_bags, layers) : (int, int)
        total_bags = total number of sandbags (rounded up)
        layers = number of horizontal layers
    """
    # 1. Calculate the number of layers
    layers = math.ceil(height / bag_height)
    
    # 2. Effective wall length depends on shape
    if shape == "Straight":
        effective_length = length
    elif shape == "Arc":
        # either user inputs arc length directly,
        # or you computed from radius+angle
        effective_length = length
    elif shape == "Circle":
        # user-provided "length" is the radius
        effective_length = 2 * math.pi * length
    elif shape == "Semicircle":
        # user-provided "length" is the radius
        effective_length = math.pi * length
    else:
        effective_length = length
    
    # 3. Bags per layer
    bags_per_layer = math.ceil(effective_length / bag_length)
    
    # 4. Total bags
    total_bags = layers * bags_per_layer
    
    return total_bags, layers

def plot_wall_cross_section_with_bags(height, bag_height, w_base, w_top, bag_width):
    """
    Plots a cross-section of a trapezoidal sandbag wall from bottom (y=0) to top (y=height),
    showing each 'bag' as a rectangle in cross-section.

    Parameters:
    -----------
    height : float
        total wall height (m).
    bag_height : float
        thickness of each bag in cross-section (m).
    w_base : float
        width of the wall at the bottom (m).
    w_top : float
        width of the wall at the top (m).
    bag_width : float
        the horizontal width of each bag in cross-section (m).
    
    Returns:
    --------
    matplotlib figure
    """
    # Compute number of layers (1 bag tall each)
    n_layers = math.ceil(height / bag_height)
    # Actual thickness of each layer
    layer_thickness = height / n_layers

    fig, ax = plt.subplots(figsize=(6, 4))

    for i in range(n_layers):
        # The bottom and top y-coordinates of this layer
        y_bottom = i * layer_thickness
        y_top = (i + 1) * layer_thickness
        
        # fraction along the height
        frac_bottom = (y_bottom / height) if height != 0 else 0
        frac_top = (y_top / height) if height != 0 else 1
        
        # Interpolate widths for bottom & top of layer
        width_bottom = w_base + (w_top - w_base) * frac_bottom
        width_top    = w_base + (w_top - w_base) * frac_top
        
        # Approximate the layer's width as the average
        avg_layer_width = (width_bottom + width_top) / 2.0
        
        # Number of bags across this layer
        n_bags_layer = math.floor(avg_layer_width / bag_width)
        
        # Total horizontal space occupied by those bags
        total_bags_width = n_bags_layer * bag_width
        
        # Center them around x=0
        x_start = -(total_bags_width / 2.0) + (bag_width / 2.0)

        for b in range(n_bags_layer):
            x_center = x_start + b * bag_width
            # rectangle corners
            x_left = x_center - (bag_width / 2.0)
            x_right = x_center + (bag_width / 2.0)
            xs = [x_left, x_right, x_right, x_left, x_left]
            ys = [y_bottom, y_bottom, y_top, y_top, y_bottom]
            
            # Draw this bag
            ax.fill(xs, ys, color="skyblue", alpha=0.6, edgecolor="blue")

    ax.set_title(f"Cross-Section\nHeight={height}m, Base={w_base:.2f}m, Top={w_top:.2f}m")
    ax.set_xlabel("Horizontal distance (m)")
    ax.set_ylabel("Height (m)")

    half_max_width = max(w_base, w_top) / 2.0
    ax.set_xlim(-half_max_width * 1.2, half_max_width * 1.2)
    ax.set_ylim(0, height * 1.1)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.3)

    return fig

def main():
    st.title("Sandbag Wall Calculator")

    # ==========================
    # 1. USER INPUTS (Step 1)
    # ==========================
    st.header("1. Number of Sandbags Calculation")
    shape = st.selectbox(
        "Select the shape of your wall:",
        ["Straight", "Arc", "Circle", "Semicircle"]
    )
    height = st.number_input("Wall Height (m):", value=1.0, min_value=0.1)
    
    # For the shape dimension
    if shape == "Straight":
        length = st.number_input("Wall length (m):", value=10.0, min_value=0.1)
    elif shape == "Arc":
        st.write("Option: Input the arc length directly or specify radius & angle.")
        arc_choice = st.radio("Arc definition:", ["Arc length", "Radius + angle"])
        if arc_choice == "Arc length":
            length = st.number_input("Arc length (m):", value=15.0, min_value=0.1)
        else:
            radius = st.number_input("Arc radius (m):", value=5.0, min_value=0.1)
            angle_deg = st.number_input("Arc angle (degrees):", value=180.0, min_value=0.1, max_value=360.0)
            length = math.radians(angle_deg) * radius
    elif shape == "Circle":
        st.write("Enter the radius (m).")
        length = st.number_input("Radius (m):", value=5.0, min_value=0.1)
    else:  # Semicircle
        st.write("Enter the radius (m).")
        length = st.number_input("Radius (m):", value=5.0, min_value=0.1)

    bag_length = st.slider("Sandbag length (m) [along the wall]:", 0.2, 0.6, 0.35, 0.01)
    bag_height = st.slider("Sandbag height (m) [layer thickness]:", 0.05, 0.2, 0.10, 0.01)

    st.write("---")

    # ==========================
    # 2. AUTOMATED CALC + CROSS-SECTION
    # ==========================
    if st.button("Calculate & Visualize"):
        # --- Calculate total bags ---
        total_bags, layers = calculate_bags(height, length, shape, bag_length, bag_height)

        st.subheader("Calculation Results")
        st.write(f"**Total Bags Needed:** {total_bags}")
        st.write(f"**Number of Layers:** {layers}")
        st.markdown("""
       
        """)

        # --- Auto-Populate Cross-Section Values ---
        # We'll pick a recommended base width (e.g. 3 * height) and top width (e.g. 1 * height)
        # You can tweak or let users override if you want.
        recommended_base = 3 * height
        recommended_top = 1 * height

        st.write("---")
        st.header("Auto-Populated Cross-Section")
        st.write("Below is a simple trapezoidal cross-section, using recommended base/top widths.")
        
        st.write(f"**Recommended Base Width** = 3 × Height = {recommended_base:.2f} m")
        st.write(f"**Recommended Top Width** = 1 × Height = {recommended_top:.2f} m")

        st.write("**(You can adjust these values or the bag cross-section width if desired)**")
        
        # We'll show "editable" number inputs, starting with recommended defaults
        base_width = st.number_input("Base Width (m):", value=float(recommended_base), min_value=0.0, step=0.1)
        top_width = st.number_input("Top Width (m):", value=float(recommended_top), min_value=0.0, step=0.1)
        
        # Bag cross-section width (different from bag_length "along the wall")
        bag_cross_width = st.number_input("Bag Width in Cross-Section (m):", value=0.25, min_value=0.01, step=0.01)

        # Show figure
        fig = plot_wall_cross_section_with_bags(
            height=height,
            bag_height=bag_height,
            w_base=base_width,
            w_top=top_width,
            bag_width=bag_cross_width
        )
        st.pyplot(fig)

if __name__ == "__main__":
    main()
