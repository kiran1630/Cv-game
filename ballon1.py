import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import warnings

class run_ballon_game:
    def __init__(self):
        # Suppress TensorFlow warnings if they are causing issues
        warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

        # Initialize Pygame
        pygame.init()

        # Create Window/Display
        self.width, self.height = 1280, 720
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Balloon Pop")

        # Initialize Clock for FPS
        self.fps = 30
        self.clock = pygame.time.Clock()

        # Webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)  # width
        self.cap.set(4, 720)  # height

        # Check if webcam is opened
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            pygame.quit()
            exit()

        # Load Images
        try:
            self.imgBalloon = pygame.image.load(r"onlygreen.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading image: {e}")
            self.cap.release()  # Ensure the camera is released if image loading fails
            pygame.quit()
            exit()

        self.rectBalloon = pygame.Rect(500, 300, self.imgBalloon.get_width(), self.imgBalloon.get_height())

        # Variables
        self.initial_speed = 10
        self.max_speed = 30
        self.speed_increase_interval = 3  # seconds
        self.speed = self.initial_speed
        self.score = 0
        self.startTime = time.time()
        self.totalTime = 25
        self.pop_display_time = 0.4  # time in seconds to display '10+' where the balloon was popped
        self.last_pop_time = 0
        self.pop_position = None

        # Hand Detector
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)

        self.run_game()

    def resetBalloon(self):
        self.rectBalloon.x = random.randint(100, self.width - 100)
        self.rectBalloon.y = self.height + 50

    def get_current_speed(self, elapsed_time):
        """Return speed based on elapsed time."""
        new_speed = self.initial_speed + (elapsed_time // self.speed_increase_interval) * 2
        return min(new_speed, self.max_speed)

    def run_game(self):
        # Main loop
        start = True
        try:
            while start:
                # Get Events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        start = False

                # Apply Logic
                elapsed_time = time.time() - self.startTime
                timeRemain = int(self.totalTime - elapsed_time)

                if timeRemain < 0:
                    self.window.fill((255, 255, 255))

                    font = pygame.font.Font(None, 50)
                    textScore = font.render(f'Your Score: {self.score}', True, (50, 50, 255))
                    textTime = font.render(f'Time UP', True, (50, 50, 255))
                    self.window.blit(textScore, (450, 350))
                    self.window.blit(textTime, (530, 275))

                else:
                    # OpenCV
                    success, img = self.cap.read()
                    if not success:
                        print("Failed to capture image")
                        continue
                    
                    img = cv2.flip(img, 1)
                    hands, img = self.detector.findHands(img, flipType=False)

                    self.speed = self.get_current_speed(elapsed_time)
                    self.rectBalloon.y -= self.speed  # Move the green balloon up

                    if self.rectBalloon.y < 0:
                        self.resetBalloon()
                        self.speed = self.get_current_speed(elapsed_time)

                    if hands:
                        hand = hands[0]
                        x, y = hand['lmList'][8][0:2]
                        if self.rectBalloon.collidepoint(x, y):
                            # Green Balloon is popped
                            self.resetBalloon()
                            self.score += 10
                            self.speed = self.get_current_speed(elapsed_time)
                            self.last_pop_time = time.time()
                            self.pop_position = (x, y)

                    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    imgRGB = np.rot90(imgRGB)
                    frame = pygame.surfarray.make_surface(imgRGB).convert()
                    frame = pygame.transform.flip(frame, True, False)
                    self.window.blit(frame, (0, 0))
                    self.window.blit(self.imgBalloon, self.rectBalloon)

                    font = pygame.font.Font(None, 50)
                    textScore = font.render(f'Score: {self.score}', True, (50, 50, 255))
                    textTime = font.render(f'Time: {timeRemain}', True, (50, 50, 255))
                    self.window.blit(textScore, (35, 35))
                    self.window.blit(textTime, (1000, 35))

                    # Display '10+' at pop position
                    if self.pop_position and time.time() - self.last_pop_time < self.pop_display_time:
                        textPop = font.render(f'+10', True, (255, 0, 0))
                        self.window.blit(textPop, self.pop_position)

                # Update Display
                pygame.display.update()
                # Set FPS
                self.clock.tick(self.fps)

        finally:
            # Release resources
            print("Releasing camera...")
            self.cap.release()
            print("Camera released.")
            pygame.quit()

