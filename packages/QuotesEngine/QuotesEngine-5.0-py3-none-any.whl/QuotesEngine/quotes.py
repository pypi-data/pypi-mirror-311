import random
from colorama import Fore, init, Style
import sys
import time

class Motivater:
    class username:
        def __init__(self, name: str) -> None:
            print()
            init(autoreset=True)
            self.name = name
            print(Style.BRIGHT + f"""Hello {Fore.CYAN}{self.name}{Style.RESET_ALL} !, {Fore.BLACK} this is my first project. {Style.RESET_ALL}""")        
        
        def motivate(self) -> str:
            print(f"choosing the best quote for you, {Fore.BLUE}{self.name}{Style.RESET_ALL}....", end="\r", flush=True)
            time.sleep(4)
            sys.stdout.write("\033[K\r")
            sys.stdout.flush()

            predictions = {
                1: f"Every day is a new beginning, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Take a deep breath, smile, and start again.",
                2: f"Remember, {Fore.CYAN}{self.name}{Style.RESET_ALL}, the only limit to our realization of tomorrow is our doubts of today.",
                3: f"Don’t watch the clock, {Fore.CYAN}{self.name}{Style.RESET_ALL}; do what it does. Keep going.",
                4: f"Believe you can, {Fore.CYAN}{self.name}{Style.RESET_ALL}, and you're halfway there.",
                5: f"The future belongs to those who believe in the beauty of their dreams, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep dreaming big.",
                6: f"Success is not final, failure is not fatal: It is the courage to continue that counts, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                7: f"The best way to predict the future is to create it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Start today!",
                8: f"You’re never too old to set another goal or to dream a new dream, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It's never too late.",
                9: f"Your limitation—it's only your imagination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Break free from it.",
                10: f"Push yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}, because no one else is going to do it for you.",
                11: f"Great things never come from comfort zones, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Step out and embrace the challenge.",
                12: f"Dream it. Wish it. Do it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Make it happen.",
                13: f"Success doesn’t just find you, {Fore.CYAN}{self.name}{Style.RESET_ALL}. You have to go out and get it.",
                14: f"The harder you work for something, the greater you’ll feel when you achieve it, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                15: f"Dream bigger. Do bigger, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Your potential is limitless.",
                16: f"Wake up with determination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go to bed with satisfaction.",
                17: f"Do something today that your future self will thank you for, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                18: f"Little things make big days, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Cherish every moment.",
                19: f"It’s going to be hard, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but hard does not mean impossible. Keep striving.",
                20: f"Don’t stop when you’re tired, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stop when you’re done.",
                21: f"Wake up with a purpose, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live your life with passion.",
                22: f"You are capable of amazing things, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Believe in yourself.",
                23: f"Your only limit is you, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be brave and fearless.",
                24: f"Sometimes you will never know the value of a moment until it becomes a memory, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                25: f"Life is tough, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but so are you. Keep fighting.",
                26: f"The best time for new beginnings is now, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Start today.",
                27: f"You don’t have to be great to start, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but you have to start to be great.",
                28: f"Every accomplishment starts with the decision to try, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                29: f"Life is not about finding yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It’s about creating yourself.",
                30: f"You are stronger than you think, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep pushing through.",
                31: f"Believe in the magic of new beginnings, {Fore.CYAN}{self.name}{Style.RESET_ALL}. They can change everything.",
                32: f"Your vibe attracts your tribe, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stay positive.",
                33: f"Be a voice, not an echo, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stand out.",
                34: f"Do what you can, with what you have, where you are, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                35: f"Life is a journey, and if you fall in love with the journey, you will be in love forever, {Fore.CYAN}{self.name }. Embrace every step.",
                36: f"Success usually comes to those who are too busy to be looking for it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep working hard.",
                37: f"Opportunities don’t happen, you create them, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Make your own path.",
                38: f"Don’t be pushed around by the fears in your mind, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be led by the dreams in your heart.",
                39: f"Everything you’ve ever wanted is on the other side of fear, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Face it bravely.",
                40: f"Success is walking from failure to failure with no loss of enthusiasm, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep your spirit high.",
                41: f"Your life does not get better by chance, it gets better by change, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Take the leap.",
                42: f"Act as if what you do makes a difference, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It does.",
                43: f"Success is not how high you have climbed, but how you make a positive difference to the world, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                44: f"Keep your face always toward the sunshine—and shadows will fall behind you, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                45: f"Believe in yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. You are capable of achieving great things.",
                46: f"Your passion is waiting for your courage to catch up, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go for it.",
                47: f"Don’t count the days, make the days count, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live fully.",
                48: f"Success is not the key to happiness. Happiness is the key to success, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Enjoy the journey.",
                49: f"Life is 10% what happens to us and 90% how we react to it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Choose positivity.",
                50: f"Challenges are what make life interesting, and overcoming them is what makes life meaningful, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                51: f"Your limitation—it's only your imagination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Dream big.",
                52: f"Sometimes we’re tested not to show our weaknesses, but to discover our strengths, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                53: f"The harder you work for something, the greater you’ll feel when you achieve it, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                54: f"Dream bigger, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Your potential is limitless.",
                55: f"Wake up with determination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go to bed with satisfaction.",
                56: f"Do something today that your future self will thank you for, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                57: f"Little things make big days, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Cherish every moment.",
                58: f"It’s going to be hard, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but hard does not mean impossible. Keep striving.",
                59: f"Don’t stop when you’re tired, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stop when you’re done.",
                60: f"Wake up with a purpose, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live your life with passion.",
                61: f"You are capable of amazing things, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Believe in yourself.",
                62: f"Your only limit is you, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be brave and fearless.",
                63: f"Sometimes you will never know the value of a moment until it becomes a memory, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                64: f"Life is tough, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but so are you. Keep fighting.",
                65: f"The best time for new beginnings is now, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Start today.",
                66: f"You don’t have to be great to start, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but you have to start to be great.",
                67: f"Every accomplishment starts with the decision to try, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                68: f"Life is not about finding yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It’s about creating yourself.",
                69: f"You are stronger than you think, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep pushing through.",
                70: f"Believe in the magic of new beginnings, {Fore.CYAN }{self.name}{Style.RESET_ALL}. They can change everything.",
                71: f"Your vibe attracts your tribe, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stay positive.",
                72: f"Be a voice, not an echo, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stand out.",
                73: f"Do what you can, with what you have, where you are, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                74: f"Life is a journey, and if you fall in love with the journey, you will be in love forever, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Embrace every step.",
                75: f"Success usually comes to those who are too busy to be looking for it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep working hard.",
                76: f"Opportunities don’t happen, you create them, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Make your own path.",
                77: f"Don’t be pushed around by the fears in your mind, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be led by the dreams in your heart.",
                78: f"Everything you’ve ever wanted is on the other side of fear, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Face it bravely.",
                79: f"Success is walking from failure to failure with no loss of enthusiasm, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep your spirit high.",
                80: f"Your life does not get better by chance, it gets better by change, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Take the leap.",
                81: f"Act as if what you do makes a difference, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It does.",
                82: f"Success is not how high you have climbed, but how you make a positive difference to the world, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                83: f"Keep your face always toward the sunshine—and shadows will fall behind you, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                84: f"Believe in yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. You are capable of achieving great things.",
                85: f"Your passion is waiting for your courage to catch up, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go for it.",
                86: f"Don’t count the days, make the days count, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live fully.",
                87: f"Success is not the key to happiness. Happiness is the key to success, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Enjoy the journey.",
                88: f"Life is 10% what happens to us and 90% how we react to it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Choose positivity.",
                89: f"Challenges are what make life interesting, and overcoming them is what makes life meaningful, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                90: f"Your limitation—it's only your imagination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Dream big.",
                91: f"Sometimes we’re tested not to show our weaknesses, but to discover our strengths, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                92: f"The harder you work for something, the greater you’ll feel when you achieve it, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                93: f"Dream bigger, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Your potential is limitless.",
                94: f"Wake up with determination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go to bed with satisfaction.",
                95: f"Do something today that your future self will thank you for, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                96: f"Little things make big days, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Cherish every moment.",
                97: f"It’s going to be hard, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but hard does not mean impossible. Keep striving.",
                98: f"Don’t stop when you’re tired, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stop when you’re done.",
                99: f"Wake up with a purpose, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live your life with passion.",
                100: f"You are capable of amazing things, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Believe in yourself.",
                101: f"Your only limit is you, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be brave and fearless.",
                102: f"Sometimes you will never know the value of a moment until it becomes a memory, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                103: f"Life is tough, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but so are you. Keep fighting.",
                104: f"The best time for new beginnings is now, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Start today.",
                105: f"You don’t have to be great to start, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but you have to start to be great.",
                106: f"Every accomplishment starts with the decision to try, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                107: f"Life is not about finding yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It’s about creating yourself.",
                108: f"You are stronger than you think, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep pushing through.",
                109: f"Believe in the magic of new beginnings, {Fore.CYAN}{self.name}{Style.RESET_ALL}. They can change everything.",
                110: f"Your vibe attracts your tribe, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stay positive.",
                111: f"Be a voice, not an echo, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stand out.",
                112: f"Do what you can, with what you have, where you are, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                113: f"Life is a journey, and if you fall in love with the journey, you will be in love forever, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Embrace every step.",
                114: f"Success usually comes to those who are too busy to be looking for it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep working hard.",
                115: f"Opportunities don’t happen, you create them, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Make your own path.",
                116: f"Don’t be pushed around by the fears in your mind, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be led by the dreams in your heart.",
                117: f"Everything you’ve ever wanted is on the other side of fear, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Face it bravely.",
                118: f"Success is walking from failure to failure with no loss of enthusiasm, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep your spirit high.",
                119: f"Your life does not get better by chance, it gets better by change, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Take the leap.",
                120: f"Act as if what you do makes a difference, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It does.",
                121: f"Success is not how high you have climbed, but how you make a positive difference to the world, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                122: f"Keep your face always toward the sunshine—and shadows will fall behind you, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                123: f"Believe in yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. You are capable of achieving great things.",
                124: f"Your passion is waiting for your courage to catch up, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go for it.",
                125: f"Don’t count the days, make the days count, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live fully.",
                126: f"Success is not the key to happiness. Happiness is the key to success, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Enjoy the journey.",
                127: f"Life is 10% what happens to us and 90% how we react to it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Choose positivity.",
                128: f"Challenges are what make life interesting, and overcoming them is what makes life meaningful, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                129: f"Your limitation—it's only your imagination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Dream big.",
                130: f"Sometimes we’re tested not to show our weaknesses, but to discover our strengths, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                131: f"The harder you work for something, the greater you’ll feel when you achieve it, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                132: f"Dream bigger, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Your potential is limitless.",
                133: f"Wake up with determination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go to bed with satisfaction.",
                134: f"Do something today that your future self will thank you for, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                135: f"Little things make big days, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Cherish every moment.",
                136: f"It’s going to be hard, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but hard does not mean impossible. Keep striving.",
                137: f"Don’t stop when you’re tired, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stop when you’re done.",
                138: f"Wake up with a purpose, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live your life with passion.",
                139: f"You are capable of amazing things, {Fore .CYAN}{self.name}{Style.RESET_ALL}. Believe in yourself.",
                140: f"Your only limit is you, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be brave and fearless.",
                141: f"Sometimes you will never know the value of a moment until it becomes a memory, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                142: f"Life is tough, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but so are you. Keep fighting.",
                143: f"The best time for new beginnings is now, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Start today.",
                144: f"You don’t have to be great to start, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but you have to start to be great.",
                145: f"Every accomplishment starts with the decision to try, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                146: f"Life is not about finding yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It’s about creating yourself.",
                147: f"You are stronger than you think, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep pushing through.",
                148: f"Believe in the magic of new beginnings, {Fore.CYAN}{self.name}{Style.RESET_ALL}. They can change everything.",
                149: f"Your vibe attracts your tribe, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stay positive.",
                150: f"Be a voice, not an echo, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stand out.",
                151: f"Do what you can, with what you have, where you are, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                152: f"Life is a journey, and if you fall in love with the journey, you will be in love forever, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Embrace every step.",
                153: f"Success usually comes to those who are too busy to be looking for it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep working hard.",
                154: f"Opportunities don’t happen, you create them, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Make your own path.",
                155: f"Don’t be pushed around by the fears in your mind, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be led by the dreams in your heart.",
                156: f"Everything you’ve ever wanted is on the other side of fear, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Face it bravely.",
                157: f"Success is walking from failure to failure with no loss of enthusiasm, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep your spirit high.",
                158: f"Your life does not get better by chance, it gets better by change, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Take the leap.",
                159: f"Act as if what you do makes a difference, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It does.",
                160: f"Success is not how high you have climbed, but how you make a positive difference to the world, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                161: f"Keep your face always toward the sunshine—and shadows will fall behind you, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                162: f"Believe in yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. You are capable of achieving great things.",
                163: f"Your passion is waiting for your courage to catch up, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go for it.",
                164: f"Don’t count the days, make the days count, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live fully.",
                165: f"Success is not the key to happiness. Happiness is the key to success, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Enjoy the journey.",
                166: f"Life is 10% what happens to us and 90% how we react to it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Choose positivity.",
                167: f"Challenges are what make life interesting, and overcoming them is what makes life meaningful, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                168: f"Your limitation—it's only your imagination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Dream big.",
                169: f"Sometimes we’re tested not to show our weaknesses, but to discover our strengths, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                170: f"The harder you work for something, the greater you’ll feel when you achieve it, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                171: f"Dream bigger, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Your potential is limitless.",
                172: f"Wake up with determination, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Go to bed with satisfaction.",
                173: f"Do something today that your future self will thank you for, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                174: f"Little things make big days, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Cherish every moment.",
                175: f"It’s going to be hard, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but hard does not mean impossible. Keep striving.",
                176: f"Don’t stop when you’re tired, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stop when you’re done.",
                177: f"Wake up with a purpose, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Live your life with passion.",
                178: f"You are capable of amazing things, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Believe in yourself.",
                179: f"Your only limit is you, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be brave and fearless.",
                180: f"Sometimes you will never know the value of a moment until it becomes a memory, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                181: f"Life is tough, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but so are you. Keep fighting.",
                182: f"The best time for new beginnings is now, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Start today.",
                183: f"You don’t have to be great to start, {Fore.CYAN}{self.name}{Style.RESET_ALL}, but you have to start to be great.",
                184: f"Every accomplishment starts with the decision to try, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                185: f"Life is not about finding yourself, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It’s about creating yourself.",
                186: f"You are stronger than you think, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep pushing through.",
                187: f"Believe in the magic of new beginnings, {Fore.CYAN}{self.name}{Style.RESET_ALL}. They can change everything.",
                188: f"Your vibe attracts your tribe, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stay positive.",
                189: f"Be a voice, not an echo, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Stand out.",
                190: f"Do what you can, with what you have, where you are, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                191: f"Life is a journey, and if you fall in love with the journey, you will be in love forever, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Embrace every step.",
                192: f"Success usually comes to those who are too busy to be looking for it, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep working hard.",
                193: f"Opportunities don’t happen, you create them, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Make your own path.",
                194: f"Don’t be pushed around by the fears in your mind, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Be led by the dreams in your heart.",
                195: f"Everything you’ve ever wanted is on the other side of fear, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Face it bravely.",
                196: f"Success is walking from failure to failure with no loss of enthusiasm, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Keep your spirit high.",
                197: f"Your life does not get better by chance, it gets better by change, {Fore.CYAN}{self.name}{Style.RESET_ALL}. Take the leap.",
                198: f"Act as if what you do makes a difference, {Fore.CYAN}{self.name}{Style.RESET_ALL}. It does.",
                199: f"Success is not how high you have climbed, but how you make a positive difference to the world, {Fore.CYAN}{self.name}{Style.RESET_ALL}.",
                200: f"Keep your face always toward the sunshine—and shadows will fall behind you, {Fore.CYAN}{self.name}{Style.RESET_ALL}."
            }
            predicted_num = random.randint(1, 200)
            prediction = predictions.get(predicted_num, "Sorry, I couldn't find a prediction for you now...")
            length = len(prediction)
            forma=input("Enter which format(text/box): ").lower()
            if forma=="text":
                print(prediction)
            elif forma=="box":
            # Print the border and the quote
                self.print_box(length, prediction)
            else:
                print("Invalid input. Please enter either 'text' or 'box'")
        
        def print_box(self, length: int, prediction: str) -> None:
            # This function prints the quote inside a box with appropriate width
            try:
                print("┌" + '─' * length + "┐")
                print('│' + " " * 5 + f"{prediction}" + " " * 4 + '│')
                print("└" + '─' * length + '┘')
            except UnicodeEncodeError:
                print("Error: Unable to print Unicode characters. Please check your terminal encoding settings.")
                
    class farewell:
        
        def __init__(self, name: str) -> None:
            self.name = name
            print(Fore.WHITE + Style.BRIGHT + f"""It was nice having you, {self.name}{Style.RESET_ALL}""")
            print(Fore.CYAN + f"Goodbye, {self.name}{Style.RESET_ALL}!")
            print(Style.RESET_ALL)

