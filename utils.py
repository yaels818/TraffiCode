import pygame

def scale_image(img, factor):
    """
    Scale an image by the given factor.
    Return the scaled image.

    Parameters
    ----------
    img : Surface
        Image to scale

    factor : double
        The factor to scale the image by.

    Notes
    -----
    1. If factor > 1 ==> image will get bigger (still within original scale).
    2. If factor < 1 ==> image will get smaller (still within original scale). 
    """
    
    # Calculate the new size for the image after the scale
    size = round(img.get_width() * factor), round(img.get_height() * factor)

    # Return the image in its new size
    return pygame.transform.scale(img, size)

def stretch_image(img, factor_width, factor_height):
    """
    Stretch an image by given factors.
    Return the stretched image.

    Parameters
    ----------
    img : Surface
        Image to stretch

    factor_width : double
        The factor by which to stretch the image horizontally.

    factor_height : double
        The factor by which to stretch the image vertically.

    Notes
    -----
    1. If factor > 1 ==> image will get bigger.
    2. If factor < 1 ==> image will get smaller. 
    """

    # Calculate the new size for the image after the stretch
    size = round(img.get_width() * factor_width), round(img.get_height() * factor_height)

    # Return the image in its new size
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    """
    Rotate an image in pygame without distortions.
    Return the new bounding rect for the image (after the rotation).

    Parameters
    ----------
    win : Surface
        Window to draw the image on

    img : Surface
        Image to rotate

    top_left : (x,y)
        Top-left corner of the image's rect

    angle : int
        The angle by which to rotate the image
    """

    # Create a copy of the original image after rotation by given angle
    rotated_image = pygame.transform.rotate(image, angle)

    # Get a new rectangle for the rotated image
    # (around the center of the image, without damaging x or y values)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = top_left).center)
    
    # Draw the rotated image with the new rectangle's top left corner as an anchor position
    win.blit(rotated_image, new_rect.topleft)

    # Return the new bounding rectangle for the image
    return new_rect

def blit_text_in_pos(win, font, color, text, pos):
    """
    Display text in given position on given window.

    Parameters
    ----------
    win : Surface
        Window to display the text on
    font : Font
        Font for the text
    color : (R,G,B)
        Color for the text
    text : String
        Text to display
    pos : (x,y)
        Position on the window to display the text at

    Notes
    -----
    1. If given position is too much to the left for us to center the text horizontally
    around it, text will only be centered vertically (y axis).
    """
    
    # Render the text in the given font and color
    # (1 is for anti-aliasing)
    render = font.render(text, 1, color)
    
    # Check if we can center around x axis
    if pos[0] > render.get_width()/2:
        # Center the text both horizontally and vertically around given position
        position = (pos[0] - render.get_width()/2, pos[1] - render.get_height()/2)
    else:
        # Center the text only vertically around given position
        position = (pos[0], pos[1] - render.get_height()/2)

    # Display text on the window 
    win.blit(render, position)