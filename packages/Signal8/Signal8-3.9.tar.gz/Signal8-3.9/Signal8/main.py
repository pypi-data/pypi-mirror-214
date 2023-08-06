import Signal8

env = Signal8.env()
env.reset(options={'problem_instance': 'circle'})
start_state = env.state()
observation, _, terminations, truncations, _ = env.last()
start_state = env.state()
env.step(1)
env.step(1)
env.close()
