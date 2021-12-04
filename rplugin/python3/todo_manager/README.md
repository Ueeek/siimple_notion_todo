A simple Neovim remote plugin for Todo-list Management on Notion

# Setup
You have to set some environment variables before use this
```
export NOTION_TODO_TOKEN_V2=''
export NOTION_TODO_PAGE_URLL=``
```
* token v2 is auth-token which you can find it in Cokkie of notion
* PAGE_URL is the page url you use to this plugin
    * recommend to create new_page for this plugin


# Usage
```
:NotionTodoTodoList
```
* create new split window and show todo-list

```
:NotionTodoAddTodo task_name
```
* create new_entry named "task_name" in todo_list

```
:NotionTodoDeleteTodo task_idx
```
* delete {task_idx}-th entry from todo_list
* index is 0-origin

```
:NotionTodoToggleTodo task_idx
```
* toggle {done,not_done} status of {task_idx}-th entry in todo_list

# Caution
* this plugin edit notion-page
    * DO NOT SET IMPORTANT NOTION PAGE 
        * create new page for this plugin is recommended

# LIMITATION
* TodoBlockにしか対応してないので、その他のobjは無視されます
* nested Todoには対応してないです。
        
