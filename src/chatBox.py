import pygame as pg

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
CHAT_LIMIT = 15


class ChatBox:

    def __init__(self, x, y, w, h, text='', chats=None):
        if chats is None:
            chats = []
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.chats = chats
        self.chat_txt_surface = []
        for chat in self.chats[max(0, len(self.chats) - CHAT_LIMIT):]:
            self.chat_txt_surface.append(FONT.render(chat, True, self.color))
        self.active = False

    def handle_event(self, event, player_symbol):
        updated_chatbox = False
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if self.text != '':
                        self.chats.append(player_symbol + ': ' + self.text)
                        self.text = ''
                        updated_chatbox = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                # Limit the chat box
                self.chat_txt_surface = []
                for chat in self.chats[max(0, len(self.chats) - CHAT_LIMIT):]:
                    self.chat_txt_surface.append(FONT.render(chat, True, self.color))
        return updated_chatbox

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the chat.
        self.chat_txt_surface = []
        for chat in self.chats[max(0, len(self.chats) - CHAT_LIMIT):]:
            self.chat_txt_surface.append(FONT.render(chat, True, self.color))
        for line in range(len(self.chat_txt_surface)):
            screen.blit(self.chat_txt_surface[line], (self.rect.x, self.rect.y - 560 + (line * 32) + (5 * line)))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
