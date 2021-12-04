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
        self.todo_list=self.get_members()

    def echo(self,msg):
        self.nvim.command("echo '{}'".format(msg))

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

    def prependTodos(self):
        self.nvim.command('setlocal modifiable')
        for todo in self.todo_list:
            self.nvim.current.buffer.append(todo,0)
        self.nvim.current.window.cursor=(1,1)
        self.nvim.command('setlocal nomodifiable')

    @pynvim.command(_command_prefix+"AddTodo",nargs=1)
    def add_new_todo(self,title):
        if len(title)==0:
            raise Exception("tilte is required")
        else:
            self.page.children.add_new(TodoBlock,title=title[0])
        self.echo("add {}".format(title[0]))

    @pynvim.command(_command_prefix+"DeleteTodo",nargs=1)
    def delete_todo(self,idx):
        child = self.page.children[int(idx[0])]
        removing_title=child.title
        child.remove()
        self.echo("remove {}".format(removing_title))


    @pynvim.command(_command_prefix+"ToggleTodo",nargs=1)
    def toggle_checked(self,idx):
        child = self.page.children[int(idx)]
        child.checked = not child.checked
        self.echo("Toggle {}".format(child.title))

    @pynvim.command(_command_prefix+"TodoList")
    def todoList(self):
        self.nvim.command('setlocal splitright')
        self.nvim.command('vnew')
        self.nvim.command('setlocal buftype=nofile bufhidden=hide nolist nonumber nomodifiable wrap')
        self.prependTodos().generate(self.nvim.current.window.width)
