from manimlib import *
from utils.constants import *


# Define a function to create the text and underline mobject
def create_text_with_underline(
    text_str: str,
    font_name: str,
    color_gradient: tuple,
    font_size: float = 1.5,  # Adjusted to a typical ManimGL scale, 100 might be too large directly
    underline_thickness: float = 2,  # User's specified thickness
) -> VGroup:
    """
    Creates a Text mobject with a gradient and a gradient-colored underline.

    Args:
        text_str (str): The text content.
        font_name (str): The name of the font to use.
        color_gradient (tuple): A tuple of colors for the gradient (e.g., (COLOR1, COLOR2, COLOR3)).
        font_size (float): The size of the text (ManimGL scale). Default is 1.5.
        underline_thickness (float): The thickness of the underline. Default is 0.1.

    Returns:
        VGroup: A VGroup containing the text mobject and its underline, grouped together.
    """
    # Create the text Mobject
    # Note: ManimGL's font_size is typically scaled relative to its internal default (often 1.0)
    # Using 100 directly might create an extremely large text. 1.5 is usually a good large size.
    text_mobject = Text(
        text_str,
        font=font_name,
        font_size=font_size,
        color=WHITE,  # Initial color, will be overridden by gradient
        weight="BOLD",
    )
    text_mobject.set_color_by_gradient(
        *color_gradient
    )  # Unpack the tuple for the gradient

    # Create the underline
    underline = Line(LEFT, RIGHT)
    underline.set_width(
        text_mobject.get_width() * 1.1  # Make it slightly wider than the text
    )
    underline.set_stroke(width=underline_thickness)  # Set the thickness
    underline.next_to(text_mobject, DOWN, buff=0.1)  # Position below the text
    underline.set_color_by_gradient(*color_gradient)  # Apply gradient

    # Group them together so they move as one unit
    text_with_underline_group = VGroup(text_mobject, underline)
    return text_with_underline_group
