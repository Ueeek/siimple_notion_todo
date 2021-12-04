from notion.client import NotionClient
from notion.block import TodoBlock
from notion.block import PageBlock
import json
import pynvim
import os


@pynvim.plugin
class TodoAPI:

    def __init__(self,nvim):
        self.keys=dict()
        self.nvim=nvim
        self.set_api_key()
        self.client = NotionClient(token_v2=self.keys["TOKEN_V2"])
        self.page = self.client.get_block(self.keys["PAGE_URL"])
        print("page=>",self.page)

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

    @pynvim.function("AddTodo")
    def add_new_odo(self,title):
        if len(title)==0:
            raise Exception("tilte is required")
        else:
            self.pag.children.add_new(TodoBlock,title=title[0])

    @pynvim.funcion("DeleteTodo")
    def delete_tdo(self,idx):
        print("delete called idx:{}".format(idx))
        child = self.page.children[idx]
        child.remove()

    @pynvim.function("ToggleTodo")
    def toggle_checked(self,idx):
        print("toggle_cheched idx:{}".format(idx))
        child = self.page.children[idx]
        child.checked = not child.checked
