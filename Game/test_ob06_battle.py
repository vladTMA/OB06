# test_ob06_battle

# Юнит-тесты для боевой логики: оружие, защита, герои и симуляция боя
import unittest
from OB06_battle import Sword, Bow, Dagger, Armor, MagicShield, NoDefence, Hero, simulate_turn


class TestBattleMechanics(unittest.TestCase):
    # Проверка урона от оружия (меч: 0 или 30)
    def test_weapon_damage(self):
        sword = Sword()
        for _ in range(100):
            damage = sword.attack()
            self.assertIn(damage, [0, 30])

    # Проверка логики защиты: броня, щит, отсутствие защиты
    def test_defense_logic(self):
        armor = Armor()
        self.assertEqual(armor.absorb_damage(25), 15)
        shield = MagicShield()
        self.assertEqual(shield.absorb_damage(20), 10)
        nodef = NoDefence()
        self.assertEqual(nodef.absorb_damage(20), 20)

    # Проверка уменьшения здоровья после атаки
    def test_hero_attack_reduces_health(self):
        attacker = Hero("A", Sword(), NoDefence())
        defender = Hero("B", Bow(), Armor())
        initial_health = defender.health
        attacker.attack(defender)
        self.assertLessEqual(defender.health, initial_health)

    # Проверка состояния героя после смерти
    def test_hero_death(self):
        hero = Hero("X", Dagger(), NoDefence())
        hero.health = 0
        self.assertFalse(hero.is_alive())

    # Проверка симуляции одного хода атаки
    def test_simulate_turn(self):
        attacker = Hero("A", Sword(), NoDefence())
        defender = Hero("B", Bow(), Armor())
        result = simulate_turn(attacker, defender)
        self.assertIn("Урон", result)


# Запуск тестов при прямом запуске файла
if __name__ == "__main__":
    unittest.main()

