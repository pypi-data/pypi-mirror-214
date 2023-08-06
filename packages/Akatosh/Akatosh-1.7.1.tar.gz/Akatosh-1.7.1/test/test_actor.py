from typing import Callable
from Akatosh import Actor, Mundus



def test_actor_creation():

    actor1 = Actor(lambda: None, at=0)
    assert actor1.time == 0
