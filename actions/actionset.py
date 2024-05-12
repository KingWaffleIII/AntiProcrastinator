import importlib

from .action import Action


class ActionSet:
    def __init__(self, actions: list[Action] = None):
        """
        Creates a set of Actions.
        """
        self.actions = actions if actions is not None else []

    def to_json(self):
        """
        Converts the action set to JSON.
        :return: JSON representation of the action set.
        """
        return [action.to_json() for action in self.actions]

    def add_action(self, action: Action):
        """
        Adds an action to the set.
        :param action: the action to add.
        """
        self.actions.append(action)

    def add_actions(self, actions: list[Action]):
        """
        Adds multiple actions to the set.
        :param actions: the actions to add.
        """
        self.actions.extend(actions)

    def load_json(self, json: list):
        """
        Loads actions from JSON.
        :param json: the JSON to load.
        """
        import util

        for action in json:
            module = importlib.import_module(f"actions.{action['action'].lower()}")
            condition_func = action['condition_func']
            if condition_func is not None:
                action['condition_func'] = util.functions.build_condition_function(
                    condition_func['function'],
                    condition_func['inverse'],
                    condition_func['args']
                )
            args = {k: v for k, v in action.items() if k != 'action'}
            self.actions.append(getattr(module, action['action'])(**args))

    def remove_action(self, action: Action):
        """
        Removes an action from the set.
        :param action: the action to remove.
        """
        self.actions.remove(action)

    async def execute(self, *args, **kwargs):
        """
        Executes all actions in the set.
        """
        for action in self.actions:
            await action.execute(*args, **kwargs)

    async def execute_action(self, index: int, *args, **kwargs):
        """
        Executes a specific action in the set.
        """
        await self.actions[index].execute(*args, **kwargs)
