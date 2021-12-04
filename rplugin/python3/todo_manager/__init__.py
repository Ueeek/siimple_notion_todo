from notion.client import NotionClient
from notion.block import TodoBlock
from notion.block import PageBlock
import json
import pynvim
import os


_command_prefix="NotionTodo"

@pynvim.plugin
class TodoAPI:
    keys:Dict
    nvim:pynvim.Nvim
    client:NotionClient
    page:Any
    todo_list:List

    def __init__(self,nvim:pynvim.Nvim):
        self.set_api_key()
        self.client = NotionClient(token_v2=self.keys["TOKEN_V2"])
        self.page = self.client.get_block(self.keys["PAGE_URL"])
        self.update_list()


    def update_list(self):
        self.page = self.client.get_block(self.keys["PAGE_URL"])
        self.todo_list=self.get_members()


    def set_api_key(self):
        keys=["TOKEN_V2","PAGE_URL"]
        for key in keys:
            if os.getenv("NOTION_TODO_{}".format(key)) is None:
                raise Exception("Required Environment variables are missing")
            else:
                self.keys[key]=os.getenv("NOTION_TODO_{}".format(key))

    def get_members(self)->List:
        cur_todos=[(child.title,child.checked) for child in self.page.children if isinstance(child,TodoBlock)]
        
        return cur_todos

    def show_list(self):
        self.nvim.command('setlocal modifiable')
        for todo,checked in self.todo_list:
            if checked:
                preseq="[x]:"
            else:
                preseq="[ ]:"
            self.nvim.current.buffer.append(preseq+todo)
        self.nvim.current.window.cursor=(1,1)
        self.nvim.command('setlocal nomodifiable')

    @pynvim.command(_command_prefix+"AddTodo",nargs=1)
    def add_new_todo(self,title):
        if len(title)==0:
            raise Exception("tilte is required")
        else:
            self.page.children.add_new(TodoBlock,title=title[0])
        self.echo("add {}".format(title[0]))
        self.update_list()

    @pynvim.command(_command_prefix+"DeleteTodo",nargs=1)
    def delete_todo(self,idx):
        child = self.page.children[int(idx[0])]
        removing_title=child.title
        child.remove()
        self.echo("remove {}".format(removing_title))
        self.update_list()


    @pynvim.command(_command_prefix+"ToggleTodo",nargs=1)
    def toggle_checked(self,idx):
        child = self.page.children[int(idx[0])]
        child.checked = not child.checked
        self.update_list()
        self.echo("Toggle {}".format(child.title))

    @pynvim.command(_command_prefix+"TodoList")
    def todoList(self):
        self.nvim.command('setlocal splitright')
        self.nvim.command('vnew')
        self.nvim.command('setlocal buftype=nofile bufhidden=hide nolist nonumber nomodifiable wrap')
        self.show_list()
