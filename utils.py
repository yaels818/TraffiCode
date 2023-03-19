import pygame

def scale_image(img, factor):
    """
    Scale an image by given factor.
    If factor > 1 ==> image will get bigger.
    If factor < 1 ==> image will get smaller. 
    Return the scaled image.
    """
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def stretch_image(img, factor_width, factor_height):
    """
    Stretch an image by given factors.
    If factor > 1 ==> image will get bigger.
    If factor < 1 ==> image will get smaller. 
    Return the stretched image.
    """
    size = round(img.get_width() * factor_width), round(img.get_height() * factor_height)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    """ 
    Rotate an image in pygame without distortions.
    Return the new bounding rect for the image after the rotation.
    """
    rotated_image = pygame.transform.rotate(image, angle)
    # Rotate around the center of the image, without damaging x or y values
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    return new_rect


def blit_text_center(win, font, text):
    """
    Display text on in the center of the screen
    """
    # 1 is for anti-aliasing (always put 1), last parameter is RGB for text color
    render = font.render(text, 1, (200, 200, 200))

    # Show render at the center of the window (get x,y for top-left position of the render)
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2 - 30))