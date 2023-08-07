from customtkinter import CTkScrollableFrame, CTkFrame, CTkLabel, CTkScrollbar, ThemeManager


class CTkKanbanCard(CTkFrame):
    def __init__(self, master=None,
                 title: str = "",
                 corner_radius: int = None,
                 width=200, height=360,
                 add_task: str = "Add task",
                 add_task_button: bool = True,
                 **kwargs):
        super().__init__(master, width=width, height=height, corner_radius=corner_radius, **kwargs)

        try:
            if "CTkKanban" in ThemeManager.theme:
                if "corner_radius" not in kwargs:
                    self._corner_radius = ThemeManager.theme["CTkKanban"]["card_corner_radius"]
                if "fg_color" not in kwargs:
                    self._fg_color = ThemeManager.theme["CTkKanban"]["card_color"]
                if "border_width" not in kwargs:
                    self._border_width = ThemeManager.theme["CTkKanban"]["card_border_width"]
                if "border_color" not in kwargs:
                    self._border_color = ThemeManager.theme["CTkKanban"]["card_border_color"]
        except:
            pass

        self.__label_title = CTkLabel(self, text=title)
        self.__label_title.pack(fill="x", side="top", padx=4, pady=4)

        self.__button_add = CTkButton(self, text=add_task, border_width=0, command=lambda: self.add_task())
        if add_task_button:
            self.__button_add.pack(fill="x", side="bottom", padx=4, pady=(0, 4))

        self._draw()
        self.__label_title._draw()

    @property
    def title(self):
        return self.__label_title

    @property
    def addbutton(self):
        return self.__button_add

    def add_task(self, width=192, height=80, *args, **kwargs):
        __ = CTkFrame(self, width=width, height=height, *args, **kwargs)
        try:
            if "CTkKanban" in ThemeManager.theme:
                if "corner_radius" not in kwargs:
                    __._corner_radius = ThemeManager.theme["CTkKanban"]["task_corner_radius"]
                if "fg_color" not in kwargs:
                    __._fg_color = ThemeManager.theme["CTkKanban"]["task_color"]
                if "border_width" not in kwargs:
                    __._border_width = ThemeManager.theme["CTkKanban"]["task_border_width"]
                if "border_color" not in kwargs:
                    __._border_color = ThemeManager.theme["CTkKanban"]["task_border_color"]
        except:
            pass
        __.pack(fill="x", side="top", ipadx=5, ipady=5, padx=4, pady=4)
        __._draw()
        return __


class CTkKanban(CTkScrollableFrame):
    def __init__(self, master=None, width=640, height=380, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)

        try:
            if "CTkKanban" in ThemeManager.theme:
                if "corner_radius" not in kwargs:
                    self._corner_radius = ThemeManager.theme["CTkKanban"]["corner_radius"]
                if "fg_color" not in kwargs:
                    self._fg_color = ThemeManager.theme["CTkKanban"]["color"]
                if "border_width" not in kwargs:
                    self._border_width = ThemeManager.theme["CTkKanban"]["border_width"]
        except:
            pass

    def create_taskcard(self, title: str = "", *args, **kwargs):
        __ = CTkKanbanCard(self, title=title, *args, **kwargs)
        __.pack(side="left", anchor="nw", ipadx=5, ipady=5, padx=3, pady=3)
        return __


if __name__ == '__main__':
    from customtkinterx import CTkCustom, CTkMinimalTheme
    from customtkinter import CTkButton, CTkLabel, CTkFont, set_appearance_mode

    set_appearance_mode("light")
    CTkMinimalTheme()

    root = CTkCustom()
    root.create_sizegrip()

    kanban = CTkKanban(root.mainframe)
    kanban_card1 = kanban.create_taskcard(title="Card1")
    kanban_card1_task1 = kanban_card1.add_task()
    kanban_card1_task1_label1 = CTkLabel(kanban_card1_task1, text="Hello!", font=CTkFont(size=15))
    kanban_card1_task1_label1.pack(fill="x", padx=5, pady=5)
    kanban_card1_task1_button1 = CTkButton(kanban_card1_task1, text="Okay")
    kanban_card1_task1_button1.pack(fill="x", padx=5, pady=5, ipady=10)
    kanban_card2 = kanban.create_taskcard(title="Card2")
    kanban_card2_task1 = kanban_card2.add_task()
    kanban_card2_task2 = kanban_card2.add_task()
    kanban.pack(fill="both", expand="yes", padx=5, pady=5)

    root.mainloop()