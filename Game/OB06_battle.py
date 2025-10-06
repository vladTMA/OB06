# 0B06_battle.py

# Модуль боевой логики: абстракция оружия, подклассы и случайный выбор

from abc import ABC, abstractmethod
import random # для вероятностной атаки и выбора оружия

# Создаем абстрактный базовый класс - оружие
class Weapon(ABC):
    @abstractmethod
    def attack(self) -> int:
        # Возвращает полученный урон
        pass

# Создаем подклассы оружия
# int показывает степень урона при применении разного оружия, выражается целым числом
# Подкласс - меч
class Sword(Weapon):
    def attack(self) -> int:
        return 30 if random.random() <0.9 else 0 # шанс удара 90%


# Подкласс - лук
class Bow(Weapon):
    def attack(self) -> int:
        return 20 if random.random() <0.8 else 0 # шанс удара 80%


# Подкласс - кинжал
class Dagger(Weapon):
    def attack(self) -> int:
        return 10 if random.random() <0.95 else 0 # шанс 95%


# Создаем класс случайного выбора оружия их доступного
class WeaponSelector:
    def __init__(self, weapons: list[Weapon]):
        self.weapons = weapons

    def get_random_weapon(self) -> Weapon:
        return random.choice(self.weapons)


# Создаем абстрактный класс защиты: определяет интерфейс поглощения урона
class Defence(ABC):
    @abstractmethod
    def absorb_damage(self, damage: int) -> int:
      # Возвращает урон после применения защиты
      pass

# Подклассы:

# Без защиты: урон не уменьшается
class NoDefence(Defence):
    def absorb_damage(self, damage: int) -> int:
        return damage


# Броня: уменьшает урон на фиксированное значение (10 единиц)
class Armor(Defence):
    def absorb_damage(self, damage: int) -> int:
        return max(damage - 10,0)


# Волшебный щит: поглощает половину входящего урона
class MagicShield(Defence):
    def absorb_damage(self, damage: int) -> int:
        return damage // 2  # поглощает половину урона


# Создаем класс героя: содержит имя, здоровье, оружие и защиту
class Hero:
    def __init__(self, name: str, weapon: Weapon, defence: Defence):
        self.name = name
        self.health = 100
        self.weapon = weapon
        self.defence = defence

    # Возвращаем название используемой защиты
    def get_defence_name(self) -> str:
        return self.defence.__class__.__name__

    # Атакуем противника и выводим результат боя
    def attack(self, other: "Hero"):
        weapon_name = self.weapon.__class__.__name__
        defence_name = other.get_defence_name()
        raw_damage = self.weapon.attack()

        print(f"{self.name} применил {weapon_name}.")
        print(f"{other.name} использует защиту: {defence_name}.")

        if raw_damage == 0:
            print(f"{self.name} промах!")
            return

        actual_damage = other.defence.absorb_damage(raw_damage)
        other.health -= actual_damage

        if actual_damage < raw_damage:
            print(f"{other.name} частично защитился. Урон составил: {actual_damage}")
        else:
            print(f"{other.name} Полный урон {actual_damage}")

        health_percent = max(other.health, 0) 
        print(f"осталось здоровья: {int(health_percent)}%")

    # Проверяем, жив ли герой
    def is_alive(self) -> bool:
        return self.health > 0


# Создаем класс игры с управлением боем и чередованием ходов
class Game:
    def __init__(self, player: Hero, computer: Hero):
        self.player = player
        self.computer = computer

    # Начинаем бой и чередуем ходы до победы одного из участников
    def start(self):
        print("Батл начинается!")
        round_number = 1
        selector = WeaponSelector([Sword(), Bow(), Dagger()])

        while self.player.is_alive() and self.computer.is_alive():
            print(f"\nРаунд {round_number}:")

            # Смена оружия перед каждым раундом
            self.player.weapon = selector.get_random_weapon()
            self.computer.weapon = selector.get_random_weapon()

            # Ход героя
            self.player.attack(self.computer)
            if not self.computer.is_alive():
                print(f"\n{self.computer.name} повержен! Победил {self.player.name}!")
                break

            # Ход компьютера
            self.computer.attack(self.player)
            if not self.player.is_alive():
                print(f"\n{self.player.name} повержен! Победил {self.computer.name}!")
                break

            # Нумерация раундов, начинаем с 1 и далее +1
            round_number += 1

        print("\nИгра завершена.")


# Метод автоматизирует один ход с расчётом урона и выводом текста
def simulate_turn(attacker: Hero, defender: Hero) -> str:
    if not attacker.is_alive():
        return f"{attacker.name} мёртв и не может атаковать."

    if not defender.is_alive():
        return f"{defender.name} уже мёртв."

    # Выводим результата атаки
    print(f"{attacker.name} применил {attacker.weapon.__class__.__name__}.")
    print(f"{defender.name} использует защиту: {defender.defence.__class__.__name__}.")

    damage = attacker.weapon.attack()
    absorbed = defender.defence.absorb_damage(damage)
    defender.health -= absorbed
    defender.health = max(defender.health, 0)

    if absorbed == 0:
        result = f"{defender.name} полностью защитился."
    elif absorbed == damage:
        result = f"{defender.name} не смог защитится. Урон: {absorbed}"
    else:
        result = f"{defender.name} частично защитился. Урон составил: {absorbed}"

    print(result)
    print(f"Осталось здоровья: {defender.health}%")

    return result


# Точка входа: инициализация компонентов и запуск боя
if __name__ == "__main__":
    # Создаём оружие
    sword = Sword()
    bow = Bow()
    dagger = Dagger()

    # Создаём защиту
    armor = Armor()
    shield = MagicShield()

    # Участники боя с выбранным оружием и защитой
    player = Hero(name="Игрок", weapon=sword, defence=armor)
    computer = Hero(name="Компьютер", weapon=bow, defence=shield)

    # Запускаем игру по шагам
    game = Game(player, computer)
    game.start()











