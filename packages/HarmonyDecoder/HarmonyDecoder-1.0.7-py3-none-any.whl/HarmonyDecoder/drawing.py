from __future__ import annotations

from PIL import Image, ImageDraw
from HarmonyDecoder.note import note
from HarmonyDecoder.function import function
from HarmonyDecoder.note import note
from HarmonyDecoder.scale import scale
import os


class drawing:
    def __init__(self, tonation:scale = scale('C', 'major')) -> None:
        if tonation is None:
            raise TypeError("tonation cannot be none")

        self.__staff_line_spacing:int = 20
        self.__staff_spacing:int = 300
        self.__staff_line_width:int = 5
        self.__tonation:scale = tonation

        self.__flat:Image.Image = Image.open(f"{os.path.dirname(os.path.realpath(__file__))}/Images/Flat.png")
        self.__sharp:Image.Image = Image.open(f"{os.path.dirname(os.path.realpath(__file__))}/Images/Sharp.png")
        self.__resize_signs()

        self.__note_line_heigth:int = self.__staff_line_spacing * 5
        self.__function_spacing:int = 5 * self.__staff_line_spacing

        self.__size_x:int = 3508
        self.__size_y:int = 600
        self.__margin_x:int = 20
        self.__margin_y:int = 100

        self.__background_color = 'white'
        self.__staff_color = 'black'
        self.__color_profile = 'RGBA'

        self.__image:Image.Image = Image.new(self.__color_profile, (self.__size_x, self.__size_y), self.__background_color)
        self.__drawing:ImageDraw.ImageDraw = ImageDraw.Draw(self.__image)

# public:
    def draw_staff(self) -> None:
        self.__draw_one_staff(0, 'Treble')
        self.__draw_one_staff(self.__staff_spacing, 'Bass')
        self.draw_measure_line(0, 0)

    def show(self) -> None:
        self.__image.show()

    def clear(self) -> None:
        self.__image = Image.new(self.__color_profile, (self.__size_x, self.__size_y), self.__background_color)
        self.__drawing = ImageDraw.Draw(self.__image)

    def draw_measure_line(self, pos_x:int, pos_y:int) -> None:
        start_x:int = self.__margin_x + pos_x
        end_x:int = start_x

        start_y:int = self.__margin_y + pos_y
        end_y:int = self.__margin_y + pos_y + (4 * self.__staff_line_spacing) + self.__staff_spacing

        self.__draw_line((start_x, start_y), (end_x, end_y), self.__staff_line_width, self.__staff_color)

    def insert_image(self, pos_x:int, pos_y:int, source:str, scale:float=1.0) -> None:
        if pos_x < 0 or pos_x > self.__size_x or pos_y < 0 or pos_y > self.__size_y:
            raise ValueError("Cannot insert image oudside the canvas.")
        
        try:
            to_insert:Image.Image = Image.open(source)
        except FileNotFoundError:
            print(f"File {source} not found.")
            return
        
        size:tuple[int, int] = (to_insert.size[0], to_insert.size[1])
        max_y:int = 10 * self.__staff_line_spacing
        resize_value:int = (size[1] / max_y) / scale

        to_insert = to_insert.resize(
            (int(size[0] / resize_value),
            int(size[1] / resize_value))
        )
        
        self.__image.paste(to_insert, (pos_x, pos_y - int(to_insert.size[1] / 2)))

    def draw_note(self, what:note, direction:str="up", cleff:str="Treble", staff_position:int=0, x:int=0) -> None:
        if direction not in ['up', 'down']:
            raise ValueError("Direction must be one of [up, down].")
        
        if cleff not in ['Treble', 'Bass']:
            raise ValueError("Key must be one of [up, down]")
        
        if what is None:
            raise TypeError("Note cannot be none.")
        
        if cleff == 'Treble':
            C5_position:int = int(4.5 * self.__staff_line_spacing)
        else:
            C5_position:int = int(-1.5 * self.__staff_line_spacing)            

        difference_dict:dict[str, int] = {
            "C" : 0,
            "D" : 1,
            "E" : 2,
            "F" : 3,
            "G" : 4,
            "A" : 5,
            "B" : 6
        }

        difference:int = difference_dict[what.name[0]]
        difference += 7 * (what.octave - 5)

        note_position:int = C5_position - difference * int(self.__staff_line_spacing / 2)

        note_start_x:int = self.__margin_x + 4 * self.__function_spacing + x * self.__function_spacing
        note_start_y:int = self.__margin_y + (staff_position * self.__staff_spacing) + note_position
        note_end_x:int = note_start_x + (2 * self.__staff_line_spacing)
        note_end_y:int = note_start_y + self.__staff_line_spacing

        self.__drawing.ellipse(
            [(note_start_x, note_start_y), (note_end_x, note_end_y)],
            width=1,
            fill=self.__staff_color
        )

        line_y:int = note_start_y + int(0.5 * self.__staff_line_spacing)

        if direction == 'up':
            line_x:int = note_start_x + (2 * self.__staff_line_spacing)
            self.__draw_line((line_x, line_y), (line_x, line_y - self.__note_line_heigth), self.__staff_line_width, self.__staff_color)
        else:
            line_x:int = note_start_x
            self.__draw_line((line_x, line_y), (line_x, line_y + self.__note_line_heigth), self.__staff_line_width, self.__staff_color)

        add_line_start_x:int = note_start_x - int(self.__staff_line_width / 2)
        add_line_end_x:int = note_start_x + int(2.5 * self.__staff_line_spacing)
        
        add_line_limit_y:int = int((note_start_y + note_end_y) / 2)

        if cleff == "Bass":
            if what >= note("C", 5):
                add_line_start_y:int = self.__margin_y + self.__staff_spacing * staff_position - self.__staff_line_spacing

                while add_line_start_y >= add_line_limit_y:
                    self.__draw_line(
                        (add_line_start_x, add_line_start_y),
                        (add_line_end_x, add_line_start_y),
                        self.__staff_line_width,
                        self.__staff_color
                    )
                    
                    add_line_start_y -= self.__staff_line_spacing
            elif what <= note("E", 3):
                add_line_start_y:int = self.__margin_y + self.__staff_spacing * staff_position + 5 * self.__staff_line_spacing

                while add_line_start_y <= add_line_limit_y:
                    self.__draw_line(
                        (add_line_start_x, add_line_start_y),
                        (add_line_end_x, add_line_start_y),
                        self.__staff_line_width,
                        self.__staff_color
                    )
                    
                    add_line_start_y += self.__staff_line_spacing
        else:
            if what >= note("A", 6):
                add_line_start_y:int = self.__margin_y + self.__staff_spacing * staff_position - self.__staff_line_spacing
                
                while add_line_start_y >= add_line_limit_y:
                    self.__draw_line(
                        (add_line_start_x, add_line_start_y),
                        (add_line_end_x, add_line_start_y),
                        self.__staff_line_width,
                        self.__staff_color
                    )
                    
                    add_line_start_y -= self.__staff_line_spacing
            elif what <= note("C", 5):
                add_line_start_y:int = self.__margin_y + self.__staff_spacing * staff_position + 5 * self.__staff_line_spacing

                while add_line_start_y <= add_line_limit_y:
                    self.__draw_line(
                        (add_line_start_x, add_line_start_y),
                        (add_line_end_x, add_line_start_y),
                        self.__staff_line_width,
                        self.__staff_color
                    )
                    
                    add_line_start_y += self.__staff_line_spacing                
        
        sign_x:int = note_start_x - int(self.__staff_line_spacing * 1.5)        

        if '#' in what.name: #and what.name not in self.__tonation.notes:
            sign_y:int = note_start_y - int(self.__staff_line_spacing * 0.5)
            to_insert:Image.Image = self.__sharp
            self.__image.paste(to_insert, (sign_x, sign_y))
        elif 'b' in what.name: #and what.name not in self.__tonation.notes:
            sign_y:int = note_start_y - int(self.__staff_line_spacing * 0.8)
            to_insert:Image.Image = self.__flat
            self.__image.paste(to_insert, (sign_x, sign_y))        

    def draw_function(self, what:function, staff_position:int=0, x:int=0) -> None:
        self.draw_note(what.soprano, "up", "Treble", staff_position, x)
        self.draw_note(what.alto, "down", "Treble", staff_position, x)
        self.draw_note(what.tenore, "up", "Bass", staff_position + 1, x)
        self.draw_note(what.bass, "down", "Bass", staff_position + 1, x)

    def save(self, name:str) -> None:
        self.__image.save(name)

# private:
    def __draw_line(self, start:tuple[int, int], end:tuple[int, int], width:int, color:str) -> None:
        for coordinate in [start[0], end[0]]:
            if coordinate < 0 or coordinate > self.__size_x:
                raise ValueError("Cannot draw line outside of the canvas.")
            
        for coordinate in [start[1], end[1]]:
            if coordinate < 0 or coordinate > self.__size_y:
                raise ValueError("Cannot draw line outside of the canvas.")

        self.__drawing.line(
            [start, end],
            width=width,
            fill=color
        )

    def __draw_one_staff(self, pos_y:int, cleff:str) -> None:
        if pos_y < 0 or (pos_y + 6 * self.__staff_line_spacing) > self.__size_y:
            raise ValueError("Cannot draw staff outside of the canvas.")
        
        scale:int = 0.5 if cleff == 'Bass' else 1

        self.insert_image(
            self.__margin_x + self.__function_spacing,
            self.__margin_y + 2 * self.__staff_line_spacing + pos_y,
            f'{os.path.dirname(os.path.realpath(__file__))}/Images/{cleff}Cleff.png',
            scale=scale
        )

        for index in range(5):
            start_x:int = self.__margin_x
            end_x:int = self.__size_x - self.__margin_x

            start_y:int = self.__margin_y + pos_y + index * self.__staff_line_spacing
            end_y:int = start_y

            self.__draw_line((start_x, start_y), (end_x, end_y), width=self.__staff_line_width, color=self.__staff_color)

    def __resize_signs(self) -> None:
        resize_scalar:int = int((self.__sharp.size[1] / self.__staff_line_spacing) / 2)

        self.__sharp = self.__sharp.resize(
            (int(self.__sharp.size[0] / resize_scalar),
            int(self.__sharp.size[1] / resize_scalar))
        )

        resize_scalar = int((self.__flat.size[1] / self.__staff_line_spacing) / 2)

        self.__flat = self.__flat.resize(
            (int(self.__flat.size[0] / resize_scalar),
            int(self.__flat.size[1] / resize_scalar))
        )

    def __get_image(self) -> Image.Image:
        return self.__image

# properties:
    image:Image.Image = property(__get_image)