import flet as ft

from ..models import user_model


def home_page(page: ft.Page):
    page.title = "Muncher"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user = user_model.User(first_name="Mohamed", last_name="Mohamed")

    txt_name = user.first_name
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text(value=txt_name),
                ft.Row(
                    controls=[
                        ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                        txt_number,
                        ft.IconButton(ft.icons.ADD, on_click=plus_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )
