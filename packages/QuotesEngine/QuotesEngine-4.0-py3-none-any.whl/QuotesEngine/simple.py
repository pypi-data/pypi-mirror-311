import random
import sys
import time

class Motivate:
    class username:
        def __init__(self, name: str) -> None:
            print()
            self.name = name
            print(f"Hello {self.name} !, this is my first project.")
            self.motivate(name)
        
        def motivate(self,name) -> str:
            print(f"choosing the best quote for you, {name}....", end="\r", flush=True)
            time.sleep(4)
            sys.stdout.write("\033[K\r")
            sys.stdout.flush()

            predictions = {
                1: f"Every day is a new beginning, {self.name}. Take a deep breath, smile, and start again.",
                2: f"Remember, {self.name}, the only limit to our realization of tomorrow is our doubts of today.",
                3: f"Don’t watch the clock, {self.name}; do what it does. Keep going.",
                4: f"Believe you can, {self.name}, and you're halfway there.",
                5: f"The future belongs to those who believe in the beauty of their dreams, {self.name}. Keep dreaming big.",
                6: f"Success is not final, failure is not fatal: It is the courage to continue that counts, {self.name}.",
                7: f"The best way to predict the future is to create it, {self.name}. Start today!",
                8: f"You’re never too old to set another goal or to dream a new dream, {self.name}. It's never too late.",
                9: f"Your limitation—it's only your imagination, {self.name}. Break free from it.",
                10: f"Push yourself, {self.name}, because no one else is going to do it for you.",
                11: f"Great things never come from comfort zones, {self.name}. Step out and embrace the challenge.",
                12: f"Dream it. Wish it. Do it, {self.name}. Make it happen.",
                13: f"Success doesn’t just find you, {self.name}. You have to go out and get it.",
                14: f"The harder you work for something, the greater you’ll feel when you achieve it, {self.name}.",
                15: f"Dream bigger. Do bigger, {self.name}. Your potential is limitless.",
                16: f"Wake up with determination, {self.name}. Go to bed with satisfaction.",
                17: f"Do something today that your future self will thank you for, {self.name}.",
                18: f"Little things make big days, {self.name}. Cherish every moment.",
                19: f"It’s going to be hard, {self.name}, but hard does not mean impossible. Keep striving.",
                20: f"Don’t stop when you’re tired, {self.name}. Stop when you’re done.",
                21: f"Wake up with a purpose, {self.name}. Live your life with passion.",
                22: f"You are capable of amazing things, {self.name}. Believe in yourself.",
                23: f"Your only limit is you, {self.name}. Be brave and fearless.",
                24: f"Sometimes you will never know the value of a moment until it becomes a memory, {self.name}.",
                25: f"Life is tough, {self.name}, but so are you. Keep fighting.",
                26: f"The best time for new beginnings is now, {self.name}. Start today.",
                27: f"You don’t have to be great to start, {self.name}, but you have to start to be great.",
                28: f"Every accomplishment starts with the decision to try, {self.name}.",
                29: f"Life is not about finding yourself, {self.name}. It’s about creating yourself.",
                30: f"You are stronger than you think, {self.name}. Keep pushing through.",
                31: f"Believe in the magic of new beginnings, {self.name}. They can change everything.",
                32: f"Your vibe attracts your tribe, {self.name}. Stay positive.",
                33: f"Be a voice, not an echo, {self.name}. Stand out.",
                34: f"Do what you can, with what you have, where you are, {self.name}.",
                35: f"Life is a journey, and if you fall in love with the journey, you will be in love forever, {self.name}. Embrace every step.",
                36: f"Success usually comes to those who are too busy to be looking for it, {self.name}. Keep working hard.",
                37: f"Opportunities don’t happen, you create them, {self.name}. Make your own path.",
                38: f"Don’t be pushed around by the fears in your mind, {self.name}. Be led by the dreams in your heart.",
                39: f"Everything you’ve ever wanted is on the other side of fear, {self.name}. Face it bravely.",
                40: f"Success is walking from failure to failure with no loss of enthusiasm, {self.name}. Keep your spirit high.",
                41: f"Your life does not get better by chance, it gets better by change, {self.name}. Take the leap.",
                42: f"Act as if what you do makes a difference, {self.name}. It does.",
                43: f"Success is not how high you have climbed, but how you make a positive difference to the world, {self.name}.",
                44: f"Keep your face always toward the sunshine—and shadows will fall behind you, {self.name}.",
                45: f"Believe in yourself, {self.name}. You are capable of achieving great things.",
                46: f"Your passion is waiting for your courage to catch up, {self.name}. Go for it.",
                47: f"Don’t count the days, make the days count, {self.name}. Live fully.",
                48: f"Success is not the key to happiness. Happiness is the key to success, {self.name}. Enjoy the journey.",
                49: f"Life is 10% what happens to us and 90% how we react to it, {self.name}. Choose positivity.",
                50: f"Challenges are what make life interesting, and overcoming them is what makes life meaningful, {self.name}.",
                51: f"Your limitation—it's only your imagination, {self.name}. Dream big.",
                52: f"Sometimes we’re tested not to show our weaknesses, but to discover our strengths, {self.name}.",
                53: f"The harder you work for something, the greater you’ll feel when you achieve it, {self.name}.",
                54: f"Dream bigger, {self.name}. Your potential is limitless.",
                55: f"Wake up with determination, {self.name}. Go to bed with satisfaction.",
                56: f"Do something today that your future self will thank you for, {self.name}.",
                57: f"Little things make big days, {self.name}. Cherish every moment.",
                58: f"It’s going to be hard, {self.name}, but hard does not mean impossible. Keep striving.",
                59: f"Don’t stop when you’re tired, {self.name}. Stop when you’re done.",
                60: f"Wake up with a purpose, {self.name}. Live your life with passion.",
                61: f"You are capable of amazing things, {self.name}. Believe in yourself.",
                62: f"Your only limit is you, {self.name}. Be brave and fearless.",
                63: f"Sometimes you will never know the value of a moment until it becomes a memory, {self.name}.",
                64: f"Life is tough, {self.name}, but so are you. Keep fighting.",
                65: f"The best time for new beginnings is now, {self.name}. Start today.",
                66: f"You don’t have to be great to start, {self.name}, but you have to start to be great.",
                67: f"Every accomplishment starts with the decision to try, {self.name}.",
                68: f"Life is not about finding yourself, {self.name}. It’s about creating yourself.",
                69: f"You are stronger than you think, {self.name}. Keep pushing through.",
                70: f"Believe in the magic of new beginnings, {self.name}. They can change everything.",
                71: f"Your vibe attracts your tribe, {self.name}. Stay positive.",
                72: f"Be a voice, not an echo, {self.name}. Stand out.",
                73: f"Do what you can, with what you have, where you are, {self.name}.",
                74: f"Life is a journey, and if you fall in love with the journey, you will be in love forever, {self.name}. Embrace every step.",
                75: f"Success usually comes to those who are too busy to be looking for it, {self.name}. Keep working hard.",
                76: f"Opportunities don’t happen, you create them, {self.name}. Make your own path.",
                77: f"Don’t be pushed around by the fears in your mind, {self.name}. Be led by the dreams in your heart.",
                78: f"Everything you’ve ever wanted is on the other side of fear, {self.name}. Face it bravely.",
                79: f"Success is walking from failure to80",
                81: f"Your life does not get better by chance, it gets better by change, {self.name}. Take the leap.",
                82: f"Act as if what you do makes a difference, {self.name}. It does.",
                83: f"Success is not how high you have climbed, but how you make a positive difference to the world, {self.name}.",
                84: f"Keep your face always toward the sunshine—and shadows will fall behind you, {self.name}.",
                85: f"Believe in yourself, {self.name}. You are capable of achieving great things.",
                86: f"Your passion is waiting for your courage to catch up, {self.name}. Go for it.",
                87: f"Don’t count the days, make the days count, {self.name}. Live fully.",
                88: f"Success is not the key to happiness. Happiness is the key to success, {self.name}. Enjoy the journey.",
                89: f"Life is 10% what happens to us and 90% how we react to it, {self.name}. Choose positivity.",
                90: f"Challenges are what make life interesting, and overcoming them is what makes life meaningful, {self.name}.",
                91: f"Your limitation—it's only your imagination, {self.name}. Dream big.",
                92: f"Sometimes we’re tested not to show our weaknesses, but to discover our strengths, {self.name}.",
                93: f"The harder you work for something, the greater you’ll feel when you achieve it, {self.name}.",
                94: f"Dream bigger, {self.name}. Your potential is limitless.",
                95: f"Wake up with determination, {self.name}. Go to bed with satisfaction.",
                96: f"Do something today that your future self will thank you for, {self.name}.",
                97: f"Little things make big days, {self.name}. Cherish every moment.",
                98: f"It’s going to be hard, {self.name}, but hard does not mean impossible. Keep striving.",
                99: f"Don’t stop when you’re tired, {self.name}. Stop when you’re done.",
                100: f"Wake up with a purpose, {self.name}. Live your life with passion."}
            prediction = random.choice(list(predictions.values()))
            print("--------------------------------------------------------------------------------------------")
            print(prediction)
            print("--------------------------------------------------------------------------------------------")
            
m=Motivate.username("suriya")
