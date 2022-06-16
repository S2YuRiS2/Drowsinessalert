import time
import pygame

def sound_alarm():
    pygame.mixer.init()
    alarm = pygame.mixer.Sound('Sound/alarm_sound.wav')
    alarm.play()
    time.sleep(0.1)
    alarm.play()
    time.sleep(0.1)
    alarm.play()
    time.sleep(0.1)
    alarm.play()

