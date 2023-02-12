from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі

#підвантажуємо окремо функції для роботи зі шрифтом

# шрифти і написи
font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont("Arial", 36)

# фонова музика
"""mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 """
# нам потрібні такі картинки:
img_back = "galaxy.jpg"  # фон гри
img_hero = "rocket.png"  # герой
img_bullet = "bullet.png" # куля
img_enemy = "ufo.png"  # ворог
img_ast = "asteroid.png" # астероїд

score = 0  # збито кораблів
goal = 10 # стільки кораблів потрібно збити для перемоги
lost = 0  # пропущено кораблів
max_lost = 3 # програли, якщо пропустили стільки
life = 3  # очки життя

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# клас спрайта-кулі   
class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# створення групи спрайтів-ворогів
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)



bullets = sprite.Group()

# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна

rel_time = False  # прапор, що відповідає за перезаряджання

num_fire = 0  # змінна для підрахунку пострілів    

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        #подія натискання на пробіл - спрайт стріляє
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #перевіряємо, скільки пострілів зроблено і чи не відбувається перезаряджання
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    #fire_sound.play()
                    ship.fire()
                    
                if num_fire >= 5 and rel_time == False : #якщо гравець зробив 5 пострілів
                    last_time = timer() #засікаємо час, коли це сталося
                    rel_time = True #ставимо прапор перезарядки

    # сама гра: дії спрайтів, перевірка правил гри, перемальовка
    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))

        # рухи спрайтів
        ship.update()
        monsters.update()
        bullets.update()
 
        #оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # перезарядка
        if rel_time == True:
            now_time = timer() # зчитуємо час
         
            if now_time - last_time < 3: #поки не минуло 3 секунди виводимо інформацію про перезарядку
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0     #обнулюємо лічильник куль
                rel_time = False #скидаємо прапор перезарядки

         #перевірка зіткнення кулі та монстрів (і монстр, і куля при дотику зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #Цей цикл повториться стільки разів, скільки монстрів підбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        '''
        # можливий програш: пропустили занадто багато чи герой зіткнувся з ворогом чи астероїдом
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= max_lost:
            finish = True # програли, ставимо тло і більше не керуємо спрайтами.
            window.blit(lose, (200, 200))
        '''
        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True) 
            life = life -1

        #програш
        if life == 0 or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))

        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # задаємо різний колір залежно від кількості життів
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    #бонус: автоматичний перезапуск гри
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()    
      

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)   

    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)