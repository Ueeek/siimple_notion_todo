from notion.client import NotionClient
from notion.block import TodoBlock
from notion.block import PageBlock
import json
import pynvim
import os


_command_prefix="NotionTodo"

@pynvim.plugin
class TodoAPI:

    def __init__(self,nvim):
        self.keys=dict()
        self.nvim=nvim
        self.set_api_key()
        self.client = NotionClient(token_v2=self.keys["TOKEN_V2"])
        self.page = self.client.get_block(self.keys["PAGE_URL"])

    def echo(self,msg):
        self.nvim.command("echo '" + msg + "'")

    def set_api_key(self):
        keys=["TOKEN_V2","PAGE_URL"]
        for key in keys:
            if os.getenv("NOTION_TODO_{}".format(key)) is None:
                raise Exception("Required Environment variables are missing")
            else:
                self.keys[key]=os.getenv("NOTION_TODO_{}".format(key))

    def get_members(self):
        cur_todos=[child.title for child in self.page.children]
        return cur_todos

    @pynvim.command(_command_prefix+"AddTodo",nargs=1)
    def add_new_todo(self,title):
        self.echo("success")
        self.echo(title[0][0])
        self.echo(title[0])
        if len(title)==0:
            raise Exception("tilte is required")
        else:
            self.page.children.add_new(TodoBlock,title=title[0][0])

    @pynvim.command(_command_prefix+"DeleteTodo",nargs=1)
    def delete_todo(self,idx):
        self.echo("delete {}".format(str(idx)))
        child = self.page.children[int(idx)]
        child.remove()

    @pynvim.command(_command_prefix+"ToggleTodo",nargs=1)
    def toggle_checked(self,idx):
        self.echo("toggle {}".format(str(idx)))
        child = self.page.children[int(dx)]
        child.checked = not child.checked
