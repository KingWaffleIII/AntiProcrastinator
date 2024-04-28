from .action import Action


class ActionSet:
    def __init__(self, repeat: bool = False):
        """
        Creates a set of Actions.

        :param repeat: whether to repeat the set of actions after executing all actions. Only use when using multiprocessing (so you can terminate the ActionSet).
        """
        self.actions = []
        self.repeat = repeat

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

        if self.repeat:
            await self.execute(*args, **kwargs)

    async def execute_action(self, index: int, *args, **kwargs):
        """
        Executes a specific action in the set.
        """
        await self.actions[index].execute(*args, **kwargs)
