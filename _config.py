def place_center(self,win_width,win_height):
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    x_cord = (screen_width/2)-(win_width/2)
    y_cord = (screen_height/2)-(win_height/2)

    return x_cord, y_cord