import os
import tempfile
import pytest
import time
from .context import make_app, mongo, User, Window, Group

class TestUser:
    def setup(self):
        self.user = User.create("pytest", "pytest")
        self.group = Group.create("name")
        if self.user is None:
            self.user = User.find_by_username("pytest")
        self.window = Window.create(time.time(), 1000, self.group.obj["_id"])

    def teardown(self):
        print("\nTearing down")
        User.delete(self.user.obj["_id"])
        Window.delete(self.window.obj["_id"])
        Group.delete(self.group.obj["_id"])

    def test_user_exists(self):
        user = User.find_by_username("pytest")
        assert user is not None

    def test_find_by_id(self):
        user = User.find_by_id(self.user.obj["_id"])
        assert user is not None

    def test_find_by_username(self):
        user = User.find_by_username(self.user.obj["username"])
        assert user is not None

    def test_has_no_window_then_does(self):
        assert not self.user.has_window(self.window.obj["_id"])
        self.user.add_window(self.window.obj["_id"])
        assert self.user.has_window(self.window.obj["_id"]) == True
        self.user.remove_window(self.window.obj["_id"])
        assert not self.user.has_window(self.window.obj["_id"])

    def test_detects_active(self):
        self.user.add_window(self.window.obj["_id"])
        assert self.user.in_window()
        self.user.remove_window(self.window.obj["_id"])


class TestWindow:
    def setup(self):
        self.user = User.create("pytest", "pytest")
        self.group = Group.create("name")
        if self.user is None:
            self.user = User.find_by_username("pytest")
        self.window = Window.create(time.time(), 1000, self.group.obj["_id"])

    def teardown(self):
        print("\nTearing down")
        User.delete(self.user.obj["_id"])
        Window.delete(self.window.obj["_id"])
        Group.delete(self.group.obj["_id"])

    def test_add_user(self):
        assert len(self.window.obj["users"])==0
        assert self.window.add_user(self.user.obj["_id"])
        assert len(self.window.obj["users"])==1
        assert self.window.remove_user(self.user.obj["_id"])
        assert len(self.window.obj["users"])==0


test_data = [{
  "username": "Tin",
  "password": "Stepmom"
}, {
  "username": "Zamit",
  "password": "Captain Phillips"
}, {
  "username": "Regrant",
  "password": "Keeper of the Flame"
}, {
  "username": "Gembucket",
  "password": "Orwell Rolls in His Grave"
}, {
  "username": "Hatity",
  "password": "League of Extraordinary Gentlemen, The (a.k.a. LXG)"
}, {
  "username": "Alphazap",
  "password": "John Q"
}, {
  "username": "Vagram",
  "password": "Sun Also Rises, The"
}, {
  "username": "Latlux",
  "password": "Sekirei"
}, {
  "username": "Pannier",
  "password": "Last Time I Saw Paris, The"
}, {
  "username": "Kanlam",
  "password": "Nick Fury: Agent of S.H.I.E.L.D."
}, {
  "username": "Andalax",
  "password": "Spy Kids 3-D: Game Over"
}, {
  "username": "Home Ing",
  "password": "Kon-Tiki"
}, {
  "username": "Kanlam",
  "password": "Master, The"
}, {
  "username": "Keylex",
  "password": "Unfaithful"
}, {
  "username": "Regrant",
  "password": "Om Shanti Om"
}, {
  "username": "Konklux",
  "password": "Bluebeard (Landru)"
}, {
  "username": "Zaam-Dox",
  "password": "Black Magic Rites & the Secret Orgies of the 14th Century (Riti, magie nere e segrete orge nel trecento...)"
}, {
  "username": "Treeflex",
  "password": "Perfect Stranger"
}, {
  "username": "Tin",
  "password": "Of Human Bondage"
}, {
  "username": "Holdlamis",
  "password": "Zombie Honeymoon"
}, {
  "username": "Zoolab",
  "password": "Glass Web, The"
}, {
  "username": "Fintone",
  "password": "Libre échange"
}, {
  "username": "Transcof",
  "password": "The Plague of the Zombies"
}, {
  "username": "Regrant",
  "password": "Patton Oswalt: Tragedy Plus Comedy Equals Time"
}, {
  "username": "Alphazap",
  "password": "Sokkotanssi"
}, {
  "username": "Tresom",
  "password": "Desk Set"
}, {
  "username": "Cookley",
  "password": "Velvet Goldmine"
}, {
  "username": "Quo Lux",
  "password": "Mimino"
}, {
  "username": "Home Ing",
  "password": "Texas Chainsaw Massacre: The Beginning, The"
}, {
  "username": "Stringtough",
  "password": "Fuck You, Goethe (Fack Ju Göhte)"
}, {
  "username": "Zaam-Dox",
  "password": "Wayne's World 2"
}, {
  "username": "Namfix",
  "password": "Bonneville"
}, {
  "username": "Solarbreeze",
  "password": "Which Way Is the Front Line From Here?  The Life and Time of Tim Hetherington"
}, {
  "username": "Flexidy",
  "password": "Story of Qiu Ju, The (Qiu Ju da guan si)"
}, {
  "username": "Ventosanzap",
  "password": "Still of the Night"
}, {
  "username": "Andalax",
  "password": "Noel"
}, {
  "username": "Regrant",
  "password": "The Boy"
}, {
  "username": "Home Ing",
  "password": "Summer of '42"
}, {
  "username": "Overhold",
  "password": "Hole, The (Dong)"
}, {
  "username": "Sonair",
  "password": "African Queen, The"
}, {
  "username": "Temp",
  "password": "St. Ives"
}, {
  "username": "Temp",
  "password": "Repentance"
}, {
  "username": "Bitwolf",
  "password": "American Heart"
}, {
  "username": "Viva",
  "password": "Monsieur Lazhar"
}, {
  "username": "Solarbreeze",
  "password": "Rainmaker, The"
}, {
  "username": "Opela",
  "password": "I Start Counting"
}, {
  "username": "Andalax",
  "password": "Anvil! The Story of Anvil"
}, {
  "username": "Konklab",
  "password": "Knocked Up"
}, {
  "username": "Zontrax",
  "password": "1408"
}, {
  "username": "Cardify",
  "password": "Treatment, The"
}, {
  "username": "Sub-Ex",
  "password": "Enemy at the Gates"
}, {
  "username": "Quo Lux",
  "password": "Barenaked in America"
}, {
  "username": "Tempsoft",
  "password": "Savage Messiah"
}, {
  "username": "Flowdesk",
  "password": "July Rhapsody (Laam yan sei sap)"
}, {
  "username": "Alpha",
  "password": "Great Flamarion, The"
}, {
  "username": "Ventosanzap",
  "password": "Planet B-Boy"
}, {
  "username": "Tin",
  "password": "Red Dragon"
}, {
  "username": "Trippledex",
  "password": "Kids, The (Mistons, Les) (Mischief Makers, The)"
}, {
  "username": "Bitchip",
  "password": "Kestrel's Eye (Falkens öga)"
}, {
  "username": "Zaam-Dox",
  "password": "Save the Last Dance 2"
}, {
  "username": "Pannier",
  "password": "My Boss's Daughter"
}, {
  "username": "Cardguard",
  "password": "Dragon Ball: The Curse Of The Blood Rubies (Doragon bôru: Shenron no densetsu)"
}, {
  "username": "Zontrax",
  "password": "X"
}, {
  "username": "Cardguard",
  "password": "Nightwatching"
}, {
  "username": "Regrant",
  "password": "Dear Brigitte"
}, {
  "username": "Duobam",
  "password": "Three Musketeers, The"
}, {
  "username": "Bitchip",
  "password": "Abandon Ship! (Seven Waves Away)"
}, {
  "username": "Redhold",
  "password": "Super Fly (Superfly)"
}, {
  "username": "Vagram",
  "password": "Buffalo Bill and the Indians, or Sitting Bull's History Lesson (a.k.a. Buffalo Bill and the Indians)"
}, {
  "username": "Bitchip",
  "password": "Soup to Nuts"
}, {
  "username": "Tres-Zap",
  "password": "Björk at the Royal Opera House"
}, {
  "username": "Subin",
  "password": "Steal Big, Steal Little"
}, {
  "username": "Veribet",
  "password": "Belle Starr"
}, {
  "username": "Mat Lam Tam",
  "password": "Four Lions"
}, {
  "username": "Tresom",
  "password": "Half Moon Street"
}, {
  "username": "Fintone",
  "password": "Alone in the Dark II"
}, {
  "username": "Subin",
  "password": "Across the Tracks"
}, {
  "username": "Prodder",
  "password": "Nasty Girl, The (schreckliche Mädchen, Das)"
}, {
  "username": "Bytecard",
  "password": "Arizona Raiders"
}, {
  "username": "Holdlamis",
  "password": "Cinemania"
}, {
  "username": "Flexidy",
  "password": "Take Me Home Tonight"
}, {
  "username": "Rank",
  "password": "Brown Sugar"
}, {
  "username": "Fintone",
  "password": "Maniac"
}, {
  "username": "Job",
  "password": "What Alice Found"
}, {
  "username": "Home Ing",
  "password": "Four Rooms"
}, {
  "username": "Daltfresh",
  "password": "Miracle on 34th Street"
}, {
  "username": "Opela",
  "password": "Secret Society"
}, {
  "username": "Zamit",
  "password": "Lorna"
}, {
  "username": "Job",
  "password": "What Richard Did"
}, {
  "username": "Keylex",
  "password": "Stay"
}, {
  "username": "Ronstring",
  "password": "Amazing Panda Adventure, The"
}, {
  "username": "Voyatouch",
  "password": "Jaws 3-D"
}, {
  "username": "Solarbreeze",
  "password": "Death Note 2: The Last Name"
}, {
  "username": "Alpha",
  "password": "On the Job"
}, {
  "username": "Span",
  "password": "Cargo"
}, {
  "username": "Treeflex",
  "password": "Evil Remains (Trespassing)"
}, {
  "username": "Biodex",
  "password": "Sea Hawk, The"
}, {
  "username": "Redhold",
  "password": "Deuce Bigalow: Male Gigolo"
}, {
  "username": "Y-Solowarm",
  "password": "Child, The (L'enfant)"
}, {
  "username": "Sonsing",
  "password": "Sacco and Vanzetti (Sacco e Vanzetti)"
}]