from customtkinter import CTkFrame, CTkLabel, CTkButton, ThemeManager


class CTkSnackBar(CTkFrame):
    def __init__(self, master=None,
                 info: str = "",
                 width=200, height=30,
                 action=["$close"],
                 **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)

        self.__label_info = CTkLabel(self, text=info)
        self.__label_info.pack(fill="y", side="left", anchor="w", padx=8, pady=5, ipadx=3, ipady=3)

        self.__actions = []

        for text in reversed(action):
            __ = CTkButton(self, text=text, width=29, height=29, border_width=0, )
            if text == "$close":
                __.configure(text="✕", fg_color=self._fg_color, text_color=ThemeManager.theme["CTkLabel"]["text_color"], command=lambda: self.hind())
            if text == "$dismiss":
                __.configure(text="Dismiss",
                             fg_color=self._fg_color, command=lambda: self.hind())
            __._draw()
            __.pack(fill="y", side="right", padx=(0, 8), pady=5)
            self.__actions.append(__)

        try:
            if "CTkSnackBar" in ThemeManager.theme:
                if "fg_color" not in kwargs:
                    self._fg_color = ThemeManager.theme["CTkSnackBar"]["fg_color"]
                if "text_color" not in kwargs:
                    self.__label_info._text_color = ThemeManager.theme["CTkSnackBar"]["text_color"]
                    self.__label_info._draw()
        except:
            pass

    @property
    def info(self):
        return self.__label_info

    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, action):
        for widget in self.__actions:
            widget.destroy()

        for text in reversed(action):
            __ = CTkButton(self, text=text, width=29, height=32, border_width=0, )
            if text == "$close":
                __.configure(text="✕", fg_color=self._fg_color, text_color=ThemeManager.theme["CTkLabel"]["text_color"], command=lambda: self.hind())
            if text == "$dismiss":
                __.configure(text="Dismiss",
                             fg_color=self._fg_color, command=lambda: self.hind())
            __._draw()
            __.pack(fill="y", side="right", padx=(0, 8), pady=5)
            self.__actions.append(__)

    def hind(self):
        self.forget()

    def show(self, *args, **kwargs):
        self.pack(fill="x", side="bottom", padx=4, pady=4, ipadx=2, ipady=2, *args, **kwargs)


if __name__ == '__main__':
    from customtkinterx import CTkCustom, CTkMinimalTheme

    CTkMinimalTheme()

    root = CTkCustom()
    root.create_sizegrip()

    snackbar = CTkSnackBar(root.mainframe, info="This is a SnackBar")
    snackbar.actions = ["Hello World", "$close"]
    snackbar.show()

    root.mainloop()