
def write(surface,font,color,string):
    """Utility function that draws multiple lines of text."""
    accumulator = 0
    
    while len(string):
        (line,_,string) = string.partition('\n')
        text = font.render(line, True, color)
        accumulator += font.get_height()
        surface.blit(text, (0,accumulator) )
    