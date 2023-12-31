import pygame
from pygame import mixer

from components.button import Button
from components.config import CONFIG, CONST, Fonts, debug
from components.events import process
from components.font import Font
from screens.ingame import Ingame
from screens.settings import update_settings

from components.sfx_collection import SFX

reload = False
music_playing = True

def update_menu():
    def process_menu(event: pygame.event.Event):
        """인게임 이벤트 처리용 (process() child 함수)"""
        global reload, music_playing
        nonlocal need_to_exit

        ctrl = pygame.key.get_mods() & pygame.K_LCTRL  # ctrl 키 누르는 여부

        match event.type:
            case pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 시
                if button_play.check_for_input(mouse_pos):  # 시작
                    music_playing = False
                    mixer.music.stop()

                    Ingame.default = Ingame()
                    Ingame.default.update_ingame()
                    return

                if button_settings.check_for_input(mouse_pos):
                    update_settings()
                    return

                if button_exit.check_for_input(mouse_pos):  # 종료
                    CONFIG.is_running = False
                    return

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        CONFIG.is_running = False

                    case pygame.K_r:  # Reload
                        if ctrl:
                            reload = True
                            need_to_exit = True

    def play_music():
        mixer.music.load("assets/audio/bg_daily.ogg")
        mixer.music.set_volume(SFX.volume)
        mixer.music.play(-1)

    global music_playing
    
    need_to_exit = False

    background = pygame.image.load("assets/images/background_menu.png")
    background = pygame.transform.scale(background, CONST.SCREEN_SIZE)

    play_music()

    while CONFIG.is_running and not need_to_exit:
        CONFIG.clock.tick(CONFIG.FPS)
        
        if not music_playing:
            music_playing = True
            play_music()

        CONFIG.surface.blit(background, (0, 0))

        mouse_pos = CONFIG.get_mouse_pos()
        title = pygame.image.load("assets/images/menu_title.png")
        title = pygame.transform.scale_by(title, 0.6)

        button_play_image = pygame.image.load("assets/images/menu_play_rect.png")
        button_play_image = pygame.transform.scale(button_play_image, (300, 80))
        button_play = Button(
            image=button_play_image,
            pos=(478, 380),
            text_input="시작",
            font=Font(Fonts.TITLE2, 60).to_pygame(),
            base_color="#ffffff",
            hovering_color="White",
        )

        button_settings_image = pygame.image.load(
            "assets/images/button_settings.png"
        )
        button_settings_image = pygame.transform.scale_by(button_settings_image, 0.4)
        button_settings = Button(image=button_settings_image, pos=(588, 480))

        button_exit_image = pygame.image.load("assets/images/menu_play_rect.png")
        button_exit_image = pygame.transform.scale(button_exit_image, (200, 80))
        button_exit = Button(
            image=button_exit_image,
            pos=(428, 480),
            text_input="종료",
            font=Font(Fonts.TITLE2, 50).to_pygame(),
            base_color="#ffffff",
            hovering_color="White",
        )

        for button in [button_play, button_settings, button_exit]:
            button.change_color(mouse_pos)
            button.update(CONFIG.surface)

        CONFIG.surface.blit(title, title.get_rect(center=(480, 140)))
        CONFIG.update_screen()

        process(process_menu)
